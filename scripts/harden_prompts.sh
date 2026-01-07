#!/usr/bin/env bash
set -euo pipefail
file="prompts/implement_stub_prompt.txt"
if [[ -f "$file" ]]; then
  echo -e "\nDO NOT output code fences (no ``` or ~~~). Return the raw file content only.\n" >> "$file"
  echo "Patched $file"
else
  echo "No $file found (skipped)."
fi
