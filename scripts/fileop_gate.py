"""Require a file-operation report when a pushed range deletes or renames files.

AGENTS.md §8「ファイル・フォルダ操作の報告」の機械的ゲート。

強制できるのは削除（D）と改名（R）だけである。コピーは追加（A）、上書きは変更（M）として
現れるため通常の編集と区別できず、未追跡ファイルと作業ルート外の操作はGitから見えない。
この範囲の限界は規則の文面で補う。

報告書はパスを`AI-IDE-NRA`配下の形（例`NRA-IDE/theory/AXIOMS.md`）で書くため、
Gitが返すリポジトリ相対パス（例`theory/AXIOMS.md`）の部分一致で照合する。

frontmatterの解析規則は`id_gate.py`と同じだが、`python -I`（isolated modeでは
スクリプトのディレクトリがsys.pathに入らない）でも動くよう、ここに複製する。
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from typing import Mapping, Sequence


EXIT_PASS = 0
EXIT_FINDINGS = 1
EXIT_GATE_ERROR = 2

REPORT_PREFIX = "audit/file_operations/"
REPORT_EXTENSION = ".md"
REQUIRED_KEYS = ("id", "kind", "created", "title")
REPORT_ID_PATTERN = re.compile(r"REPORT-FILEOP-\d{8}-\d{4}")


class GateError(Exception):
    pass


@dataclass(frozen=True)
class Finding:
    rule: str
    path: str
    detail: str


def run_git(repo: pathlib.Path, *arguments: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *arguments],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", "replace").strip()
        raise GateError(f"git {' '.join(arguments[:2])} failed: {message}")
    return result.stdout


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Return the top-level `key: value` pairs of a leading `---` block, or None."""
    lines = text.lstrip(chr(0xFEFF)).splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    values: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return values
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", line)
        if match:
            value = re.sub(r"\s+#.*$", "", match.group(2)).strip()
            values[match.group(1)] = value.strip("\"'")
    return None


def is_report(path: str) -> bool:
    return path.startswith(REPORT_PREFIX) and path.endswith(REPORT_EXTENSION)


def parse_name_status(raw: bytes) -> tuple[list[str], list[tuple[str, str]]]:
    """Split `--name-status -z` output into deleted paths and (old, new) rename pairs.

    A status field is followed by one path, except R/C which carry two.
    """
    tokens = [item.decode("utf-8") for item in raw.split(b"\0") if item]
    deleted: list[str] = []
    renamed: list[tuple[str, str]] = []
    index = 0
    while index < len(tokens):
        status = tokens[index]
        if status[:1] in ("R", "C"):
            if index + 2 >= len(tokens):
                raise GateError("malformed name-status output")
            renamed.append((tokens[index + 1], tokens[index + 2]))
            index += 3
            continue
        if index + 1 >= len(tokens):
            raise GateError("malformed name-status output")
        if status[:1] == "D":
            deleted.append(tokens[index + 1])
        index += 2
    return deleted, renamed


def mentions(text: str, path: str) -> bool:
    """A report may write the path with either separator."""
    return path in text or path.replace("/", "\\") in text


def read_reports(repo: pathlib.Path, head: str, paths: Sequence[str]) -> dict[str, str]:
    """Read report blobs by object id; `git show rev:path` fails on long Windows paths."""
    wanted = set(paths)
    oids: dict[str, str] = {}
    for entry in run_git(repo, "ls-tree", "-r", "-z", head).split(b"\0"):
        if not entry:
            continue
        meta, _, raw_path = entry.partition(b"\t")
        path = raw_path.decode("utf-8")
        if path in wanted:
            oids[path] = meta.split()[2].decode("ascii")
    contents: dict[str, str] = {}
    for path, oid in oids.items():
        blob = run_git(repo, "cat-file", "blob", oid)
        try:
            contents[path] = blob.decode("utf-8")
        except UnicodeDecodeError as error:
            raise GateError(f"not valid UTF-8: {path}") from error
    return contents


def check_reports(reports: Mapping[str, str]) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(reports):
        frontmatter = parse_frontmatter(reports[path])
        if frontmatter is None:
            findings.append(Finding("NO_FRONTMATTER", path, "frontmatter (--- block at line 1) is missing"))
            continue
        for key in REQUIRED_KEYS:
            if not frontmatter.get(key):
                findings.append(Finding("MISSING_KEY", path, f"required key is missing or empty: {key}"))
        identifier = frontmatter.get("id", "")
        if identifier and not REPORT_ID_PATTERN.fullmatch(identifier):
            findings.append(Finding("BAD_REPORT_ID", path,
                                    f"id does not match {REPORT_ID_PATTERN.pattern}: {identifier}"))
    return findings


def evaluate_range(repo: pathlib.Path, base: str, head: str):
    """Return the affected paths, the reports added in the range, and the findings."""
    deleted, renamed = parse_name_status(
        run_git(repo, "diff", "--name-status", "-z", "-M", "--diff-filter=DR", base, head)
    )
    # 50 requires both sides of a move; a rename with detection off arrives as D plus A.
    # 過去の報告書の削除・改名も対象に含める。除外すると記録なしで記録を消せる。
    affected = sorted({*deleted, *(old for old, _ in renamed), *(new for _, new in renamed)})

    added = [
        item.decode("utf-8")
        for item in run_git(repo, "diff", "--name-only", "-z", "-M", "--diff-filter=AMR", base, head).split(b"\0")
        if item
    ]
    report_paths = sorted(path for path in added if is_report(path))

    findings: list[Finding] = []
    if not affected:
        return affected, {}, findings

    reports = read_reports(repo, head, report_paths)
    if not reports:
        findings.append(Finding(
            "MISSING_REPORT", REPORT_PREFIX,
            f"{len(affected)} path(s) deleted or renamed, but no report was added under {REPORT_PREFIX}",
        ))
        return affected, reports, findings

    findings.extend(check_reports(reports))
    for path in affected:
        if not any(mentions(text, path) for text in reports.values()):
            findings.append(Finding("PATH_NOT_REPORTED", path,
                                    "deleted or renamed path is not named in any added report"))
    return affected, reports, findings


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check that pushed deletions and renames carry a file-operation report."
    )
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--base")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args(argv)
    repo = arguments.repo.resolve()

    try:
        if not arguments.base:
            raise GateError("--base is required")
        affected, reports, findings = evaluate_range(repo, arguments.base, arguments.head)
    except GateError as error:
        print(f"FILEOP_GATE: error: {error}", file=sys.stderr)
        return EXIT_GATE_ERROR

    if arguments.json:
        print(json.dumps({"schema_version": 1, "status": "FAIL" if findings else "PASS",
                          "scanned_files": len(affected), "report_files": len(reports),
                          "base": arguments.base, "head": arguments.head,
                          "findings": [asdict(f) for f in findings]}, ensure_ascii=True))
        return EXIT_FINDINGS if findings else EXIT_PASS
    print(f"FILEOP_GATE: checked {len(affected)} deleted/renamed path(s) against {len(reports)} report(s)")
    for finding in findings:
        print(json.dumps(asdict(finding)))
    if findings:
        print(f"FILEOP_GATE: FAIL ({len(findings)} finding(s))", file=sys.stderr)
        return EXIT_FINDINGS
    print("FILEOP_GATE: PASS")
    return EXIT_PASS


if __name__ == "__main__":
    sys.exit(main())
