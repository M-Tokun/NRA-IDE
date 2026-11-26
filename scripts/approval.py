"""合言葉の承認ファイル（1回限り）。書くのは prompt_gate、使うのは push.py・commit.py。

AGENTS.md §7「合言葉の完全一致」の機械側。承認は利用者の入力から hook が作り、
AI は作成・変更しない（PreToolUse ガードで拒否する）。

  .agent_state/approvals/push.json    {"kind": "push", "plan": <計画のパス>, "at": <時刻>}
  .agent_state/approvals/commit.json  {"kind": "commit", "at": <時刻>}

承認はリポジトリ内のファイルで、OS の境界ではない（スクリプト経由の書込みは防げない）。
"""
from __future__ import annotations

import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
APPROVAL_DIR = ROOT / ".agent_state" / "approvals"
KINDS = ("push", "commit")


def _path(kind: str) -> pathlib.Path:
    if kind not in KINDS:
        raise ValueError(f"unknown approval kind: {kind}")
    return APPROVAL_DIR / f"{kind}.json"


def clear_all() -> None:
    """残っている承認をすべて消す。"""
    for kind in KINDS:
        path = _path(kind)
        if path.exists():
            path.unlink()


def write(kind: str, **fields: str) -> None:
    """他の種類の承認を消してから、kind の承認を1つだけ書く。"""
    clear_all()
    APPROVAL_DIR.mkdir(parents=True, exist_ok=True)
    record = {"kind": kind, "at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), **fields}
    _path(kind).write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")


def consume(kind: str, **expected: str) -> str:
    """承認を読んで消す（1回限り）。一致すれば ""、そうでなければ reason を返す。

    読めた承認は、一致しなくても消す（使い回しを防ぐ）。
    """
    path = _path(kind)
    if not path.exists():
        return "NO_APPROVAL"
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        record = {}
    finally:
        path.unlink(missing_ok=True)
    if record.get("kind") != kind:
        return "APPROVAL_MISMATCH"
    for key, value in expected.items():
        if record.get(key) != value:
            return "APPROVAL_MISMATCH"
    return ""
