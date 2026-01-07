#!/usr/bin/env bash
set -euo pipefail
REPO="${KYRA_REPO_ROOT:-$PWD}"
cd "$REPO"
mkdir -p logs
if [[ -f .kyra_pool.pid ]] && ps -p "$(cat .kyra_pool.pid)" >/dev/null 2>&1; then
  echo "Pool already running with PID $(cat .kyra_pool.pid)"; exit 0
fi
( python3 scripts/pool_worker_wrapper.py --config pool_config.yaml > logs/pool_loop.out 2>&1 ) &
echo $! > .kyra_pool.pid
echo "Started pool loop PID $(cat .kyra_pool.pid)"
