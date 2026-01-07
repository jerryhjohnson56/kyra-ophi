#!/usr/bin/env python3
import argparse, os, subprocess, sys, time, json
from pathlib import Path

REPO = Path(os.environ.get("KYRA_REPO_ROOT", os.getcwd()))
(REPO/"logs").mkdir(exist_ok=True, parents=True)

def run(cmd):
    print("+", " ".join(cmd), flush=True)
    return subprocess.run(cmd, text=True, capture_output=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="pool_config.yaml")
    ap.add_argument("--once", action="store_true")
    args = ap.parse_args()

    # preflight
    pf = run(["python3","scripts/auto_fixers.py"])
    print(pf.stdout, end="")

    proc = run(["python3","scripts/pool_worker.py","--config",args.config] + (["--once"] if args.once else []))

    tel = REPO/"telemetry"; tel.mkdir(parents=True, exist_ok=True)
    with (tel/"telemetry.jsonl").open("a") as f:
        rec = {"ts": int(time.time()), "rc": proc.returncode, "stdout": proc.stdout[-8000:], "stderr": proc.stderr[-8000:]}
        f.write(json.dumps(rec)+"\n")

    print(proc.stdout, end="")
    print(proc.stderr, end="", file=sys.stderr)

if __name__=="__main__":
    main()
