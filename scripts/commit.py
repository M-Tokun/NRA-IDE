"""commit の入口（固定経路）。AGENTS.md 59 から呼ぶ。設計：local_reports/route_design_20261126/

  python -B scripts/commit.py run --paths <p> [<p> ...] --message-file <f>

経路（番号はこのファイル内だけ。最後の1行の最初の語が呼び出し元への戻り：STOP・DONE）:
  10 承認（commit）を消費する。なければ STOP NO_APPROVAL／APPROVAL_MISMATCH
  20 指定パスだけを stage する（作業ツリーにあるパスは git add、ないパスは git rm --cached
     --ignore-unmatch で削除を stage）。失敗は STOP STAGE_FAILED
  30 IF cached の一覧 != 指定パス: STOP CACHED_DIFFERS
  40 cached から、削除・改名（D・R）、過去に削除されたパスの再追加（復元）、
     追跡済みファイルと同じ内容の追加（コピー）を集める（報告書そのものは除く）
  50 IF 40 が空でない AND（報告書 audit/file_operations/*.md が cached にない
     OR frontmatter が欠ける OR 各パスを本文に書いていない）: STOP FILEOP_REPORT_MISSING
  60 署名を外す指定なしで git commit -F <f>。失敗は STOP COMMIT_FAILED
  70 commit ID を出して DONE

STOP のとき stage は戻さない（状態を報告するだけ。戻すのは利用者）。
STOP は直前の行に reason: を出す。detail（パス等）は記録 local_reports/commit_gate/commit_log.jsonl にだけ残す。
reason：NO_APPROVAL・APPROVAL_MISMATCH・BAD_ARGUMENTS・STAGE_FAILED・CACHED_DIFFERS・
        FILEOP_REPORT_MISSING・GIT_FAILED・COMMIT_FAILED
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import approval  # noqa: E402
import fileop_gate  # noqa: E402

LOG_DIR = ROOT / "local_reports" / "commit_gate"
TIMEOUT = 120
EMPTY_BLOBS = {"e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
               "473a0f4c3be8a93681a267e3b1e9a7dcda1185436fe141f7749120a303721813"}  # SHA-1・SHA-256


class Stop(Exception):
    def __init__(self, reason, detail=""):
        super().__init__(reason)
        self.reason, self.detail = reason, detail


def _log(step, result, reason="", detail=""):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    rec = {"at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
           "step": step, "result": result, "reason": reason}
    if detail:
        rec["detail"] = detail
    with (LOG_DIR / "commit_log.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _git(*args, check=True):
    done = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, timeout=TIMEOUT)
    if check and done.returncode != 0:
        raise Stop("GIT_FAILED", " ".join(args[:2]))
    return done


def _z(raw: bytes) -> list[str]:
    return [item.decode("utf-8") for item in raw.split(b"\0") if item]


def _rel(path: str) -> str:
    """指定パスをリポジトリ相対の / 区切りにする。ルート外は BAD_ARGUMENTS。"""
    p = pathlib.Path(path)
    full = (p if p.is_absolute() else ROOT / p).resolve()
    if ROOT != full and ROOT not in full.parents:
        raise Stop("BAD_ARGUMENTS", path)
    return full.relative_to(ROOT).as_posix()


def collect_fileops(cached_status: bytes) -> list[str]:
    """40：報告書が要るパス（削除・改名の両側、復元、コピー）。報告書そのものは除く。"""
    deleted, renamed = fileop_gate.parse_name_status(cached_status)
    need = {*deleted, *(o for o, _ in renamed), *(n for _, n in renamed)}
    added = _z(_git("diff", "--cached", "--name-only", "-z", "--no-renames", "--diff-filter=A").stdout)
    if added:
        ever_deleted = set(_z(_git("log", "--diff-filter=D", "--name-only", "--format=", "-z").stdout))
        head = _git("rev-parse", "--verify", "--quiet", "HEAD", check=False)
        tracked_blobs = set()
        if head.returncode == 0:
            for entry in _git("ls-tree", "-r", "-z", "HEAD").stdout.split(b"\0"):
                if entry:
                    tracked_blobs.add(entry.split(b"\t", 1)[0].split()[2].decode("ascii"))
        staged = {}
        for entry in _git("ls-files", "-s", "-z", "--", *added).stdout.split(b"\0"):
            if entry:
                meta, _, raw_path = entry.partition(b"\t")
                staged[raw_path.decode("utf-8")] = meta.split()[1].decode("ascii")
        tracked_blobs -= EMPTY_BLOBS  # 空ファイル同士は「コピー」と見なさない
        for path in added:
            if path in ever_deleted or staged.get(path) in tracked_blobs:
                need.add(path)
    return sorted(p for p in need if not fileop_gate.is_report(p))


def read_staged_reports(paths: list[str]) -> dict[str, str]:
    reports = {}
    for entry in _git("ls-files", "-s", "-z", "--", *paths).stdout.split(b"\0"):
        if not entry:
            continue
        meta, _, raw_path = entry.partition(b"\t")
        blob = _git("cat-file", "blob", meta.split()[1].decode("ascii")).stdout
        reports[raw_path.decode("utf-8")] = blob.decode("utf-8", "replace")
    return reports


def run(paths: list[str], message_file: str) -> str:
    # 10
    reason = approval.consume("commit")
    if reason:
        raise Stop(reason)
    if not paths or not pathlib.Path(message_file).is_file():
        raise Stop("BAD_ARGUMENTS", message_file)
    wanted = sorted({_rel(p) for p in paths})
    # 20 作業ツリーにあるパスは add、ないパス（削除）は index から外す。
    #    削除がすでに stage 済みでも失敗しない（git add は pathspec 不一致で失敗する）。範囲は 30 が照合する。
    present = [p for p in wanted if (ROOT / p).exists()]
    absent = [p for p in wanted if p not in present]
    if present and _git("add", "--", *present, check=False).returncode != 0:
        raise Stop("STAGE_FAILED")
    if absent and _git("rm", "--cached", "--ignore-unmatch", "--quiet", "--", *absent,
                       check=False).returncode != 0:
        raise Stop("STAGE_FAILED")
    # 30
    cached = sorted(set(_z(_git("diff", "--cached", "--name-only", "-z", "--no-renames").stdout)))
    if cached != wanted:
        extra = sorted(set(cached) - set(wanted))
        missing = sorted(set(wanted) - set(cached))
        raise Stop("CACHED_DIFFERS", json.dumps({"extra": extra, "missing": missing}, ensure_ascii=False))
    # 40
    status = _git("diff", "--cached", "--name-status", "-z", "-M").stdout
    need = collect_fileops(status)
    # 50
    if need:
        report_paths = [p for p in cached if fileop_gate.is_report(p)]
        reports = read_staged_reports(report_paths) if report_paths else {}
        missing = [p for p in need if not any(fileop_gate.mentions(t, p) for t in reports.values())]
        if not reports or fileop_gate.check_reports(reports) or missing:
            raise Stop("FILEOP_REPORT_MISSING", json.dumps({"unreported": missing}, ensure_ascii=False))
    # 60
    if _git("commit", "-F", str(pathlib.Path(message_file).resolve()), check=False).returncode != 0:
        raise Stop("COMMIT_FAILED")
    # 70
    return _git("rev-parse", "HEAD").stdout.decode("ascii").strip()


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="commit の入口（固定経路）")
    parser.add_argument("stage", choices=["run"])
    parser.add_argument("--paths", nargs="+", required=True)
    parser.add_argument("--message-file", required=True)
    args = parser.parse_args(argv)
    try:
        oid = run(args.paths, args.message_file)
    except Stop as stop:
        _log("run", "STOP", stop.reason, stop.detail)
        print(f"reason: {stop.reason}")
        print("STOP")
        return 1
    except subprocess.TimeoutExpired:
        _log("run", "STOP", "TIMEOUT")
        print("reason: TIMEOUT")
        print("STOP")
        return 1
    _log("70", "DONE", detail=oid)
    print(f"commit: {oid}")
    print("DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
