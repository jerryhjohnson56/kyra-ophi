# Release Process

1. **Bump app version** in `app/kyra-control/tauri.conf.json` (and your app code if you display it).
2. Commit, then tag:
   ```bash
   git tag vX.Y.Z -m "Kyra Control vX.Y.Z"
   git push origin vX.Y.Z
   ```
3. Wait for workflows to finish:
   - `desktop-build` (from the earlier pack) or **`release-publish`** in this pack will attach artifacts.
   - `gh-pages-updates` will publish `updates/latest.json` for the auto-updater.
   - `slsa-provenance` will attach provenance.
   - `cosign-sign` will sign installers (optional).
4. Verify:
   - GitHub **Releases** page — assets + checksums + SBOM + attestation.
   - **Pages**: `https://<owner>.github.io/<repo>/updates/latest.json`
5. Distribute the download page linking to your Release or Pages feed.
