
#!/usr/bin/env python3
import subprocess, sys

def run_model(cmd, prompt: str) -> str:
    p = subprocess.run(cmd, input=prompt, text=True, stdout=subprocess.PIPE, check=True)
    return p.stdout

if __name__ == "__main__":
    # echo back for smoke tests
    prompt = sys.stdin.read()
    print(prompt)
