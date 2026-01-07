# Kyra Hardware Program — v1
Generated: 2026-01-04T08:02:40.441365Z

This kit defines how official Kyra hardware complements the OS and enables a turn‑key,
*fast-by-default* experience. It includes SKU specs, acceptance tests, factory prep,
first-boot provisioning, warranty/RMA templates, and benchmark scripts the local AIs can run.

## Highlights
- Preinstalled Kyra SuperISO (+ signed packs), device-tailored power/cgroup profiles.
- First‑boot persona and creator pipeline calibrated for bundled camera/mics.
- Kyra Base Station option (LAN cache for models/updates/content).
- Hardware attestation for secure updates, LTS channel, one‑tap Recovery.
- Bench suite shipped; results shown in Settings → Performance.

## Directory layout
- `hardware/skus/*.yaml` — authoritative SKU definitions.
- `hardware/packs/*.yaml` — model/content packs that ship on each SKU.
- `hardware/profiles/*.yaml` — Performance profiles (Balanced/Creator Boost/Lite) tuned per SKU.
- `scripts/hw/*.sh` — factory preinstall, first-boot prep, bench runner.
- `docs/*.md` — QA, firmware, provisioning, marketing copy blocks.
- `policy/hw/*.md` — Warranty, RMA, privacy notes.
- `manufacturing/*.md` — QA checklist, packaging, burn-in tests.
- `status/bench_schema.json` — JSON schema for benchmark results.
