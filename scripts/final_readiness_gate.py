
#!/usr/bin/env python3
import argparse, json, os, re, subprocess, sys
from pathlib import Path

def run(cmd, cwd=None):
    print("+", " ".join(cmd))
    p = subprocess.run(cmd, cwd=cwd, text=True)
    return p.returncode == 0

def grep_code_fences(root: Path):
    count = 0
    rex = re.compile(r'^\s*(```|~~~)', re.M)
    for p in root.rglob("*"):
        if p.is_file():
            try:
                s = p.read_text(encoding="utf-8", errors="ignore")
                if rex.search(s):
                    count += 1
            except Exception:
                pass
    return count

def require_files(paths):
    missing = [p for p in paths if not Path(p).exists()]
    return missing

def read_json_if_exists(p: Path):
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/final_gate.yaml")
    ap.add_argument("--print-report", action="store_true")
    args = ap.parse_args()

    import yaml
    cfg = yaml.safe_load(Path(args.config).read_text())

    thresholds = cfg["thresholds"]
    paths = cfg["paths"]
    cmds = cfg["commands"]
    perf = cfg.get("perf_files", {})

    report = []
    all_ok = True

    # 1) Backlog & stubs hygiene
    manifest_path = Path(paths["manifest"])
    if not manifest_path.exists():
        report.append(("manifest", False, "manifest.json missing"))
        all_ok = False
    else:
        man = json.loads(manifest_path.read_text(encoding="utf-8"))
        items = man.get("items", [])
        ok_items = len(items) >= thresholds["min_items"]
        report.append(("items_count", ok_items, f"{len(items)} >= {thresholds['min_items']}"))
        all_ok &= ok_items

        have_code = sum(1 for it in items if it.get("code"))
        ok_code = have_code == len(items)
        report.append(("items_have_code", ok_code, f"with code: {have_code}/{len(items)}"))
        all_ok &= ok_code

    stubs_root = Path(paths["stubs_root"])
    bak_count = sum(1 for _ in stubs_root.rglob("*.bak"))
    ok_bak = bak_count <= thresholds["max_bak_files"]
    report.append(("no_bak_files", ok_bak, f".bak files: {bak_count}"))
    all_ok &= ok_bak

    fence_count = grep_code_fences(stubs_root)
    ok_fences = fence_count <= thresholds["max_code_fences"]
    report.append(("no_code_fences", ok_fences, f"files with fences: {fence_count}"))
    all_ok &= ok_fences

    # 2) Builds & tests
    for key in ("python_lint","python_tests","rust_check","c_build","ts_check"):
        ok = run(cmds[key])
        report.append((key, ok, "ok" if ok else "failed"))
        all_ok &= ok

    # 3) VM/JIT/Bytecode health (best-effort)
    for key in ("bytecode_roundtrip","vm_selftest","jit_microbench"):
        ok = run(cmds[key])
        report.append((key, ok, "ok" if ok else "skipped/failed"))
        # not hard failing here

    # 4) KyraLift & Persona
    for key in ("kyralift_smoke","persona_smoke"):
        ok = run(cmds[key])
        report.append((key, ok, "ok" if ok else "skipped/failed"))

    # 5) Packaging & SBOM
    artifacts_dir = Path(paths["artifacts_dir"])
    artifacts_ok = artifacts_dir.exists() and any(artifacts_dir.iterdir())
    report.append(("artifacts_present", artifacts_ok, f"dist exists: {artifacts_ok}"))
    all_ok &= artifacts_ok

    sbom_dir = Path(paths["sbom_dir"])
    sbom_ok = sbom_dir.exists() and any(sbom_dir.iterdir())
    report.append(("sboms_present", sbom_ok, f"sbom exists: {sbom_ok}"))
    # optional

    # 6) Docs required
    missing_docs = require_files(paths.get("docs_required", []))
    docs_ok = len(missing_docs)==0
    report.append(("docs_required", docs_ok, "all found" if docs_ok else f"missing: {', '.join(missing_docs)}"))
    all_ok &= docs_ok

    # 7) Optional perf thresholds if metrics present
    jit_metrics = read_json_if_exists(Path(perf.get("jit_metrics","")))
    if jit_metrics and "startup_ms" in jit_metrics:
        ok = jit_metrics["startup_ms"] <= thresholds["jit_startup_ms_max"]
        report.append(("perf_jit_startup", ok, f"{jit_metrics['startup_ms']} <= {thresholds['jit_startup_ms_max']}"))
        all_ok &= ok

    vm_metrics = read_json_if_exists(Path(perf.get("vm_metrics","")))
    if vm_metrics and "throughput_ops" in vm_metrics:
        ok = vm_metrics["throughput_ops"] >= thresholds["vm_throughput_ops_min"]
        report.append(("perf_vm_throughput", ok, f"{vm_metrics['throughput_ops']} >= {thresholds['vm_throughput_ops_min']}"))
        all_ok &= ok

    if args.print_report:
        width = max(len(k) for k,_,_ in report) + 2
        for k, ok, msg in report:
            print(f"{k.ljust(width)} {'PASS' if ok else 'FAIL'}  {msg}")
        print("\nRESULT:", "ALL PASS — READY TO SHIP" if all_ok else "NO-GO — FIX FAILURES ABOVE")

    return 0 if all_ok else 2

if __name__ == "__main__":
    sys.exit(main())
