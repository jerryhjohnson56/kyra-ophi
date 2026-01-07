#!/usr/bin/env bash
set -euo pipefail
REPO="${KYRA_REPO_ROOT:-$PWD}"
cd "$REPO"
python3 scripts/pool_worker_wrapper.py --config pool_config.yaml --once
