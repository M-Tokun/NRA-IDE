"""Check internal links in root README.md and README_JP.md."""
import re
import os
import sys

TARGET_FILES = ["README.md", "README_JP.md"]
LINK_RE = re.compile(r'\[.*?\]\(([^)]+)\)')

errors = []

for readme in TARGET_FILES:
    content = open(readme, encoding="utf-8").read()
    for raw in LINK_RE.findall(content):
        path = raw.split("#")[0].strip()
        if not path or path.startswith("http") or path.startswith("mailto"):
            continue
        path = path.lstrip("./")
        if not os.path.exists(path):
            errors.append(f"{readme}: broken → {path}")

if errors:
    for e in errors:
        print(f"FAIL {e}")
    sys.exit(1)

print(f"OK  internal links ({', '.join(TARGET_FILES)})")
