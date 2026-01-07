
# Final Product Readiness (GO/NO-GO) — Kyra System

This gate declares the product *ship-ready*: language (Kyra), VM/bytecode/JIT, KyraLift, Persona/Render IO, tools, CI/CD, packaging.

Run the gate locally or in CI. If **every** check is PASS -> **GO**. Any FAIL -> **NO-GO**.

## One-liner
```bash
python3 scripts/final_readiness_gate.py --config config/final_gate.yaml --print-report
```

## What is checked (defaults in `config/final_gate.yaml`)
1. **Backlog completion**
   - `manifest.json` exists
   - All items have a code path
   - No stub leftovers (`.bak`, code fences) 
2. **Build & tests (multi-language)**
   - Python: pyflakes clean, pytest green
   - Rust: `cargo check` (optionally `cargo test`)
   - C: `make` for each C stub dir
   - TS: configurable check (default: node smoke; you can switch to `tsc`)
3. **VM/JIT/Bytecode invariants**
   - Bytecode assembler/disassembler round-trip (script-defined)
   - VM self-tests green
   - JIT smoke microbench meets thresholds
4. **KyraLift conversion**
   - N sample repos compile to Kyra IR without errors
5. **Persona/Render IO**
   - Face input + renderer smoke tests green
6. **Packaging & SBOM**
   - Release artifacts present
   - SBOMs found and signed
7. **Docs & Demos**
   - Required guides exist (Language Spec, VM, Bytecode, JIT, KyraLift, Persona, Install)
   - Demos compile & run smoke

Tune thresholds/paths in `config/final_gate.yaml` as your repo evolves.
