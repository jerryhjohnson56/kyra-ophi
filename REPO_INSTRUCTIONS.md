
# Repository Instructions for Local Models (Drop-in Pack)

Place these folders/files at the root of your fresh repo:
- `docs/`, `prompts/`, `config/`, `scripts/`, `.github/workflows/`

Then:
1) Copy `config/pool_config.template.yaml` to `pool_config.yaml`, set your git identity and model.
2) Run your environment installer (from the Master Bootstrap kit) to install Python/Rust/C toolchains.
3) When ready, set `enabled: true` and run:
   - `python3 scripts/pool_worker_v2.py --config pool_config.yaml --once` (smoke)
   - `python3 scripts/pool_worker_v2.py --config pool_config.yaml` (loop)

The worker enforces: no code fences, correct entrypoints, language-aware build, and PR-per-item.
