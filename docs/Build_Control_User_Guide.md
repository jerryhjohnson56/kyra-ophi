# Build Control — User Guide (Short)

## Tabs
- **Dashboard**: queue size, claimed item, active step, PR URL (if any).
- **Queue**: all items left, language, branch name, claimed owner.
- **Logs**: tail of the worker command; errors highlighted.
- **Config**: edit and save `pool_config.yaml`.
- **PRs**: quick list of open PRs created by the worker.

## Controls
- **Run once**: executes a single claim→implement→test→PR cycle.
- **Start loop**: launches `bash scripts/pool_loop.sh` with a managed PID.
- **Stop loop**: kills the managed PID (safe; PRs are already pushed).

## Where it looks for things
- Repo root: from `.env` → `KYRA_REPO_ROOT=/Users/you/code/kyra-ophi`.
- Worker: `scripts/pool_worker.py`, `scripts/claim_item.py`.
- Telemetry: `telemetry/telemetry.jsonl` (auto-created).

## Troubleshooting
- If Start/Stop buttons look disabled, check `.env` paths.
- If GH CLI prompts, login: `gh auth login` and set `GH_TOKEN` if needed.
- If logs show code fences in Rust, enable the *Fence Stripper* toggle in Config.
