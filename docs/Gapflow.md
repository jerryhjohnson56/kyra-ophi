# Kyra GapFlow

**Goal:** if local models discover a missing piece, the system opens an issue, appends to the backlog, and keeps coding until green.

## How it works
1) CI runs `gapflow_scan.py` after tests.
2) Failures -> labeled GitHub Issues + new backlog rows (IDs like K1000).
3) Workers pick up new items and implement them (failing test first).

## Setup
- Commit this kit to your repo root and push.
- Ensure `kyra_master_backlog_merged.csv` exists (or adjust `configs/gapflow.yaml`).
- No extra secrets required (uses `GITHUB_TOKEN`).

## Local dry run
```bash
python3 scripts/gapflow_scan.py --config configs/gapflow.yaml
```
