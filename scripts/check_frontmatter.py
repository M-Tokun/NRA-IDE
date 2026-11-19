"""Read-only check of the frontmatter rollout (2026-11). Writes nothing.

  python -B scripts/check_frontmatter.py [--citations local_reports/frontmatter_inventory_2026-11-17/h4_citations.json]

Checks
  F1 format   : every tracked .md whose first line is '---' has a closed block, LF only, no BOM,
                keys id/kind/created/title present, id matches the ID Gate pattern, created is a real date.
  F2 unique   : each id is used by exactly one tracked file.
  F3 kind     : kind is one of the agreed vocabulary words.
  F4 body     : for files whose frontmatter was added later, the commit that added it changed nothing
                below the block (body bytes equal to the parent version).
  F5 exempt   : id_gate_baseline.json exempt_paths exist, lack an id, and every gated file without an id is exempt.
  F6 citations: (optional, local file) each shifted line citation points at the same text after the shift.

Exit code 0 = all checks passed, 1 = at least one finding. Findings are printed one per line.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KINDS = {"draft", "review", "report", "note", "essay", "paper", "dialog", "dict", "guide", "exp", "spec", "index"}
REQUIRED = ("id", "kind", "created", "title")
# Reviewed 2026-11-20 with the owner. Kinds used before the rollout vocabulary existed (not rewritten).
LEGACY_KINDS = {
    "dictionary/NRA-IDE数式配置の5大鉄則（式の文法）.md": "dictionary-supplement",
    "note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/NRA_IDE_Quantum_Session_Records_EN.md": "record",
    "note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/NRA_IDE_Quantum_Session_Records_JP.md": "record",
    "note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/変遷記録.md": "record",
    "note/06_対話セッション記録/NRA-IDE_開いた動的構造式と泥臭い応用式の対照精査および正典v2.5整合報告_精査報告_2026-11-16.md": "review-report",
    "note/07_知能爆発-自己再帰的改善/AI_Studio.md": "poc-log",
    "note/07_知能爆発-自己再帰的改善/exploration_review_summary_20261010.md": "review-summary",
    "note/07_知能爆発-自己再帰的改善/gemini_possibility_exploration_assessment_20261010-1913.md": "exploration-record",
    "note/07_知能爆発-自己再帰的改善/仮説は、人工知能論や技術的特異点（シンギュラリティ）の議論において「知能爆発（Intelligence Explosion）」または「自己再帰的改善（Recursive Self-Improvement）」と呼ばれるモデル.md": "dialogue-log",
    "note/07_知能爆発-自己再帰的改善/可能性探索における記録・再検索・更新の方法20261010-1904.md": "method",
    "note/07_知能爆発-自己再帰的改善/理解と束縛の分離_着想20261012.md": "idea",
    "note/07_知能爆発-自己再帰的改善/相関票と多数決の限界_着想20261012.md": "idea",
    "note/07_知能爆発-自己再帰的改善/論点纏め_境界理解と検証構造_20261012.md": "summary",
    "note/07_知能爆発-自己再帰的改善/近接化の形と計算の切替_着想20261011.md": "idea",
    "note/08_セキュリティ/#_Microsoftが確認した事実と、まだ証明されていないこと（AIサイバー攻撃の実態）.md": "article",
    "nra-core/foundations/NRA-IDE_説明用拡張式体系.md": "explanatory-reference",
    "nra-core/foundations/開放系_境界接近比の増分分解_論文草案_精査報告_別観点第二精査（条件付き完了-1）_2026-11-16.md": "review-report",
    "obsidian-index/README.md": "doc",
}
# Reviewed 2026-11-20: commits that added frontmatter together with intended body edits
# (e0505e9 added six dictionary terms; the others are October edits made before the rollout).
ACCEPTED_BODY_CHANGES = {
    "dictionary/NRA-IDE_Dictionary_EN.md": "e0505e9",
    "dictionary/NRA-IDE_Dictionary_JP.md": "e0505e9",
    "note/06_対話セッション記録/AI社会の整備・修理能力と技能継承の断絶.md": "7b1cac1",
    "note/08_セキュリティ/#_Microsoftが確認した事実と、まだ証明されていないこと（AIサイバー攻撃の実態）.md": "1be1cc2",
    "note/AIリテラシー/HF事件/HF事件_今までのAIとは何が変わったのか_別視点_20260913-2114.md": "266f895",
    "note/AIリテラシー/HF事件/報酬ハッキング_1200体AI_HuggingFace事件_20260913-1830.md": "266f895",
}


def git(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True).stdout


def split_block(raw: bytes):
    """Return (fields, body_bytes) or None when the file has no closed frontmatter block."""
    if not raw.startswith(b"---\n"):
        return None
    end = raw.find(b"\n---\n", 3)
    if end < 0:
        return None
    fields = {}
    for line in raw[4:end].decode("utf-8").split("\n"):
        if ":" in line and not line.startswith((" ", "-")):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.split(" #")[0].strip().strip('"')
    body = raw[end + 5:]
    return fields, body[1:] if body.startswith(b"\n") else body


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--citations", type=Path)
    args = ap.parse_args(argv)
    policy = json.loads((ROOT / "id_gate_policy.json").read_text(encoding="utf-8"))
    baseline = json.loads((ROOT / "id_gate_baseline.json").read_text(encoding="utf-8"))
    id_pattern = re.compile(policy["id_pattern"])
    gated = tuple(policy["include_prefixes"])
    findings: list[str] = []
    notes: list[str] = []
    owners: dict[str, list[str]] = {}
    with_fm = 0
    files = [p for p in git("ls-files", "-z", "*.md").decode("utf-8").split("\0") if p]

    for rel in files:
        raw = (ROOT / rel).read_bytes()
        if b"\r" in raw:
            # Judge the committed state; a CRLF working copy over an LF index is only a local note.
            indexed = git("show", f":{rel}")
            if b"\r" not in indexed:
                notes.append(f"W1 WORKTREE_CRLF {rel}")
                raw = indexed
        if raw.startswith(b"\xef\xbb\xbf---") or (raw.startswith(b"---") and b"\r" in raw[:400]):
            findings.append(f"F1 BOM_OR_CRLF {rel}")
            continue
        block = split_block(raw)
        if raw.startswith(b"---\n") and block is None:
            findings.append(f"F1 UNCLOSED {rel}")
            continue
        if block is None:
            continue
        fields, _ = block
        if not fields.get("id"):
            continue
        with_fm += 1
        for key in REQUIRED:
            if not fields.get(key):
                findings.append(f"F1 MISSING_{key.upper()} {rel}")
        if not id_pattern.fullmatch(fields["id"]):
            findings.append(f"F1 BAD_ID {rel} {fields['id']}")
        try:
            datetime.date.fromisoformat(fields.get("created", ""))
        except ValueError:
            findings.append(f"F1 BAD_CREATED {rel} {fields.get('created')}")
        if fields.get("kind") not in KINDS and LEGACY_KINDS.get(rel) != fields.get("kind"):
            findings.append(f"F3 KIND {rel} {fields.get('kind')}")
        owners.setdefault(fields["id"], []).append(rel)

    for ident, paths in owners.items():
        if len(paths) > 1:
            findings.append(f"F2 DUPLICATE {ident} " + " ".join(paths))

    # F4: find the commit that first gave the file a frontmatter block and compare bodies with its parent.
    checked_f4 = 0
    for ident, paths in owners.items():
        rel = paths[0]
        log = git("log", "--format=%H", "--follow", "--", rel).decode().split()
        added = None
        for commit in reversed(log):  # oldest first
            try:
                blob = git("show", f"{commit}:{rel}")
            except subprocess.CalledProcessError:
                continue
            if split_block(blob) and split_block(blob)[0].get("id"):
                added = (commit, blob)
                break
        if not added or added[0] == log[-1]:
            continue  # created with frontmatter from the start
        try:
            parent = git("show", f"{added[0]}^:{rel}")
        except subprocess.CalledProcessError:
            continue  # renamed in the same commit; skip
        checked_f4 += 1
        if split_block(added[1])[1] != parent and not added[0].startswith(ACCEPTED_BODY_CHANGES.get(rel, "-")):
            findings.append(f"F4 BODY_CHANGED {rel} at {added[0][:7]}")

    exempt = set(baseline["exempt_paths"])
    tracked = set(files)
    for rel in sorted(exempt):
        if rel not in tracked:
            findings.append(f"F5 EXEMPT_MISSING {rel}")
        elif rel.endswith(".md") and any(rel in p for p in owners.values()):
            findings.append(f"F5 EXEMPT_HAS_ID {rel}")
    has_id = {p for paths in owners.values() for p in paths}
    for rel in files:
        if rel.startswith(gated) and rel not in has_id and rel not in exempt:
            findings.append(f"F5 GATED_WITHOUT_ID {rel}")

    checked_f6 = 0
    if args.citations:
        rows = json.loads(args.citations.read_text(encoding="utf-8"))
        for row in rows:
            target = row["target"]
            now = (ROOT / target).read_text(encoding="utf-8").splitlines()
            log = git("log", "--format=%H", "--", target).decode().split()
            before = None
            for commit in log:  # newest first; first version without frontmatter
                blob = git("show", f"{commit}:{target}")
                if not blob.startswith(b"---\n"):
                    before = blob.decode("utf-8").splitlines()
                    break
            if before is None:
                findings.append(f"F6 NO_PRE_VERSION {target}")
                continue
            for old, new in zip(range(row["old"][0], row["old"][1] + 1), range(row["new"][0], row["new"][1] + 1)):
                checked_f6 += 1
                if old > len(before) or new > len(now) or before[old - 1] != now[new - 1]:
                    findings.append(f"F6 SHIFT_MISMATCH {target} {old}->{new} (cited by {row['source']}:{row['source_line']})")

    for f in findings + notes:
        print(f)
    print(f"SUMMARY files={len(files)} with_id={with_fm} ids={len(owners)} body_checked={checked_f4} "
          f"citation_lines={checked_f6} findings={len(findings)} notes={len(notes)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
