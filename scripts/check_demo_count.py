"""Check demo count consistency between root README and examples/README."""
import re
import sys

def extract_count(path, pattern):
    text = open(path, encoding="utf-8").read()
    m = re.search(pattern, text)
    if not m:
        sys.exit(f"ERROR: demo count not found in {path}")
    return int(m.group(1))

root_en = extract_count("README.md",          r"all (\d+)\+? demos")
root_jp = extract_count("README_JP.md",       r"全(\d+)(?:本以上|デモ)")
ex_en   = extract_count("examples/README.md", r"(\d+)\+?\s+[Dd]emos")
ex_jp   = extract_count("examples/README_JP.md", r"全(\d+)(?:本以上|デモ)")

counts = {"README.md": root_en, "README_JP.md": root_jp,
          "examples/README.md": ex_en, "examples/README_JP.md": ex_jp}

if len(set(counts.values())) != 1:
    for f, n in counts.items():
        print(f"  {f}: {n}")
    sys.exit("FAIL demo counts do not match")

print(f"OK  demo count = {root_en} (all 4 READMEs agree)")
