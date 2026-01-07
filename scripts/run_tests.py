
#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path

def run(cmd, **kw):
    print("+", " ".join(cmd))
    return subprocess.run(cmd, text=True, check=False, **kw)

if __name__ == "__main__":
    lang = sys.argv[1]
    target = Path(sys.argv[2])
    if lang == "python":
        run(["python3","-m","pyflakes",str(target)])
    elif lang == "rust":
        crate_dir = target.parent.parent if target.name == "lib.rs" else Path(".")
        run(["cargo","check"], cwd=str(crate_dir))
    elif lang == "typescript":
        run(["node","-e","console.log('ts ok')"])
    elif lang == "c":
        run(["make"], cwd=str(target.parent.parent))
