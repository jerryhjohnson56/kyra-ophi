# Signing Guide (macOS, Windows, Linux)

## macOS (Developer ID + Notarization)
**Requires:** Apple Developer account, Developer ID Application cert

Two auth paths:
1) **App-Specific Password**  
   - Secrets: `APPLE_ID` (email), `APPLE_APP_PASS` (app-specific pw), `APPLE_TEAM_ID`.
2) **App Store Connect API Key**  
   - Secrets: `APPLE_API_KEY_BASE64` (base64 of .p8), `APPLE_API_KEY` (key id), `APPLE_API_ISSUER` (issuer id), `APPLE_TEAM_ID`.

The CI will:
- sign with Developer ID
- run `xcrun notarytool submit`
- staple the ticket

## Windows (Authenticode)
- Obtain a code signing certificate (.pfx).
- Create secrets:
  - `WIN_CERT_PFX_BASE64` – base64 of the PFX file
  - `WIN_CERT_PASSWORD` – password for the PFX

CI imports the cert and runs `signtool` on the built installer/binaries.

## Linux (GPG)
- Generate a GPG key for releases.
- Export private key (ASCII armored) → secret `LINUX_GPG_PRIVATE_KEY`
- Passphrase → secret `LINUX_GPG_PASSPHRASE`

CI will sign `.AppImage` or repo packages with `gpg --batch --yes --pinentry-mode loopback`.
