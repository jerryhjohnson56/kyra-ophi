
#!/usr/bin/env python3
import re, sys

def clean(s: str) -> str:
    s = re.sub(r'(?m)^\s*[`~\'´ˋˊ]{3,}.*\n','', s)
    s = re.sub(r'(?m)\n\s*[`~\'´ˋˊ]{3,}\s*$','', s)
    return s

if __name__ == "__main__":
    data = sys.stdin.read()
    print(clean(data), end="")
