#!/usr/bin/env python3
import sys, csv, re, argparse
from pathlib import Path
from collections import OrderedDict

def load_csv(path):
  with open(path, newline='', encoding='utf-8') as f:
    return list(csv.DictReader(f))

def normalize_id(row):
  rid = (row.get("ID") or row.get("Id") or row.get("id") or "").strip()
  if rid: return rid
  p = row.get("Path","")
  m = re.search(r'([SEK]\d{3,4})', p)
  return m.group(1) if m else ""

def is_backlog_row(row):
  rid = (row.get("ID") or row.get("Id") or row.get("id") or "").strip()
  title = (row.get("Title") or "").strip()
  area = (row.get("Area") or "").strip()
  path = (row.get("Path") or "").strip()
  ok_id = bool(re.match(r'^[SEK]\d{3,4}$', rid))
  ok_shape = bool(area and title and path)
  return ok_id or ok_shape

def main():
  ap = argparse.ArgumentParser(description="Merge multiple Kyra backlog CSVs into one master")
  ap.add_argument("--out", required=True, help="Output CSV path")
  ap.add_argument("inputs", nargs="+", help="Input CSV paths")
  args = ap.parse_args()

  headers = OrderedDict()
  rows = OrderedDict()
  for inp in args.inputs:
    for r in load_csv(inp):
      if not is_backlog_row(r): 
        continue
      rid = normalize_id(r)
      if not rid:
        continue
      for h in r.keys(): headers[h] = True
      if rid not in rows: rows[rid] = r
      else:
        for k,v in r.items():
          if k not in rows[rid] or not rows[rid][k]:
            rows[rid][k] = v

  for c in ["ID","Title","Area","Priority","Language","Path","FileType","Owner","Tags","Description","PlanToConvertToKyra","OrderHint"]:
    headers[c] = True

  with open(args.out, "w", newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(headers.keys()))
    w.writeheader()
    for r in rows.values():
      w.writerow({k: r.get(k,"") for k in headers.keys()})

  print(f"Merged {len(rows)} items into {args.out}")

if __name__ == "__main__":
  main()
