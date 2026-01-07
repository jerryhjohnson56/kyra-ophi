#!/usr/bin/env bash
set -euo pipefail
SRC=${1:-/mnt/usb/kpack_shelf}
DST=${2:-./_ophicache_storage}
mkdir -p "$DST"/{blobs/sha256,names}
rsync -a --info=progress2 "$SRC/blobs/sha256/" "$DST/blobs/sha256/" || true
rsync -a "$SRC/names/" "$DST/names/" || true
echo "[import] shelf imported from $SRC"
