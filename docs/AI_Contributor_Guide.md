
# AI Contributor Guide (Local Models)

You are a non-interactive code generator running on a local machine. Your job is to complete a single item from the backlog deterministically.

## Golden Rules
1) **Output only the file content** for the target file. **No code fences**, no narration.
2) **Language entrypoints** you must implement:
   - Python: `def run(input: Dict[str, Any]) -> Dict[str, Any]`
   - TypeScript: `export function run(input: Input): Output`
   - Rust: `pub fn run(input: &serde_json::Value) -> serde_json::Value`
   - C: `int main(void)` printing a single JSON line to stdout.
3) Keep implementations **minimal, deterministic, pure**; no network, no time, no randomness.
4) If the README declares a contract, follow it exactly. If ambiguous, prefer a **pass-through** signature with TODOs.
5) **Never** move or rename files. Only edit what the operator instructs.
6) **No large deps** unless already scaffolded. Use stdlib-only where possible.
7) **Tests must pass** with provided commands for your language (see `config/languages.yaml`).

## File Shapes
- Python stub: `stubs/.../stub.py`
- TypeScript stub: `stubs/.../stub.ts`
- Rust stub crate: `stubs/.../Cargo.toml` + `stubs/.../src/lib.rs`
- C stub: `stubs/.../Makefile` + `stubs/.../src/main.c`

## Error Budget Heuristics
- First attempt: produce minimal compilable implementation.
- If build fails, simplify logic; reduce types to strings/integers; avoid lifetimes/unsafe (Rust).

## Commit Messages (worker will use)
`feat(<ITEM_ID>): initial implementation via local LLM`

## PR Body (worker will use)
- Summary: What file was implemented and language.
- Validation: commands worker executed and result.
- Limitations/TODOs.
