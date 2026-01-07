# Kyra Auto‑Tuner (closed-loop)
- Tries a small design space (I/O scheduler, CPU governors, fan curves later).
- Benchmarks micro-latency; selects the best; writes YAML profile.
- Intended to run on first boot and after major updates.

**Outputs:** `out/auto_profile.yaml` (apply via `scripts/tune/apply_profile.sh`)
