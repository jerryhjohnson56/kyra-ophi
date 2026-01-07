
#!/usr/bin/env python3
import sys
from pathlib import Path

def ensure_rust(dir: Path):
    (dir/"Cargo.toml").write_text("[package]\nname=\"stub\"\nversion=\"0.1.0\"\nedition=\"2021\"\n\n[dependencies]\nserde = { version = \"1.0\", features=[\"derive\"] }\nserde_json = \"1.0\"\n", encoding="utf-8")
    (dir/"src").mkdir(parents=True, exist_ok=True)
    (dir/"src/lib.rs").write_text("use serde_json::{Value, json};\npub fn run(input: &Value) -> Value { input.clone() }\n", encoding="utf-8")

def ensure_c(dir: Path):
    (dir/"src").mkdir(parents=True, exist_ok=True)
    (dir/"src/main.c").write_text("#include <stdio.h>\nint main(void){ printf(\"{\\\"ok\\\":true}\\n\"); return 0; }\n", encoding="utf-8")
    (dir/"Makefile").write_text("all:\n\tcc -O2 -o bin/main src/main.c\n", encoding="utf-8")

def ensure_ts(dir: Path):
    (dir/"stub.ts").write_text("export type Input = Record<string, unknown>;\nexport type Output = Record<string, unknown>;\nexport function run(input: Input): Output { return { ok: true, echo: input }; }\n", encoding="utf-8")

def ensure_py(dir: Path):
    (dir/"stub.py").write_text("from typing import Any, Dict\n\ndef run(input: Dict[str, Any]) -> Dict[str, Any]:\n    return {\"ok\": True, \"echo\": input}\n", encoding="utf-8")

if __name__ == "__main__":
    d = Path(sys.argv[1])
    lang = sys.argv[2]
    d.mkdir(parents=True, exist_ok=True)
    if lang == "rust": ensure_rust(d)
    elif lang == "c": ensure_c(d)
    elif lang == "typescript": ensure_ts(d)
    else: ensure_py(d)
