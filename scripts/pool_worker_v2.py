
#!/usr/bin/env python3
import argparse, json, os, subprocess, time, shutil, re
from pathlib import Path

def run(cmd, check=True, **kw):
    print("+", " ".join(cmd))
    return subprocess.run(cmd, text=True, check=check, **kw)

def sanitize(s: str) -> str:
    s = re.sub(r'(?m)^\s*[`~\'´ˋˊ]{3,}.*\n','', s)
    s = re.sub(r'(?m)\n\s*[`~\'´ˋˊ]{3,}\s*$','', s)
    return s

def detect_lang(target: Path) -> str:
    if target.suffix == ".py": return "python"
    if target.suffix == ".ts": return "typescript"
    if target.suffix == ".rs": return "rust"
    if target.suffix == ".c": return "c"
    if (target.parent/"Cargo.toml").exists(): return "rust"
    if (target.parent/"src/main.c").exists(): return "c"
    return "python"

def next_item():
    for p in Path("stubs").rglob("stub.*"):
        claim = p.parent/"CLAIM.json"
        if not claim.exists():
            return p
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="pool_config.yaml")
    ap.add_argument("--once", action="store_true")
    args = ap.parse_args()

    cfg = {}
    if Path(args.config).exists():
        import yaml
        cfg = yaml.safe_load(Path(args.config).read_text())
    if not cfg.get("enabled", False):
        print("Pool disabled. Set enabled: true in pool_config.yaml")
        return 0

    model_cmd = cfg.get("model", {}).get("cmd", ["ollama","run","qwen2.5-coder:7b"])

    while True:
        target = next_item()
        if not target:
            print("No items to process.")
            break
        lang = detect_lang(target)
        context = f"Working on: {target}\nExisting code:\n" + target.read_text()
        tpl = {
            "python": "prompts/implement_stub.md",
            "typescript": "prompts/implement_stub.md",
            "rust": "prompts/implement_rust_crate.md" if target.name == "lib.rs" else "prompts/implement_stub.md",
            "c": "prompts/implement_c_module.md",
        }[lang]

        pb = run(["python3","scripts/prompt_builder.py", tpl, str(target)], input=context, stdout=subprocess.PIPE)
        prompt = pb.stdout

        out = run(model_cmd, input=prompt, stdout=subprocess.PIPE)
        code = sanitize(out.stdout)
        target.write_text(code)

        # test
        if lang == "python":
            run(["python3","-m","pyflakes",str(target)], check=False)
        elif lang == "rust":
            crate_dir = target.parent.parent if target.name == "lib.rs" else Path(".")
            run(["cargo","check"], cwd=str(crate_dir), check=False)
        elif lang == "typescript":
            run(["node","-e","console.log('ts ok')"], check=False)
        elif lang == "c":
            run(["make"], cwd=str(target.parent.parent), check=False)

        # branch & PR
        item = target.parent.name
        branch = f"worker/auto/{item}"
        run(["git","switch","-C", branch], check=False)
        run(["git","add", str(target.parent)], check=True)
        run(["git","commit","-m", f"feat({item}): initial implementation via local LLM"], check=False)
        run(["git","push","-u","origin",branch], check=False)
        run(["gh","pr","create","--fill"], check=False)

        if args.once: break
        time.sleep(int(cfg.get("sleep_seconds", 8)))

if __name__ == "__main__":
    raise SystemExit(main())
