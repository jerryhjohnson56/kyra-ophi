#!/usr/bin/env bash
set -euo pipefail
echo "[kyra-preinstall] preparing image..."
# 1) Copy signed packs & profiles
mkdir -p /opt/kyra/packs /opt/kyra/profiles
cp -r ./packs/* /opt/kyra/packs/ || true
cp -r ./profiles/* /opt/kyra/profiles/ || true
# 2) Seed model cache location (placeholder)
mkdir -p /var/lib/kyra/models
# 3) Create recovery snapshot
echo "[kyra-preinstall] creating recovery snapshot (placeholder)"
