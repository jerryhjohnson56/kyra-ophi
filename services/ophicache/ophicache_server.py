#!/usr/bin/env python3
import argparse, hashlib, json, os, pathlib, shutil, sys, time
from typing import Optional
import yaml
from fastapi import FastAPI, HTTPException, UploadFile, File, Body, Request
from fastapi.responses import StreamingResponse, JSONResponse
import aiofiles
import urllib.parse, urllib.request

app = FastAPI(title="OphiCache", version="1.0")

CFG = {}
COUNTERS = {"hits":0,"misses":0,"ingest":0,"bytes_served":0}
STORAGE = None

def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def blob_path(digest: str) -> pathlib.Path:
    p = pathlib.Path(STORAGE) / "blobs" / "sha256" / digest[:2] / digest
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def name_manifest(name: str) -> pathlib.Path:
    p = pathlib.Path(STORAGE) / "names" / f"{name}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def save_name(name:str, digest:str, size:int):
    mp = name_manifest(name)
    mp.write_text(json.dumps({"name":name,"sha256":digest,"size":size}, indent=2))

def load_name(name:str):
    mp = name_manifest(name)
    if mp.exists():
        return json.loads(mp.read_text())
    return None

def list_index():
    names_dir = pathlib.Path(STORAGE) / "names"
    if not names_dir.exists(): return []
    out = []
    for p in names_dir.glob("*.json"):
        try:
            out.append(json.loads(p.read_text()))
        except Exception:
            continue
    return out

def store_blob_from_file(src_path: pathlib.Path, expected_sha256: Optional[str]=None, name: Optional[str]=None) -> str:
    digest = sha256_file(src_path)
    if expected_sha256 and expected_sha256.lower() != digest.lower():
        raise HTTPException(status_code=400, detail="sha256 mismatch for uploaded file")
    dst = blob_path(digest)
    if not dst.exists():
        shutil.copy2(src_path, dst)
    size = dst.stat().st_size
    if name:
        save_name(name, digest, size)
    return digest

def fetch_and_cache(url: str, expected_sha256: Optional[str]=None, name: Optional[str]=None) -> str:
    tmpdir = pathlib.Path(STORAGE) / "tmp"
    tmpdir.mkdir(parents=True, exist_ok=True)
    tmp = tmpdir / f"dl-{int(time.time())}-{os.getpid()}"
    with urllib.request.urlopen(url) as r, open(tmp, "wb") as w:
        shutil.copyfileobj(r, w, length=1024*1024)
    digest = store_blob_from_file(tmp, expected_sha256, name)
    try: tmp.unlink()
    except Exception: pass
    return digest

@app.on_event("startup")
async def on_start():
    global STORAGE, CFG
    pathlib.Path(STORAGE, "db").mkdir(parents=True, exist_ok=True)

@app.get("/v1/index")
async def v1_index():
    return JSONResponse({"items": list_index(), "counters": COUNTERS})

@app.get("/v1/packs/{digest}")
async def v1_packs(digest: str, name: Optional[str] = None, request: Request = None):
    p = blob_path(digest)
    if not p.exists():
        COUNTERS["misses"] += 1
        raise HTTPException(status_code=404, detail="digest not found")
    COUNTERS["hits"] += 1
    file_size = p.stat().st_size
    rng = request.headers.get("range")
    start = 0
    end = file_size - 1
    status_code = 200
    headers = {"Accept-Ranges": "bytes"}
    if rng:
        try:
            units, range_spec = rng.split("=")
            start_s, end_s = range_spec.split("-")
            if start_s: start = int(start_s)
            if end_s: end = int(end_s)
            status_code = 206
            headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"
        except Exception:
            pass
    async def iterator():
        nonlocal start, end
        async with aiofiles.open(p, "rb") as f:
            await f.seek(start)
            remain = end - start + 1
            chunk = 1024*256
            while remain > 0:
                data = await f.read(min(chunk, remain))
                if not data: break
                remain -= len(data)
                yield data
    headers["Content-Length"] = str(end - start + 1)
    COUNTERS["bytes_served"] += end - start + 1
    return StreamingResponse(iterator(), status_code=status_code, headers=headers, media_type="application/octet-stream")

@app.get("/v1/proxy")
async def v1_proxy(url: str, sha256: Optional[str]=None, name: Optional[str]=None):
    if name:
        rec = load_name(name)
        if rec and (sha256 is None or rec.get("sha256")==sha256):
            return await v1_packs(rec["sha256"])
    if sha256:
        p = blob_path(sha256)
        if p.exists():
            return await v1_packs(sha256, name=name)
    digest = fetch_and_cache(url, sha256, name)
    return await v1_packs(digest, name=name)

@app.post("/v1/prefetch")
async def v1_prefetch(body: dict = Body(...)):
    items = body.get("items", [])
    done = []
    for it in items:
        url = it.get("url")
        sha = it.get("sha256")
        name = it.get("name")
        if not url: continue
        try:
            digest = fetch_and_cache(url, sha, name)
            done.append({"name": name, "sha256": digest, "ok": True})
        except Exception as e:
            done.append({"name": name, "error": str(e), "ok": False})
    return {"prefetched": done}

@app.get("/v1/metrics")
async def v1_metrics():
    return COUNTERS

@app.post("/v1/ingest_local")
async def v1_ingest_local(file: UploadFile = File(...), sha256: Optional[str] = None, name: Optional[str] = None):
    tmpdir = pathlib.Path(STORAGE) / "tmp"
    tmpdir.mkdir(parents=True, exist_ok=True)
    tmp = tmpdir / f"upload-{int(time.time())}-{os.getpid()}"
    async with aiofiles.open(tmp, "wb") as w:
        while True:
            chunk = await file.read(1024*1024)
            if not chunk: break
            await w.write(chunk)
    digest = store_blob_from_file(tmp, sha256, name)
    try: tmp.unlink()
    except Exception: pass
    COUNTERS["ingest"] += 1
    return {"sha256": digest, "name": name}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    global CFG, STORAGE
    CFG = yaml.safe_load(open(args.config).read())
    STORAGE = CFG.get("storage_root", "./_ophicache_storage")
    import uvicorn
    uvicorn.run("ophicache_server:app",
                host=CFG.get("listen_host","0.0.0.0"),
                port=int(CFG.get("listen_port",7060)),
                reload=False)

if __name__ == "__main__":
    main()
