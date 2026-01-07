#!/usr/bin/env bash
set -euo pipefail
CACHE_URL=${1:?cache url}
LIST=${2:?prefetch yaml}
JSON=$(python3 - <<'PY' "$LIST"
import sys, yaml, json
print(json.dumps(yaml.safe_load(open(sys.argv[1]).read())))
PY
"$LIST")
curl -fsSL -X POST -H 'Content-Type: application/json' \
    --data-raw "$JSON" \
    "$CACHE_URL/v1/prefetch"
