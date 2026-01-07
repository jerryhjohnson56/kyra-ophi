#!/usr/bin/env python3
import re, os
from pathlib import Path

REPO = Path(os.environ.get("KYRA_REPO_ROOT", os.getcwd()))
FENCE = re.compile(r'^\s*[`~\'´ˋˊ]{3,}.*$', re.M)

def strip_code_fences(text: str) -> str:
    # remove any triple backtick/tilde/variants lines
    lines = [ln for ln in text.splitlines() if not FENCE.match(ln)]
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")

def fix_serde_use(text: str) -> str:
    # common typo: "se serde_json::Value;"
    return re.sub(r'^\s*se\s+(serde_json::)', r'use \1', text, flags=re.M)

def ensure_cargo_scaffold(root: Path):
    cargo = root/"Cargo.toml"
    src = root/"src"; lib = src/"lib.rs"
    if not cargo.exists():
        name = root.name.replace('-', '_')
        cargo.write_text(f"""[package]
name = "{name}"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = {{ version = "1", features = ["derive"] }}
serde_json = "1"
""")
    if not lib.exists():
        src.mkdir(parents=True, exist_ok=True)
        lib.write_text("use serde_json::Value;\n\npub fn run(_input: &Value) -> Value {\n    serde_json::json!({ \"ok\": true })\n}\n")

def fix_file(p: Path):
    t = p.read_text(errors="ignore")
    orig = t
    if p.suffix == ".rs":
        t = strip_code_fences(t)
        t = fix_serde_use(t)
    elif p.suffix == ".py":
        t = strip_code_fences(t)
    elif p.suffix == ".c":
        t = strip_code_fences(t)
    if t != orig:
        p.write_text(t)

def main():
    fixed = 0
    for p in REPO.glob("stubs/items/*/src/lib.rs"):
        before = p.read_text(errors="ignore")
        fix_file(p)
        after = p.read_text(errors="ignore")
        if before != after: fixed += 1
        ensure_cargo_scaffold(p.parent.parent)
    for p in REPO.glob("stubs/items/*/stub.py"):
        before = p.read_text(errors="ignore")
        fix_file(p)
        if p.read_text(errors="ignore") != before: fixed += 1
    for p in REPO.glob("stubs/items/*/*.c"):
        before = p.read_text(errors="ignore")
        fix_file(p)
        if p.read_text(errors="ignore") != before: fixed += 1
    print(f"files fixed: {fixed}")

if __name__=="__main__":
    main()
