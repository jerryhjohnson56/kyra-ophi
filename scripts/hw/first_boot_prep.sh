#!/usr/bin/env bash
set -euo pipefail
echo "[kyra-firstboot] applying hardware profile..."
PROFILE=${1:-balanced}
install -D -m 0644 "/opt/kyra/profiles/${PROFILE}.yaml" "/etc/kyra/profile.yaml"
echo "[kyra-firstboot] warming caches (light)"
# Placeholders for prefetches; keep short
