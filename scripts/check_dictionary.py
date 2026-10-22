"""辞書の整合を検査する / Check the NRA-IDE dictionaries.

  python scripts/check_dictionary.py            検査
  python scripts/check_dictionary.py --update   現在のIDを dictionary/ids.json に追記（検査が通ったときだけ）

検査（規則名）
  DICT-DUP-ID          同じ辞書の中で見出しIDが重複している
  DICT-BAD-ANCHOR      <a id="..."></a> の書式が崩れている
  DICT-NO-HEADING      アンカーの次の行が「### 見出し」でない
  DICT-NO-ANCHOR       用語集（quantum-hybrid）の「### 見出し」の直前にアンカーがない
  DICT-PAIR            日英の片方にしかIDがない
  DICT-PAIR-LINK       「英語版：／Japanese version:」のリンク先IDが、その項目自身のIDと違う
  DICT-BLOCK-ID        各項目の最初のリスト行に、Obsidian用のブロックID（行末の ^ID）がない・不一致・不正
  DICT-PREFIX          用語集のIDが qh- で始まっていない
  DICT-COLLISION       用語集のIDが既存の辞書のIDと衝突している
  DICT-LINK-FILE       辞書へのリンクの、ファイルが存在しない
  DICT-LINK-ANCHOR     辞書へのリンクの、#ID または #^ID が存在しない
  DICT-ID-LOST         公開済み（ids.json 記録済み）のIDが消えた。IDは付け直さず、削除もしない
  DICT-SNAPSHOT        dictionary/ids.json がない
各メッセージは「場所:行: [規則] 何が不正か / 直し方」の形で出す。
"""
from __future__ import annotations

import difflib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DICT = ROOT / "dictionary"
SNAPSHOT = DICT / "ids.json"
ANCHOR_OK = re.compile(r'^<a id="([^"]+)"></a>\s*$')
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
BLOCK_ID_OK = re.compile(r"[A-Za-z0-9-]+")
BLOCK_TAIL = re.compile(r"\s\^([^\s]+)\s*$")
PAIR_LINK_RE = re.compile(r"^- (?:英語版|Japanese version)：?:?\s*\[.*?\]\((.+?)\)")
PAIRS = [
    ("NRA-IDE_Dictionary_JP.md", "NRA-IDE_Dictionary_EN.md"),
    ("quantum-hybrid/Glossary_JP.md", "quantum-hybrid/Glossary_EN.md"),
]
GLOSSARY = {"quantum-hybrid/Glossary_JP.md", "quantum-hybrid/Glossary_EN.md"}
ALL = [name for pair in PAIRS for name in pair]


class Report:
    def __init__(self) -> None:
        self.items: list[str] = []

    def add(self, where: str, rule: str, problem: str, fix: str) -> None:
        self.items.append(f"{where}: [{rule}] {problem}\n    直し方: {fix}")

    def __bool__(self) -> bool:
        return bool(self.items)


def read_lines(rel: str) -> list[str]:
    p = DICT / rel
    return p.read_text(encoding="utf-8").split("\n") if p.exists() else []


BLOCKS: dict[str, set[str]] = {}


def scan(rel: str, rep: Report) -> dict[str, int]:
    """IDと行番号を集める。書式の崩れもここで報告する。"""
    ids: dict[str, int] = {}
    lines = read_lines(rel)
    where = f"dictionary/{rel}"
    if not lines:
        rep.add(where, "DICT-PAIR", "ファイルがない、または空", "ファイルを作る。日英は対で作る")
        return ids
    for n, line in enumerate(lines, 1):
        if "<a id" in line:
            m = ANCHOR_OK.match(line)
            if not m:
                rep.add(f"{where}:{n}", "DICT-BAD-ANCHOR", f"アンカーの書式が不正: {line.strip()[:70]!r}",
                        '行全体を <a id="見出しID"></a> の形にする（ダブルクォート、閉じタグ、前後に余計な文字なし）')
                continue
            i = m.group(1)
            if i in ids:
                rep.add(f"{where}:{n}", "DICT-DUP-ID", f"ID '{i}' が重複（最初は {ids[i]} 行目）",
                        "どちらかを別の語にする。既存のIDは付け直さない")
            else:
                ids[i] = n
            nxt = lines[n] if n < len(lines) else ""
            first = lines[n + 1] if n + 1 < len(lines) else ""
            bm = BLOCK_TAIL.search(first)
            if not bm:
                rep.add(f"{where}:{n + 2}", "DICT-BLOCK-ID", f"項目 '{i}' の最初のリスト行の末尾にブロックID（^{i}）がない",
                        f"行末に ' ^{i}' を足す（Obsidianで安定して参照するため。空白を1つ空けて ^ と同じID）")
            else:
                b = bm.group(1)
                if not BLOCK_ID_OK.fullmatch(b):
                    rep.add(f"{where}:{n + 2}", "DICT-BLOCK-ID", f"ブロックID '^{b}' に使えない文字がある（英字・数字・ハイフンのみ）",
                            "英字・数字・ハイフンだけのIDにする。_ や日本語は使えない")
                elif b != i:
                    rep.add(f"{where}:{n + 2}", "DICT-BLOCK-ID", f"ブロックID '^{b}' が見出しID '{i}' と違う", f"^{i} に揃える")
                BLOCKS.setdefault(rel, set()).add(b)
            if not nxt.startswith("### "):
                rep.add(f"{where}:{n}", "DICT-NO-HEADING", f"アンカー '{i}' の次の行が「### 見出し」でない",
                        "アンカーの直後の行に ### の見出しを置く")
        elif rel in GLOSSARY and line.startswith("### "):
            prev = lines[n - 2] if n >= 2 else ""
            if not ANCHOR_OK.match(prev):
                rep.add(f"{where}:{n}", "DICT-NO-ANCHOR", f"見出し「{line[4:40]}」の直前にアンカーがない",
                        '直前の行に <a id="qh-..."></a> を置く')
    if rel in GLOSSARY:
        for i, n in ids.items():
            if not i.startswith("qh-"):
                rep.add(f"{where}:{n}", "DICT-PREFIX", f"ID '{i}' が qh- で始まっていない", "qh- を付ける（公開前なら）")
    return ids


def check_pair_links(rel: str, rep: Report) -> None:
    """各項目の「英語版：/Japanese version:」のリンクが、自分のIDを指しているか。"""
    lines = read_lines(rel)
    current = None
    for n, line in enumerate(lines, 1):
        m = ANCHOR_OK.match(line)
        if m:
            current = m.group(1)
            continue
        pm = PAIR_LINK_RE.match(line)
        if pm and current:
            target_id = pm.group(1).partition("#")[2].lstrip("^")
            if target_id != current:
                rep.add(f"dictionary/{rel}:{n}", "DICT-PAIR-LINK",
                        f"項目 '{current}' の対訳リンクが '{target_id}' を指している（取り違え）",
                        f"リンク先を #{current} にする。日英で別の語を指していないか、意味も確認する")


def markdown_files() -> list[pathlib.Path]:
    out = subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard", "*.md"],
                         cwd=ROOT, capture_output=True, check=True).stdout.decode("utf-8")
    return [ROOT / p for p in out.split("\0") if p]


def check_links(table: dict[str, dict[str, int]], rep: Report) -> None:
    by_name = {pathlib.PurePosixPath(k).name: k for k in table}
    paths = {(DICT / k).resolve(): k for k in table}
    for md in markdown_files():
        rel_md = md.relative_to(ROOT).as_posix()
        for n, line in enumerate(md.read_text(encoding="utf-8", errors="replace").split("\n"), 1):
            for text, raw in LINK_RE.findall(line):
                if raw.startswith(("http:", "https:", "mailto:")):
                    continue
                path, _, frag = raw.partition("#")
                key = None
                if path:
                    name = pathlib.PurePosixPath(path).name
                    if name not in by_name:
                        continue
                    resolved = (md.parent / path).resolve()
                    key = paths.get(resolved)
                    if key is None:
                        rep.add(f"{rel_md}:{n}", "DICT-LINK-FILE", f"リンク先ファイルが存在しない: {raw}",
                                f"dictionary/{by_name[name]} への正しい相対パスにする。ファイルを移したなら、元の場所に戻すか全リンクを直す")
                        continue
                elif md.relative_to(DICT).as_posix() in table if DICT in md.parents else False:
                    key = md.relative_to(DICT).as_posix()
                if key and frag:
                    is_block = frag.startswith("^")
                    ident = frag.lstrip("^")
                    pool = BLOCKS.get(key, set()) if is_block else set(table[key])
                    if ident not in pool:
                        near = difflib.get_close_matches(ident, pool or table[key].keys(), n=2)
                        hint = f"。近いID: {', '.join(near)}" if near else ""
                        what = "ブロックID ^" if is_block else "ID '"
                        end = "" if is_block else "'"
                        rep.add(f"{rel_md}:{n}", "DICT-LINK-ANCHOR", f"{key} に {what}{ident}{end} がない{hint}",
                                "リンクを実在のIDに直す（#^ID はブロックIDを持つ項目だけ）。IDを付け直した場合は、元のIDに戻す（IDは変えない）")


def main() -> int:
    rep = Report()
    table = {name: scan(name, rep) for name in ALL}
    for jp, en in PAIRS:
        a, b = table[jp], table[en]
        for i in sorted(set(a) - set(b)):
            rep.add(f"dictionary/{jp}:{a[i]}", "DICT-PAIR", f"ID '{i}' の英語版（{en}）がない",
                    f"{en} に同じIDの項目を作る。訳語は Translation_Map.md に従う" if jp in GLOSSARY else f"{en} に同じIDの項目を作る")
        for i in sorted(set(b) - set(a)):
            rep.add(f"dictionary/{en}:{b[i]}", "DICT-PAIR", f"ID '{i}' の日本語版（{jp}）がない",
                    f"{jp} に同じIDの項目を作る")
        check_pair_links(jp, rep)
        check_pair_links(en, rep)
    base = table["NRA-IDE_Dictionary_JP.md"]
    for name in GLOSSARY:
        for i, n in table[name].items():
            if i in base:
                rep.add(f"dictionary/{name}:{n}", "DICT-COLLISION", f"ID '{i}' が NRA-IDE_Dictionary_JP.md と衝突",
                        "正典の語は既存の辞書が正。複製せずリンクで参照し、この項目は別のIDにする")
    check_links(table, rep)

    current = {k: sorted(v) for k, v in table.items()}
    if "--update" in sys.argv:
        if rep:
            print("\n".join(rep.items)); print(f"\nFAIL {len(rep.items)} 件。直してから --update を実行する"); return 1
        old = json.loads(SNAPSHOT.read_text(encoding="utf-8")) if SNAPSHOT.exists() else {}
        merged = {k: sorted(set(old.get(k, [])) | set(v)) for k, v in current.items()}
        SNAPSHOT.write_text(json.dumps(merged, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("updated dictionary/ids.json"); return 0
    if SNAPSHOT.exists():
        old = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
        for name, ids in old.items():
            for i in sorted(set(ids) - set(table.get(name, {}))):
                rep.add(f"dictionary/{name}", "DICT-ID-LOST", f"公開済みのID '{i}' が消えた",
                        "IDは付け直さず、削除もしない。元に戻す。廃止する語は項目を残し「廃止、代替は #…」と書く")
    else:
        rep.add("dictionary/ids.json", "DICT-SNAPSHOT", "ids.json がない", "python scripts/check_dictionary.py --update を一度実行する")
    if rep:
        print("\n".join(rep.items)); print(f"\nFAIL {len(rep.items)} 件"); return 1
    print("OK  dictionaries:", ", ".join(f"{k}={len(v)}" for k, v in current.items() if v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
