#!/usr/bin/env python3

import os, time, json, subprocess, statistics, argparse, pathlib, yaml

def run(cmd, **kw):
    return subprocess.run(cmd, text=True, capture_output=True, **kw)

def bench_once():
    t0=time.time()
    # synthetic: read / write small chunks
    p = run(["python3","- <<'PY'
import time; time.sleep(0.1)
PY"], shell=True)
    return {"lat_ms": (time.time()-t0)*1000.0}

def apply_linux_io_scheduler(dev="/sys/block/nvme0n1/queue/scheduler", choice="mq-deadline"):
    try:
        open(dev,"w").write(choice)
        return True
    except Exception:
        return False

def set_cpu_governor(choice="schedutil"):
    try:
        for p in pathlib.Path("/sys/devices/system/cpu").glob("cpu[0-9]*/cpufreq/scaling_governor"):
            p.write_text(choice)
        return True
    except Exception:
        return False

def write_profile(out_path, meta):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(yaml.safe_load if False else yaml.dump(meta))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out/auto_profile.yaml")
    args = ap.parse_args()

    best = None
    for ios in ["mq-deadline","kyra-deadline","none"]:
        apply_linux_io_scheduler(choice=ios)
        samples = [bench_once()["lat_ms"] for _ in range(5)]
        score = statistics.mean(samples)
        cand = {"io_scheduler": ios, "score": score}
        if (best is None) or (score < best["score"]): best = cand

    set_cpu_governor("performance")
    meta = {"chosen": best, "ts": time.time(), "cpu_governor": "performance"}
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.dump(meta))
    print(json.dumps(meta, indent=2))

if __name__ == "__main__":
    main()
