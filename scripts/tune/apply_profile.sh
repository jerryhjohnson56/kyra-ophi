#!/usr/bin/env bash
set -euo pipefail
PROFILE=${1:-out/auto_profile.yaml}
echo "[apply-profile] applying $PROFILE"
# TODO: merge into /etc/kyra/thermo/profile.yaml and udev rules
