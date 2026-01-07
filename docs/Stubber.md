# Kyra Gap Stubber

Generate a language-correct stub + minimal tests for a new gap item (ID).

## Usage
```bash
python3 scripts/stub_from_gap.py --csv kyra_master_backlog_merged.csv --id K1001 --root .
```

## Notes
- Language is taken from the backlog row (`Language` column). Override with `--lang-override`.
- Output path uses the row `Path`; if missing, it falls back to `stubs/gaps/<ID>-<slug>`.
- Templates included: Python, TypeScript (Node test), Rust (cargo), C.
```
