#!/usr/bin/env bash
set -euo pipefail
REPO="${KYRA_REPO_ROOT:-$PWD}"
cd "$REPO"
if [[ -f .kyra_pool.pid ]]; then
  PID="$(cat .kyra_pool.pid || echo "")"
  if [[ -n "$PID" ]] && ps -p "$PID" >/dev/null 2>&1; then
    kill "$PID" || true
    echo "Stopped pool loop PID $PID"
  fi
  rm -f .kyra_pool.pid
else
  echo "No PID file found; nothing to stop."
fi
