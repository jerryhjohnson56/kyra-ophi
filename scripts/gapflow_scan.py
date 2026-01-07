#!/usr/bin/env python3
import os, sys, re, json, subprocess, csv, argparse, requests, yaml

def run(cmd, **kw):
    print("+", " ".join(cmd))
    return subprocess.run(cmd, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kw).stdout

def gh_post(url, token, payload):
    r = requests.post(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }, json=payload, timeout=30)
    if r.status_code >= 300:
        print("GH POST error", r.status_code, r.text, file=sys.stderr)
    return r.json()

def create_issue(repo, token, title, body, labels):
    url = f"https://api.github.com/repos/{repo}/issues"
    return gh_post(url, token, {"title": title, "body": body, "labels": labels})

def append_backlog(csv_path, row):
    headers = ["ID","Title","Area","Priority","Language","Path","FileType","Owner","Tags","Description","PlanToConvertToKyra","OrderHint"]
    exists = os.path.exists(csv_path)
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        if not exists:
            w.writeheader()
        w.writerow({k: row.get(k,"") for k in headers})

def next_gap_id(existing_ids, prefix):
    n = 1000
    while True:
        cand = f"{prefix}{n}"
        if cand not in existing_ids:
            return cand
        n += 1

def load_existing_ids(csv_path):
    ids = set()
    if not os.path.exists(csv_path):
        return ids
    with open(csv_path, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            rid = (row.get("ID") or "").strip()
            if rid:
                ids.add(rid)
    return ids

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/gapflow.yaml")
    args = ap.parse_args()

    with open(args.config, "r", encoding="utf-8") as cf:
        cfg = yaml.safe_load(cf)

    repo = os.environ.get("REPO")
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not (repo and token):
        print("GapFlow: Missing REPO or GH_TOKEN env; skipping.", file=sys.stderr)
        sys.exit(0)

    # 1) run pytest baseline
    out = run(["pytest","-q"])
    print(out)

    failures = []
    for line in out.splitlines():
        if re.search(r"^E\s+.+", line) or re.search(r"^FAILED\s+", line):
            failures.append(line)

    if not failures:
        print("GapFlow: no test failures detected.")
        return

    existing_ids = load_existing_ids(cfg.get("backlog_csv","kyra_master_backlog_merged.csv"))
    created = 0

    for i, line in enumerate(failures[:10]):
        kind = "api" if ("KeyError" in line or "TypeError" in line) else "feature"
        labels = cfg["labels"].get(kind, ["triage:needed"])
        gap_id = next_gap_id(existing_ids, cfg.get("gap_id_prefix","K"))
        existing_ids.add(gap_id)

        title = f"{gap_id}: Auto-detected {kind} gap from tests"
        body = (
            "Auto-detected {kind} gap.\n\n"
            "**Signal:** `{line}`\n\n"
            "**Proposed next steps**\n"
            "- Reproduce locally with `pytest -q`\n"
            "- Create failing test (if not already present)\n"
            "- Implement minimal fix\n"
            "- Link PR to this issue\n"
        ).format(kind=kind, line=line)

        create_issue(repo, token, title, body, labels)

        row = {
            "ID": gap_id,
            "Title": f"{kind.title()} gap fix – {gap_id}",
            "Area": "gapflow",
            "Priority": cfg.get("priority_default","P2"),
            "Language": cfg.get("language_default","python"),
            "Path": f"{cfg.get('stub_root','stubs/gaps')}/{gap_id}",
            "FileType": "mixed",
            "Owner": cfg.get("owner_default","pool"),
            "Tags": ",".join(labels),
            "Description": f"Auto-added from test failure: {line}",
            "PlanToConvertToKyra": "Kyra bytecode target after MVP fix",
            "OrderHint": str(8000 + i)
        }
        append_backlog(cfg.get("backlog_csv","kyra_master_backlog_merged.csv"), row)
        created += 1

    print(f"GapFlow: created {created} issues and appended to backlog.")

if __name__ == "__main__":
    main()
