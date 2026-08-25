from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import stat
import sys
import tempfile
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Iterable, Sequence

import unicode_gate


SCHEMA_VERSION = 1
DEFAULT_REPORT = pathlib.Path("local_reports/unicode_gate/list.list")
DECISIONS = {"PENDING", "REJECTED", "APPROVED"}
APPLY_ACTIONS = {"REMOVE_CODEPOINT", "REPLACE_CODEPOINT", "REPLACE_WITH_ESCAPE"}


@dataclass(frozen=True)
class PreparedChange:
    path: str
    candidate: pathlib.Path
    original: bytes
    updated: bytes
    mode: int
    finding_ids: tuple[str, ...]


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def immutable_fields(record: dict[str, Any]) -> dict[str, Any]:
    return {
        key: record[key]
        for key in (
            "record_type",
            "path",
            "file_sha256",
            "rule",
            "severity",
            "line",
            "column",
            "codepoint",
            "name",
            "category",
            "bidi_class",
            "escaped_context",
            "detail",
            "suggested_action",
        )
    }


def finding_id(record: dict[str, Any]) -> str:
    digest = sha256_bytes(canonical_json(immutable_fields(record)).encode("ascii"))
    return "UG-" + digest[:16].upper()


def suggested_action(rule: str, codepoint: str | None) -> str:
    if codepoint is None:
        return "MANUAL_REVIEW_ONLY"
    if rule in {
        "BIDI_CONTROL",
        "BOM",
        "CONTROL_CHARACTER",
        "FORMAT_CHARACTER",
        "INVISIBLE_FORMAT",
        "LINE_SEPARATOR",
        "NONCHARACTER",
        "VARIATION_SELECTOR",
    }:
        return "REVIEW_REMOVE_OR_REPLACE"
    return "MANUAL_REVIEW_ONLY"


def make_records(
    inputs: Iterable[tuple[str, bytes]], policy: unicode_gate.Policy
) -> tuple[int, list[dict[str, Any]]]:
    scanned = 0
    records: list[dict[str, Any]] = []
    for path, raw in inputs:
        scanned += 1
        file_hash = sha256_bytes(raw)
        for finding in unicode_gate.scan_bytes(path, raw, policy):
            record: dict[str, Any] = {
                "record_type": "finding",
                "path": path,
                "file_sha256": file_hash,
                "rule": finding.rule,
                "severity": finding.severity.upper(),
                "line": finding.line,
                "column": finding.column,
                "codepoint": finding.codepoint,
                "name": finding.name,
                "category": finding.category,
                "bidi_class": finding.bidi_class,
                "escaped_context": finding.escaped_context,
                "detail": finding.detail,
                "suggested_action": suggested_action(finding.rule, finding.codepoint),
                "decision": "PENDING",
                "action": "NONE",
                "replacement_codepoint": None,
            }
            record["id"] = finding_id(record)
            records.append(record)
    records.sort(key=lambda item: (
        item["path"], item["line"] or 0, item["column"] or 0,
        item["rule"], item["codepoint"] or "",
    ))
    return scanned, records


def report_lines(scanned: int, records: Sequence[dict[str, Any]]) -> list[str]:
    failed = sum(record["severity"] == "FAIL" for record in records)
    warned = sum(record["severity"] == "WARN" for record in records)
    record_set = sha256_bytes(
        "\n".join(record["id"] for record in records).encode("ascii")
    )
    header = {
        "record_type": "unicode_review",
        "schema_version": SCHEMA_VERSION,
        "unicode_database_version": unicodedata.unidata_version,
        "scanned_files": scanned,
        "finding_count": len(records),
        "fail_count": failed,
        "warn_count": warned,
        "record_set_sha256": record_set,
        "status": "PENDING_REVIEW" if records else "PASS",
    }
    return [canonical_json(header), *(canonical_json(record) for record in records)]


def write_report(path: pathlib.Path, lines: Sequence[str], replace_existing: bool) -> None:
    if path.exists() and not replace_existing:
        raise FileExistsError(
            f"report already exists; use --replace-existing after preserving decisions: {path}"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = ("\n".join(lines) + "\n").encode("ascii")
    path.write_bytes(payload)


def write_json_document(path: pathlib.Path, value: object, replace_existing: bool) -> None:
    if path.exists() and not replace_existing:
        raise FileExistsError(f"output already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True) + "\n").encode(
        "ascii"
    )
    path.write_bytes(payload)


def load_report(path: pathlib.Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    raw = path.read_bytes()
    raw.decode("ascii")
    documents = [json.loads(line) for line in raw.decode("ascii").splitlines() if line]
    if not documents:
        raise ValueError("empty review report")
    header, *records = documents
    if header.get("record_type") != "unicode_review":
        raise ValueError("invalid report header")
    if header.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported report schema_version")
    if header.get("finding_count") != len(records):
        raise ValueError("report finding_count mismatch")
    ids: list[str] = []
    for record in records:
        if record.get("record_type") != "finding":
            raise ValueError("invalid finding record")
        try:
            expected_id = finding_id(record)
        except KeyError as exc:
            raise ValueError(f"finding record is missing field: {exc.args[0]}") from exc
        if record.get("id") != expected_id:
            raise ValueError(f"immutable finding fields changed: {record.get('id')}")
        if record.get("decision") not in DECISIONS:
            raise ValueError(f"invalid decision for {expected_id}")
        ids.append(expected_id)
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate finding id")
    expected_set = sha256_bytes("\n".join(ids).encode("ascii"))
    if header.get("record_set_sha256") != expected_set:
        raise ValueError("report record set mismatch")
    return header, records


def baseline_document(records: Sequence[dict[str, Any]]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    approved_scope = {
        ("VARIATION_SELECTOR", "U+FE0F"),
        ("BOM", "U+FEFF"),
        ("INVISIBLE_FORMAT", "U+200D"),
    }
    for record in records:
        if (record["rule"], record["codepoint"]) not in approved_scope:
            continue
        fields = {
            key: record[key]
            for key in ("path", "file_sha256", "rule", "codepoint", "line", "column")
        }
        entries.append({
            "id": unicode_gate.baseline_entry_id(fields),
            **fields,
            "reason": "existing occurrence approved for exact baseline",
        })
    entries.sort(key=lambda item: (
        item["path"], item["line"], item["column"], item["id"]
    ))
    if not entries:
        raise ValueError("report contains no findings within the approved baseline scope")
    if len({entry["id"] for entry in entries}) != len(entries):
        raise ValueError("baseline selection contains duplicate entries")
    approved_rules = sorted({rule for rule, _ in approved_scope})
    return {
        "schema_version": 1,
        "scope": "exact existing occurrences of " + ", ".join(approved_rules) + " only",
        "entries": entries,
    }


def update_decisions(
    header: dict[str, Any],
    records: list[dict[str, Any]],
    codepoints: frozenset[str],
    decision: str,
    action: str,
    paths: frozenset[str] | None = None,
) -> int:
    if decision not in {"APPROVED", "REJECTED"}:
        raise ValueError("decision command permits only APPROVED or REJECTED")
    if decision == "APPROVED" and action not in {
        "REMOVE_CODEPOINT", "REPLACE_WITH_ESCAPE"
    }:
        raise ValueError("approved deterministic selection has an invalid action")
    if decision == "REJECTED" and action != "NONE":
        raise ValueError("rejected selection requires NONE action")
    selected = 0
    for record in records:
        if record.get("codepoint") not in codepoints:
            continue
        if paths is not None and record.get("path") not in paths:
            continue
        if decision == "APPROVED" and record.get("suggested_action") != "REVIEW_REMOVE_OR_REPLACE":
            raise ValueError(f"finding is not removable by this command: {record['id']}")
        record["decision"] = decision
        record["action"] = action
        record["replacement_codepoint"] = None
        selected += 1
    if selected == 0:
        raise ValueError("decision selection matched no findings")
    counts = {value: 0 for value in DECISIONS}
    for record in records:
        counts[record["decision"]] += 1
    header["pending_count"] = counts["PENDING"]
    header["approved_count"] = counts["APPROVED"]
    header["rejected_count"] = counts["REJECTED"]
    header["status"] = "PENDING_REVIEW" if counts["PENDING"] else "DECIDED"
    return selected


def rewrite_report(
    path: pathlib.Path, header: dict[str, Any], records: Sequence[dict[str, Any]]
) -> None:
    payload = (
        "\n".join([canonical_json(header), *(canonical_json(record) for record in records)])
        + "\n"
    ).encode("ascii")
    path.write_bytes(payload)


def safe_repo_path(repo: pathlib.Path, supplied: str) -> pathlib.Path:
    candidate = repo / pathlib.PurePosixPath(supplied)
    if candidate.is_symlink():
        raise OSError(f"symbolic link cannot be modified: {unicode_gate.ascii_escape(supplied)}")
    resolved = candidate.resolve()
    if repo != resolved and repo not in resolved.parents:
        raise OSError(f"path resolves outside repository: {unicode_gate.ascii_escape(supplied)}")
    if not resolved.is_file():
        raise OSError(f"not a regular file: {unicode_gate.ascii_escape(supplied)}")
    return resolved


def character_index(text: str, line: int, column: int) -> int:
    if line < 1 or column < 1:
        raise ValueError("line and column must be positive")
    # unicode_gate.location() treats LF as the only line boundary.  Do not use
    # splitlines(), which would also treat suspicious U+0085/U+2028/U+2029 as
    # line boundaries and could target the wrong character during remediation.
    lines = text.split("\n")
    if line > len(lines):
        raise ValueError("approved location is outside current file")
    if column > len(lines[line - 1]):
        raise ValueError("approved location is outside current file")
    index = sum(len(value) + 1 for value in lines[: line - 1]) + column - 1
    return index


def replacement_character(record: dict[str, Any]) -> str:
    action = record.get("action")
    if action not in APPLY_ACTIONS:
        raise ValueError(f"approved record has invalid action: {record['id']}")
    if action == "REMOVE_CODEPOINT":
        if record.get("replacement_codepoint") is not None:
            raise ValueError(f"removal must not specify replacement: {record['id']}")
        return ""
    if action == "REPLACE_WITH_ESCAPE":
        if record.get("replacement_codepoint") is not None:
            raise ValueError(f"escape replacement must not specify codepoint: {record['id']}")
        value = unicode_gate.parse_codepoint(record["codepoint"])
        if value <= 0xFFFF:
            return "\\u" + f"{value:04X}"
        return "\\U" + f"{value:08X}"
    replacement = record.get("replacement_codepoint")
    if not isinstance(replacement, str):
        raise ValueError(f"replacement codepoint is required: {record['id']}")
    value = unicode_gate.parse_codepoint(replacement)
    if value > 0x10FFFF or 0xD800 <= value <= 0xDFFF:
        raise ValueError(f"replacement is not a Unicode scalar: {record['id']}")
    character = chr(value)
    if record.get("codepoint") == replacement:
        raise ValueError(f"replacement must change the codepoint: {record['id']}")
    return character


def finding_signature(finding: unicode_gate.Finding) -> tuple[str, str | None, str]:
    return finding.rule, finding.codepoint, finding.detail


def prepare_approved(
    repo: pathlib.Path,
    records: Sequence[dict[str, Any]],
    policy: unicode_gate.Policy,
) -> list[PreparedChange]:
    approved = [record for record in records if record["decision"] == "APPROVED"]
    if not approved:
        raise ValueError("report contains no APPROVED findings")
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in approved:
        if record.get("codepoint") is None or record.get("line") is None or record.get("column") is None:
            raise ValueError(f"finding cannot be applied automatically: {record['id']}")
        grouped[record["path"]].append(record)

    prepared: list[PreparedChange] = []
    for path, path_records in sorted(grouped.items()):
        candidate = safe_repo_path(repo, path)
        raw = candidate.read_bytes()
        hashes = {record["file_sha256"] for record in path_records}
        if hashes != {sha256_bytes(raw)}:
            raise ValueError(f"file hash changed since scan: {unicode_gate.ascii_escape(path)}")
        text = raw.decode("utf-8")
        edits: list[tuple[int, str, str]] = []
        for record in path_records:
            index = character_index(text, record["line"], record["column"])
            expected = chr(unicode_gate.parse_codepoint(record["codepoint"]))
            if text[index] != expected:
                raise ValueError(f"codepoint mismatch at approved location: {record['id']}")
            edits.append((index, expected, replacement_character(record)))
        if len({index for index, _, _ in edits}) != len(edits):
            raise ValueError(f"multiple approved edits target one character: {unicode_gate.ascii_escape(path)}")
        updated = text
        for index, expected, replacement in sorted(edits, reverse=True):
            if updated[index] != expected:
                raise ValueError(f"edit ordering mismatch: {unicode_gate.ascii_escape(path)}")
            updated = updated[:index] + replacement + updated[index + 1:]
        updated_raw = updated.encode("utf-8")
        before = unicode_gate.scan_bytes(path, raw, policy)
        after = unicode_gate.scan_bytes(path, updated_raw, policy)
        before_counts: dict[tuple[str, str | None, str], int] = defaultdict(int)
        after_counts: dict[tuple[str, str | None, str], int] = defaultdict(int)
        for finding in before:
            before_counts[finding_signature(finding)] += 1
        for finding in after:
            after_counts[finding_signature(finding)] += 1
        if any(count > before_counts[signature] for signature, count in after_counts.items()):
            raise ValueError(
                f"approved edits introduce a new finding: {unicode_gate.ascii_escape(path)}"
            )
        prepared.append(PreparedChange(
            path=path,
            candidate=candidate,
            original=raw,
            updated=updated_raw,
            mode=stat.S_IMODE(candidate.stat().st_mode),
            finding_ids=tuple(sorted(record["id"] for record in path_records)),
        ))
    return prepared


def atomic_replace(candidate: pathlib.Path, raw: bytes, mode: int) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=candidate.name + ".", dir=candidate.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary_name, mode)
        os.replace(temporary_name, candidate)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def backup_document(prepared: Sequence[PreparedChange]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "record_type": "unicode_remediation_backup",
        "files": [
            {
                "path": item.path,
                "original_sha256": sha256_bytes(item.original),
                "planned_sha256": sha256_bytes(item.updated),
                "blob": "blobs/" + sha256_bytes(item.original) + ".blob",
                "mode": item.mode,
                "finding_ids": list(item.finding_ids),
            }
            for item in prepared
        ],
    }


def write_backup(directory: pathlib.Path, prepared: Sequence[PreparedChange]) -> None:
    if directory.exists():
        raise FileExistsError(f"backup directory already exists: {directory}")
    blobs = directory / "blobs"
    blobs.mkdir(parents=True)
    for item in prepared:
        blob = blobs / (sha256_bytes(item.original) + ".blob")
        if blob.exists():
            if blob.read_bytes() != item.original:
                raise ValueError("backup blob hash collision")
        else:
            blob.write_bytes(item.original)
    write_json_document(directory / "manifest.json", backup_document(prepared), False)


def verify_backup(directory: pathlib.Path, prepared: Sequence[PreparedChange]) -> None:
    manifest = json.loads((directory / "manifest.json").read_text(encoding="ascii"))
    if manifest != backup_document(prepared):
        raise ValueError("backup manifest does not match approved remediation")
    for item in prepared:
        blob = directory / "blobs" / (sha256_bytes(item.original) + ".blob")
        if sha256_bytes(blob.read_bytes()) != sha256_bytes(item.original):
            raise ValueError(f"backup blob verification failed: {unicode_gate.ascii_escape(item.path)}")


def restore_backup(repo: pathlib.Path, directory: pathlib.Path) -> list[str]:
    """Restore files only when the prepared manifest and current hashes agree.

    ``repo`` bounds every manifest path and ``directory`` must contain the
    schema-versioned backup manifest and referenced blobs. A file is restored
    only when its current SHA-256 equals the planned remediated hash; an already
    original file is skipped. Any path escape, hash mismatch, or malformed
    record raises ``ValueError`` before replacement of that invalid record.
    Returns repository-relative paths restored during this call.
    """
    manifest = json.loads((directory / "manifest.json").read_text(encoding="ascii"))
    if manifest.get("schema_version") != 1 or manifest.get("record_type") != "unicode_remediation_backup":
        raise ValueError("invalid remediation backup manifest")
    files = manifest.get("files")
    if not isinstance(files, list):
        raise ValueError("backup manifest files must be a list")
    prepared: list[tuple[pathlib.Path, bytes, int, str]] = []
    for item in files:
        path = item.get("path")
        if not isinstance(path, str):
            raise ValueError("backup path must be a string")
        candidate = safe_repo_path(repo, path)
        current_hash = sha256_bytes(candidate.read_bytes())
        original_hash = item.get("original_sha256")
        planned_hash = item.get("planned_sha256")
        if current_hash == original_hash:
            continue
        if current_hash != planned_hash:
            raise ValueError(
                f"current file is neither original nor planned version: {unicode_gate.ascii_escape(path)}"
            )
        blob = (directory / item["blob"]).resolve()
        if directory.resolve() not in blob.parents:
            raise ValueError("backup blob resolves outside backup directory")
        original = blob.read_bytes()
        if sha256_bytes(original) != original_hash:
            raise ValueError(f"backup original hash mismatch: {unicode_gate.ascii_escape(path)}")
        mode = item.get("mode")
        if not isinstance(mode, int):
            raise ValueError("backup mode must be an integer")
        prepared.append((candidate, original, mode, path))
    for candidate, original, mode, _ in prepared:
        atomic_replace(candidate, original, mode)
    return [path for _, _, _, path in prepared]


def apply_approved(
    repo: pathlib.Path,
    records: Sequence[dict[str, Any]],
    policy: unicode_gate.Policy,
    backup: pathlib.Path | None = None,
) -> list[str]:
    """Apply only explicitly approved and fully revalidated Unicode changes.

    ``records`` and ``policy`` are rechecked by ``prepare_approved`` against
    current file hashes and exact findings. When ``backup`` is supplied its
    manifest must match every planned change before replacement begins. Files
    are atomically replaced with their original modes, and the returned paths
    identify applied changes. Validation failures raise before any replacement.
    """
    prepared = prepare_approved(repo, records, policy)
    if backup is not None:
        verify_backup(backup, prepared)

    for item in prepared:
        atomic_replace(item.candidate, item.updated, item.mode)
    return [item.path for item in prepared]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Deterministic Unicode review workflow")
    parser.add_argument(
        "--repo",
        type=pathlib.Path,
        default=pathlib.Path.cwd(),
        help="repository root used for all reviewed paths (default: cwd)",
    )
    parser.add_argument(
        "--policy",
        type=pathlib.Path,
        help="Unicode Gate policy JSON path (default: repository policy)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="write an ASCII-only review report")
    scope = scan.add_mutually_exclusive_group(required=True)
    scope.add_argument("--all", action="store_true", help="scan tracked working-tree files")
    scope.add_argument("--paths", nargs="+", metavar="PATH", help="scan explicit repository files")
    scan.add_argument(
        "--output",
        type=pathlib.Path,
        default=DEFAULT_REPORT,
        help=f"ASCII-only review report path (default: {DEFAULT_REPORT})",
    )
    scan.add_argument(
        "--replace-existing",
        action="store_true",
        help="replace an existing report instead of refusing to overwrite it",
    )

    apply_parser = subparsers.add_parser("apply", help="apply explicitly approved records")
    apply_parser.add_argument(
        "--report",
        type=pathlib.Path,
        default=DEFAULT_REPORT,
        help=f"review report containing explicit approvals (default: {DEFAULT_REPORT})",
    )
    apply_parser.add_argument(
        "--backup",
        type=pathlib.Path,
        default=pathlib.Path("local_reports/unicode_gate/remediation_backup"),
        help="prepared backup directory whose manifest must match the planned changes",
    )

    prepare_parser = subparsers.add_parser(
        "prepare", help="materialize verified originals and a planned-hash manifest"
    )
    prepare_parser.add_argument(
        "--report",
        type=pathlib.Path,
        default=DEFAULT_REPORT,
        help=f"review report containing explicit approvals (default: {DEFAULT_REPORT})",
    )
    prepare_parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=pathlib.Path("local_reports/unicode_gate/remediation_backup"),
        help="directory for verified originals and the planned-hash manifest",
    )

    baseline_parser = subparsers.add_parser(
        "baseline", help="write an exact U+FE0F baseline from a review report"
    )
    baseline_parser.add_argument(
        "--report",
        type=pathlib.Path,
        default=DEFAULT_REPORT,
        help=f"review report used to construct exact baseline entries (default: {DEFAULT_REPORT})",
    )
    baseline_parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=pathlib.Path("unicode_gate_baseline.json"),
        help="exact baseline JSON path (default: unicode_gate_baseline.json)",
    )
    baseline_parser.add_argument(
        "--replace-existing",
        action="store_true",
        help="replace an existing baseline instead of refusing to overwrite it",
    )

    decide_parser = subparsers.add_parser(
        "decide", help="set deterministic decisions for exact codepoints"
    )
    decide_parser.add_argument(
        "--report",
        type=pathlib.Path,
        default=DEFAULT_REPORT,
        help=f"review report to update (default: {DEFAULT_REPORT})",
    )
    decide_parser.add_argument(
        "--codepoint",
        nargs="+",
        required=True,
        help="one or more exact Unicode code points such as U+202E",
    )
    decide_parser.add_argument(
        "--path",
        action="append",
        help="limit the decision to an exact repository path; repeat as needed",
    )
    decide_parser.add_argument(
        "--decision",
        choices=["APPROVED", "REJECTED"],
        required=True,
        help="human decision recorded for each matched finding",
    )
    decide_parser.add_argument(
        "--action",
        choices=["NONE", "REMOVE_CODEPOINT", "REPLACE_WITH_ESCAPE"],
        required=True,
        help="approved remediation action; NONE records review without changing text",
    )

    restore_parser = subparsers.add_parser(
        "restore", help="restore only files that exactly match a planned remediation"
    )
    restore_parser.add_argument(
        "--backup",
        type=pathlib.Path,
        default=pathlib.Path("local_reports/unicode_gate/remediation_backup"),
        help="prepared backup directory containing the restore manifest and blobs",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        repo = args.repo.resolve()
        policy_path = (args.policy or repo / "unicode_gate_policy.json").resolve()
        policy = unicode_gate.load_policy(policy_path)
        if args.command == "scan":
            inputs = (
                unicode_gate.tracked_worktree_inputs(repo)
                if args.all
                else unicode_gate.explicit_inputs(repo, args.paths)
            )
            scanned, records = make_records(inputs, policy)
            output = args.output if args.output.is_absolute() else repo / args.output
            write_report(output, report_lines(scanned, records), args.replace_existing)
            print(
                f"unicode-review report={unicode_gate.ascii_escape(str(output))} "
                f"scanned={scanned} findings={len(records)} pending={len(records)}"
            )
            return unicode_gate.EXIT_FINDINGS if records else unicode_gate.EXIT_PASS

        if args.command == "restore":
            backup = args.backup if args.backup.is_absolute() else repo / args.backup
            restored = restore_backup(repo, backup)
            print(f"unicode-review restored={len(restored)}")
            for path in restored:
                print("  " + unicode_gate.ascii_escape(path))
            return unicode_gate.EXIT_PASS

        report = args.report if args.report.is_absolute() else repo / args.report
        header, records = load_report(report)
        if args.command == "baseline":
            output = args.output if args.output.is_absolute() else repo / args.output
            document = baseline_document(records)
            write_json_document(output, document, args.replace_existing)
            print(
                f"unicode-review baseline={unicode_gate.ascii_escape(str(output))} "
                f"entries={len(document['entries'])}"
            )
            return unicode_gate.EXIT_PASS
        if args.command == "decide":
            codepoints = frozenset(
                unicode_gate.codepoint_label(unicode_gate.parse_codepoint(value))
                for value in args.codepoint
            )
            selected = update_decisions(
                header,
                records,
                codepoints,
                args.decision,
                args.action,
                frozenset(args.path) if args.path else None,
            )
            rewrite_report(report, header, records)
            print(
                f"unicode-review decision={args.decision} action={args.action} "
                f"selected={selected}"
            )
            return unicode_gate.EXIT_PASS
        if args.command == "prepare":
            output = args.output if args.output.is_absolute() else repo / args.output
            prepared = prepare_approved(repo, records, policy)
            write_backup(output, prepared)
            print(
                f"unicode-review prepared={len(prepared)} "
                f"findings={sum(len(item.finding_ids) for item in prepared)} "
                f"backup={unicode_gate.ascii_escape(str(output))}"
            )
            return unicode_gate.EXIT_PASS
        backup = args.backup if args.backup.is_absolute() else repo / args.backup
        changed = apply_approved(repo, records, policy, backup)
        print(f"unicode-review applied={len(changed)}")
        for path in changed:
            print("  " + unicode_gate.ascii_escape(path))
        return unicode_gate.EXIT_PASS
    except (OSError, ValueError, TypeError, UnicodeError, json.JSONDecodeError) as exc:
        print(
            "unicode-review internal failure: " + unicode_gate.ascii_escape(str(exc)),
            file=sys.stderr,
        )
        return unicode_gate.EXIT_GATE_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
