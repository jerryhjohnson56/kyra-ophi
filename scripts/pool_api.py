#!/usr/bin/env python3
import argparse, json, os, subprocess, sys, pathlib, time, csv

REPO = os.environ.get("KYRA_REPO_ROOT", os.getcwd())
LOGS = pathlib.Path(REPO)/"logs"
LOGS.mkdir(parents=True, exist_ok=True)
TELE = pathlib.Path(REPO)/"telemetry"
TELE.mkdir(parents=True, exist_ok=True)
STATE = TELE/"state.json"

def run(cmd, cwd=REPO, check=True):
    return subprocess.run(cmd, cwd=cwd, check=check, text=True, capture_output=True)

def write_state(d):
    STATE.write_text(json.dumps(d, indent=2))

def read_state():
    if STATE.exists(): return json.loads(STATE.read_text())
    return {"started": int(time.time()), "last": None}

def _queue_preview():
    out = {"total": 0, "by_lang": {}, "items": []}
    m = pathlib.Path(REPO)/"manifest.json"
    if m.exists():
        try:
            data = json.loads(m.read_text())
            items = data.get("items") or data
            out["total"] = len(items)
            for it in items[:30]:
                lang = (it.get("language") or "unknown").lower()
                out["by_lang"][lang] = out["by_lang"].get(lang, 0) + 1
                out["items"].append({"id": it.get("id"), "title": it.get("title"), "lang": lang, "status": it.get("status","queued")})
            return out
        except Exception:
            pass
    csvp = pathlib.Path(REPO)/"KyraOphi_AllSources_Combined_v44.csv"
    if csvp.exists():
        try:
            with csvp.open() as f:
                rdr = csv.DictReader(f)
                for i,row in enumerate(rdr):
                    lang = (row.get("Language") or "unknown").lower()
                    out["by_lang"][lang] = out["by_lang"].get(lang, 0) + 1
                    if i < 30:
                        out["items"].append({"id": row.get("ID") or row.get("Id"), "title": row.get("Title"), "lang": lang, "status":"queued"})
                    out["total"] += 1
        except Exception:
            pass
    if out["total"] == 0:
        for d in (pathlib.Path(REPO)/"stubs"/"items").glob("*"):
            if d.is_dir():
                out["total"] += 1
        out["by_lang"] = {}
    return out

def status():
    s = read_state()
    pid = None
    pidfile = pathlib.Path(REPO)/".kyra_pool.pid"
    if pidfile.exists():
        try:
            pid = int(pidfile.read_text().strip())
            os.kill(pid, 0)
            s["loop_running"] = True
            s["pid"] = pid
        except Exception:
            s["loop_running"] = False
            s["pid"] = None
    else:
        s["loop_running"] = False
        s["pid"] = None

    claim = None
    claim_files = sorted((pathlib.Path(REPO)/"stubs"/"items").glob("*/CLAIM.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if claim_files:
        try:
            claim = json.loads(claim_files[0].read_text())
        except Exception:
            pass
    s["active_claim"] = claim

    try:
        pr = run(["gh","pr","list","--state","open","--json","number,title,headRefName,webUrl"], check=False)
        s["prs"] = json.loads(pr.stdout) if pr.returncode==0 and pr.stdout else []
    except Exception:
        s["prs"] = []

    s["queue"] = _queue_preview()
    return s

def run_once():
    out = run(["python3","scripts/pool_worker_wrapper.py","--config","pool_config.yaml","--once"], check=False)
    rec = {"ts": int(time.time()), "cmd":"once", "rc": out.returncode, "stdout": out.stdout[-8000:], "stderr": out.stderr[-8000:]}
    (TELE/"telemetry.jsonl").open("a").write(json.dumps(rec)+"\n")
    write_state({"last": rec, **read_state()})
    return rec

def start_loop():
    sh = run(["bash","scripts/start_pool.sh"], check=False)
    return {"rc": sh.returncode, "out": sh.stdout+sh.stderr}

def stop_loop():
    sh = run(["bash","scripts/stop_pool.sh"], check=False)
    return {"rc": sh.returncode, "out": sh.stdout+sh.stderr}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fn", choices=["status","once","start","stop"])
    args = ap.parse_args()
    if args.fn=="status": print(json.dumps(status(), indent=2))
    elif args.fn=="once":  print(json.dumps(run_once(), indent=2))
    elif args.fn=="start": print(json.dumps(start_loop(), indent=2))
    elif args.fn=="stop":  print(json.dumps(stop_loop(), indent=2))

if __name__=="__main__":
    main()
