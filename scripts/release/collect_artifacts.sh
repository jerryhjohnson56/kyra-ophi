#!/usr/bin/env bash
set -euo pipefail

# Collects built installers from Tauri output into ./dist and writes SHA256SUMS.
# Usage: scripts/release/collect_artifacts.sh app/kyra-control

APP_DIR="${1:-app/kyra-control}"
OUT="${2:-dist}"

mkdir -p "$OUT"
BUNDLE="$APP_DIR/src-tauri/target/release/bundle"
if [[ ! -d "$BUNDLE" ]]; then
  echo "No bundle dir at $BUNDLE" >&2
  exit 1
fi

shopt -s globstar nullglob
# common tauri outputs
files=( "$BUNDLE"/**/*.dmg "$BUNDLE"/**/*.app.tar.gz "$BUNDLE"/**/*.msi "$BUNDLE"/**/*.exe "$BUNDLE"/**/*.AppImage "$BUNDLE"/**/*.deb)
for f in "${files[@]}"; do
  [[ -f "$f" ]] || continue
  cp -v "$f" "$OUT/"
done

( cd "$OUT" && shasum -a 256 * > SHA256SUMS || sha256sum * > SHA256SUMS )
echo "Wrote $OUT/SHA256SUMS"
