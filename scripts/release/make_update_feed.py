#!/usr/bin/env python3
import os, json, sys, re
from pathlib import Path

# Generates a minimal update JSON:
# {
#   "version":"vX.Y.Z",
#   "notes":"...",
#   "assets":[{"name":"...", "url":"...", "sha256":"..."}]
# }
# Provide GH_OWNER and GH_REPO (env) or pass base_url.
#
# Usage:
#   scripts/release/make_update_feed.py <version> <dist_dir> [base_url]
#   base_url default: https://github.com/{owner}/{repo}/releases/download/{version}

def main():
    if len(sys.argv) < 3:
        print("usage: make_update_feed.py <version-tag> <dist-dir> [base_url]", file=sys.stderr)
        sys.exit(2)

    version = sys.argv[1]  # e.g. v0.1.0
    dist = Path(sys.argv[2])
    base_url = sys.argv[3] if len(sys.argv) > 3 else None
    owner = os.environ.get("GH_OWNER"); repo = os.environ.get("GH_REPO")

    if not base_url:
        if not (owner and repo):
            print("Set GH_OWNER and GH_REPO or pass base_url", file=sys.stderr); sys.exit(2)
        base_url = f"https://github.com/{owner}/{repo}/releases/download/{version}"

    sums = {}
    sums_file = dist/"SHA256SUMS"
    if sums_file.exists():
        for line in sums_file.read_text().splitlines():
            parts = re.split(r"\s+", line.strip())
            if len(parts) >= 2:
                digest, name = parts[0], parts[-1]
                # Busybox shasum vs sha256sum format handling
                name = name.replace("*","").replace("./","")
                sums[name] = digest

    assets = []
    for p in dist.iterdir():
        if p.is_file() and p.name != "SHA256SUMS":
            assets.append({"name": p.name, "url": f"{base_url}/{p.name}", "sha256": sums.get(p.name)})

    feed = {"version": version, "notes": "", "assets": assets}
    print(json.dumps(feed, indent=2))

if __name__ == "__main__":
    main()
