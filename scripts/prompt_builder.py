
#!/usr/bin/env python3
from pathlib import Path
import sys

def build(context: str, template_path: str, target_file: str) -> str:
    tpl = Path(template_path).read_text(encoding="utf-8")
    tpl = tpl.replace("{{context}}", context)
    tpl = tpl.replace("{{target_file}}", target_file)
    return tpl

if __name__ == "__main__":
    ctx = sys.stdin.read()
    tpl = sys.argv[1]
    target = sys.argv[2]
    print(build(ctx, tpl, target))
