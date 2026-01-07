#!/usr/bin/env bash
set -euo pipefail
SRC=${1:-./_ophicache_storage}
DST=${2:-/mnt/usb/kpack_shelf}
mkdir -p "$DST"/{blobs/sha256,names}
rsync -a --info=progress2 "$SRC/blobs/sha256/" "$DST/blobs/sha256/" || true
rsync -a "$SRC/names/" "$DST/names/" || true
echo "[export] shelf exported to $DST"
