# Kyra Build Suite — Windows/Linux Build & Signing Add‑on (v1)

This pack adds:
- **Windows & Linux build scripts** for the Tauri desktop app (`app/kyra-control`).
- **Code signing templates** for macOS, Windows, Linux (GPG).
- **GitHub Actions CI** that builds on **macOS, Windows, and Ubuntu**, signs, and uploads artifacts.

> Drop this at the **root of your repo** (same place as `scripts/` and `app/kyra-control/`).

## Quick Start (Local)

### Windows (PowerShell)
```powershell
# prereqs (one-time)
winget install -e --id OpenJS.NodeJS.LTS
winget install -e --id Rustlang.Rust.MSVC
winget install -e --id Python.Python.3.11
# C++ toolchain for WebView2/Tauri
winget install -e --id Microsoft.VisualStudio.2022.BuildTools
npm i -g @tauri-apps/cli

# build
cd app/kyra-control
npm ci
npm run tauri build
```

### Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install -y curl wget git python3-pip libgtk-3-dev libayatana-appindicator3-dev   librsvg2-dev gcc g++ pkg-config libssl-dev libwebkit2gtk-4.1-dev
curl https://sh.rustup.rs -sSf | sh -s -- -y
npm i -g @tauri-apps/cli

cd app/kyra-control
npm ci
npm run tauri build
```

### macOS note
Your app already builds on macOS. This pack focuses on **Windows/Linux** and CI+. See `docs/Signing_Guide.md` for macOS signing/notarization.

## CI (GitHub Actions)
- Adds `.github/workflows/tauri-desktop-build.yml`
- Matrix across `ubuntu-latest`, `windows-latest`, `macos-latest`
- Caches Rust/Node deps
- Signs artifacts when secrets are present
- Uploads final `.dmg` (mac), `.msi/.exe` (win), `.AppImage/.deb` (linux) as artifacts

## Secrets to set (optional but recommended)
- **macOS**: `APPLE_TEAM_ID`, `APPLE_ID`, `APPLE_APP_PASS` *or* `APPLE_API_KEY`, `APPLE_API_ISSUER`, `APPLE_API_KEY_BASE64`
- **Windows**: `WIN_CERT_PFX_BASE64`, `WIN_CERT_PASSWORD`
- **Linux**: `LINUX_GPG_PRIVATE_KEY`, `LINUX_GPG_PASSPHRASE`

See `docs/Signing_Guide.md` for details.
