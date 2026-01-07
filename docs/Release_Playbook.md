
# Release Playbook — Kyra v1.0

## 0) Final Gate
```bash
python3 scripts/final_readiness_gate.py --config config/final_gate.yaml --print-report
# returns exit code 0 and prints ALL PASS
```

## 1) Tag & Build
```bash
git switch main && git pull
git tag -a kyra-v1.0.0 -m "Kyra v1.0.0"
git push origin kyra-v1.0.0
```

## 2) GitHub Actions (final-release-gate.yml)
- Triggers on tag push.
- Runs same gate + packaging + notarization/signing where applicable.

## 3) Publish Artifacts
- Upload build outputs and SBOMs to release assets
- Publish docs site (if applicable) and API specs

## 4) Archive Provenance
- Store signed checksums and SBOMs in `releases/kyra-v1.0.0/`
