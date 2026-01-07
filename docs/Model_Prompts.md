
# Model Prompts Overview

The worker assembles prompts from these templates in `prompts/`:
- `implement_stub.md` — default single-file task
- `implement_rust_crate.md` — Rust crate stub (`src/lib.rs` form)
- `implement_c_module.md` — C module stub with JSON stdout
- `write_tests.md` — expand tests when contract is clear
- `fix_build.md` — build error remediation without changing public API
- `refactor_for_performance.md` — after baseline green

All prompts end with: **Do not wrap your answer in code fences. Output only the full target file content.**
