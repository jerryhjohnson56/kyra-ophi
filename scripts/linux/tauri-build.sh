#!/usr/bin/env bash
set -euo pipefail
cd "${1:-app/kyra-control}"
npm ci
npm run tauri build
