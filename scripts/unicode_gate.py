from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import unicodedata
from dataclasses import asdict, dataclass
from typing import Iterable, Sequence


EXIT_PASS = 0
EXIT_FINDINGS = 1
EXIT_GATE_ERROR = 2

BIDI_CONTROLS = {
    0x061C,
    0x200E,
    0x200F,
    *range(0x202A, 0x202F),
    *range(0x2066, 0x206A),
}
INVISIBLE_FORMATS = {
    0x00AD,
    0x034F,
    0x180E,
    0x200B,
    0x200C,
    0x200D,
    0x2060,
    0x3164,
    0xFEFF,
    0xFFA0,
}
LINE_SEPARATORS = {0x0085, 0x2028, 0x2029}
IDENTIFIER_RE = re.compile(r"[^\W\d]\w*", re.UNICODE)
SEVERITIES = {"warn", "fail"}
REQUIRED_RULES = {
    "BIDI_CONTROL",
    "BOM",
    "CONTROL_CHARACTER",
    "FORMAT_CHARACTER",
    "INVISIBLE_FORMAT",
    "INVALID_UTF8",
    "LINE_SEPARATOR",
    "MIXED_SCRIPT_IDENTIFIER",
    "NONCHARACTER",
    "NON_NFC",
    "OVERSIZED_TEXT",
    "PATH_CONTROL",
    "PATH_MIXED_SCRIPT",
    "PATH_NON_NFC",
    "VARIATION_SELECTOR",
}


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    path: str
    line: int | None
    column: int | None
    codepoint: str | None
    name: str | None
    category: str | None
    bidi_class: str | None
    escaped_context: str | None
    detail: str


@dataclass(frozen=True)
class Policy:
    maximum_text_bytes: int
    normalization_form: str
    allowed_controls: frozenset[int]
    binary_extensions: frozenset[str]
    rules: dict[str, str]

    def severity(self, rule: str) -> str:
        try:
            return self.rules[rule]
        except KeyError as exc:
            raise ValueError(f"policy has no severity for rule {rule}") from exc


@dataclass(frozen=True)
class BaselineEntry:
    id: str
    path: str
    file_sha256: str
    rule: str
    codepoint: str | None
    line: int | None
    column: int | None


def ascii_escape(value: str) -> str:
    return value.encode("unicode_escape", errors="backslashreplace").decode("ascii")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def baseline_entry_id(fields: dict[str, object]) -> str:
    canonical = json.dumps(
        fields, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    return "UGB-" + sha256_bytes(canonical)[:16].upper()


def codepoint_label(value: int) -> str:
    return f"U+{value:04X}"


def parse_codepoint(value: str) -> int:
    if not re.fullmatch(r"U\+[0-9A-Fa-f]{4,6}", value):
        raise ValueError(f"invalid codepoint notation: {value!r}")
    return int(value[2:], 16)


def load_policy(path: pathlib.Path) -> Policy:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("unsupported policy schema_version")
    rules = data.get("rules")
    if not isinstance(rules, dict) or any(value not in SEVERITIES for value in rules.values()):
        raise ValueError("policy rules must map rule names to warn or fail")
    missing_rules = REQUIRED_RULES.difference(rules)
    if missing_rules:
        raise ValueError("policy is missing required rules: " + ",".join(sorted(missing_rules)))
    normalization = data.get("normalization_form")
    if normalization not in {"NFC", "NFD", "NFKC", "NFKD"}:
        raise ValueError("unsupported normalization_form")
    maximum = data.get("maximum_text_bytes")
    if not isinstance(maximum, int) or maximum <= 0:
        raise ValueError("maximum_text_bytes must be a positive integer")
    return Policy(
        maximum_text_bytes=maximum,
        normalization_form=normalization,
        allowed_controls=frozenset(
            parse_codepoint(item) for item in data.get("allowed_control_codepoints", [])
        ),
        binary_extensions=frozenset(
            str(item).lower() for item in data.get("binary_extensions", [])
        ),
        rules={str(key): str(value) for key, value in rules.items()},
    )


def load_baseline(path: pathlib.Path) -> tuple[BaselineEntry, ...]:
    data = json.loads(path.read_text(encoding="ascii"))
    if data.get("schema_version") != 1:
        raise ValueError("unsupported baseline schema_version")
    raw_entries = data.get("entries")
    if not isinstance(raw_entries, list):
        raise ValueError("baseline entries must be a list")
    entries: list[BaselineEntry] = []
    ids: set[str] = set()
    for raw in raw_entries:
        if not isinstance(raw, dict):
            raise ValueError("baseline entry must be an object")
        fields = {
            key: raw.get(key)
            for key in ("path", "file_sha256", "rule", "codepoint", "line", "column")
        }
        expected = baseline_entry_id(fields)
        if raw.get("id") != expected:
            raise ValueError(f"invalid baseline entry id: {raw.get('id')}")
        if expected in ids:
            raise ValueError(f"duplicate baseline entry id: {expected}")
        if not isinstance(fields["path"], str):
            raise ValueError(f"invalid baseline path: {expected}")
        if not isinstance(fields["file_sha256"], str) or not re.fullmatch(
            r"[0-9a-f]{64}", fields["file_sha256"]
        ):
            raise ValueError(f"invalid baseline file hash: {expected}")
        approved_scope = {
            ("VARIATION_SELECTOR", "U+FE0F"),
            ("BOM", "U+FEFF"),
            ("INVISIBLE_FORMAT", "U+200D"),
        }
        if (fields["rule"], fields["codepoint"]) not in approved_scope:
            raise ValueError(f"baseline entry is outside approved scope: {expected}")
        if not isinstance(fields["line"], int) or not isinstance(fields["column"], int):
            raise ValueError(f"baseline entry requires line and column: {expected}")
        ids.add(expected)
        entries.append(BaselineEntry(id=expected, **fields))
    return tuple(entries)


def apply_baseline(
    path: str,
    raw: bytes,
    findings: Sequence[Finding],
    entries: Sequence[BaselineEntry],
) -> tuple[list[Finding], list[str]]:
    file_hash = sha256_bytes(raw)
    entry_map = {
        (entry.path, entry.file_sha256, entry.rule, entry.codepoint, entry.line, entry.column): entry.id
        for entry in entries
    }
    active: list[Finding] = []
    matched: list[str] = []
    for finding in findings:
        key = (
            path,
            file_hash,
            finding.rule,
            finding.codepoint,
            finding.line,
            finding.column,
        )
        entry_id = entry_map.get(key)
        if entry_id is None:
            active.append(finding)
        else:
            matched.append(entry_id)
    return active, matched


def character_name(character: str) -> str:
    return unicodedata.name(character, "UNNAMED")


def is_noncharacter(value: int) -> bool:
    return 0xFDD0 <= value <= 0xFDEF or (value & 0xFFFF) in {0xFFFE, 0xFFFF}


def is_variation_selector(value: int) -> bool:
    return 0xFE00 <= value <= 0xFE0F or 0xE0100 <= value <= 0xE01EF


def script_of(character: str) -> str | None:
    name = character_name(character)
    for script in ("LATIN", "CYRILLIC", "GREEK", "HEBREW", "ARABIC"):
        if script in name:
            return script
    return None


def risky_scripts(text: str) -> set[str]:
    scripts = {script for character in text if (script := script_of(character))}
    # Greek symbols are intentionally common in NRA-IDE formulas and units.
    # Until UTS #39 skeleton data is pinned, keep this heuristic narrowly
    # focused on the high-signal Latin/Cyrillic mixture.
    if {"LATIN", "CYRILLIC"}.issubset(scripts):
        return scripts
    return set()


def location(text: str, index: int) -> tuple[int, int, str]:
    line = text.count("\n", 0, index) + 1
    line_start = text.rfind("\n", 0, index) + 1
    line_end = text.find("\n", index)
    if line_end < 0:
        line_end = len(text)
    column = index - line_start + 1
    context_start = max(line_start, index - 20)
    context_end = min(line_end, index + 21)
    return line, column, ascii_escape(text[context_start:context_end])


def make_character_finding(
    rule: str, path: str, text: str, index: int, policy: Policy, detail: str
) -> Finding:
    character = text[index]
    value = ord(character)
    line, column, context = location(text, index)
    return Finding(
        rule=rule,
        severity=policy.severity(rule),
        path=ascii_escape(path),
        line=line,
        column=column,
        codepoint=codepoint_label(value),
        name=character_name(character),
        category=unicodedata.category(character),
        bidi_class=unicodedata.bidirectional(character) or None,
        escaped_context=context,
        detail=detail,
    )


def scan_path(path: str, policy: Policy) -> list[Finding]:
    findings: list[Finding] = []
    escaped = ascii_escape(path)
    if unicodedata.normalize(policy.normalization_form, path) != path:
        findings.append(Finding(
            "PATH_NON_NFC", policy.severity("PATH_NON_NFC"), escaped,
            None, None, None, None, None, None, None,
            f"path is not {policy.normalization_form}",
        ))
    for component in re.split(r"[\\/]", path):
        for match in IDENTIFIER_RE.finditer(component):
            scripts = risky_scripts(match.group(0))
            if scripts:
                findings.append(Finding(
                    "PATH_MIXED_SCRIPT", policy.severity("PATH_MIXED_SCRIPT"), escaped,
                    None, None, None, None, None, None, None,
                    "risky scripts in path token: " + ",".join(sorted(scripts)),
                ))
    for character in path:
        value = ord(character)
        if value in BIDI_CONTROLS or (
            unicodedata.category(character) in {"Cc", "Cf"} and value not in policy.allowed_controls
        ):
            findings.append(Finding(
                "PATH_CONTROL", policy.severity("PATH_CONTROL"), escaped,
                None, None, codepoint_label(value), character_name(character),
                unicodedata.category(character), unicodedata.bidirectional(character) or None,
                None, "control or format character in path",
            ))
    return findings


def scan_text(path: str, text: str, policy: Policy) -> list[Finding]:
    findings: list[Finding] = []
    if text.startswith("\ufeff"):
        findings.append(make_character_finding("BOM", path, text, 0, policy, "UTF-8 BOM"))
    if unicodedata.normalize(policy.normalization_form, text) != text:
        findings.append(Finding(
            "NON_NFC", policy.severity("NON_NFC"), ascii_escape(path),
            None, None, None, None, None, None, None,
            f"content is not {policy.normalization_form}",
        ))
    for index, character in enumerate(text):
        value = ord(character)
        if value == 0xFEFF and index == 0:
            continue
        if value in BIDI_CONTROLS:
            rule, detail = "BIDI_CONTROL", "Unicode bidirectional control"
        elif value in LINE_SEPARATORS:
            rule, detail = "LINE_SEPARATOR", "non-ASCII line separator"
        elif is_noncharacter(value):
            rule, detail = "NONCHARACTER", "Unicode noncharacter"
        elif is_variation_selector(value):
            rule, detail = "VARIATION_SELECTOR", "Unicode variation selector"
        elif value in INVISIBLE_FORMATS:
            rule, detail = "INVISIBLE_FORMAT", "invisible or zero-width character"
        elif unicodedata.category(character) == "Cc" and value not in policy.allowed_controls:
            rule, detail = "CONTROL_CHARACTER", "disallowed control character"
        elif unicodedata.category(character) == "Cf":
            rule, detail = "FORMAT_CHARACTER", "Unicode format character"
        else:
            continue
        findings.append(make_character_finding(rule, path, text, index, policy, detail))
    for match in IDENTIFIER_RE.finditer(text):
        scripts = risky_scripts(match.group(0))
        if not scripts:
            continue
        line, column, context = location(text, match.start())
        findings.append(Finding(
            "MIXED_SCRIPT_IDENTIFIER", policy.severity("MIXED_SCRIPT_IDENTIFIER"),
            ascii_escape(path), line, column, None, None, None, None, context,
            "risky scripts in identifier: " + ",".join(sorted(scripts)),
        ))
    return findings


def scan_bytes(path: str, raw: bytes, policy: Policy) -> list[Finding]:
    findings = scan_path(path, policy)
    if pathlib.PurePosixPath(path.replace("\\", "/")).suffix.lower() in policy.binary_extensions:
        return findings
    if len(raw) > policy.maximum_text_bytes:
        findings.append(Finding(
            "OVERSIZED_TEXT", policy.severity("OVERSIZED_TEXT"), ascii_escape(path),
            None, None, None, None, None, None, None,
            f"text candidate has {len(raw)} bytes; limit is {policy.maximum_text_bytes}",
        ))
        return findings
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        findings.append(Finding(
            "INVALID_UTF8", policy.severity("INVALID_UTF8"), ascii_escape(path),
            None, None, None, None, None, None, None,
            f"UTF-8 decode failed at byte {exc.start}: {ascii_escape(exc.reason)}",
        ))
        return findings
    findings.extend(scan_text(path, text, policy))
    return findings


def git_output(repo: pathlib.Path, arguments: Sequence[str]) -> bytes:
    return subprocess.check_output(["git", *arguments], cwd=repo, stderr=subprocess.PIPE)


def decode_git_paths(raw: bytes) -> list[str]:
    return [part.decode("utf-8") for part in raw.split(b"\0") if part]


def tracked_worktree_inputs(repo: pathlib.Path) -> Iterable[tuple[str, bytes]]:
    for path in decode_git_paths(git_output(repo, ["ls-files", "-z"])):
        candidate = repo / pathlib.PurePosixPath(path)
        resolved = candidate.resolve()
        if repo != resolved and repo not in resolved.parents:
            raise OSError(f"tracked path resolves outside repository: {ascii_escape(path)}")
        yield path, candidate.read_bytes()


def staged_inputs(repo: pathlib.Path) -> Iterable[tuple[str, bytes]]:
    paths = decode_git_paths(git_output(
        repo, ["diff", "--cached", "--name-only", "-z", "--diff-filter=ACMR"]
    ))
    for path in paths:
        yield path, git_output(repo, ["show", f":{path}"])


def explicit_inputs(repo: pathlib.Path, paths: Sequence[str]) -> Iterable[tuple[str, bytes]]:
    for supplied in paths:
        candidate = (repo / supplied).resolve()
        if repo != candidate and repo not in candidate.parents:
            raise OSError(f"path resolves outside repository: {ascii_escape(supplied)}")
        if not candidate.is_file():
            raise OSError(f"not a regular file: {ascii_escape(supplied)}")
        yield candidate.relative_to(repo).as_posix(), candidate.read_bytes()


def directory_inputs(repo: pathlib.Path, supplied: str) -> Iterable[tuple[str, bytes]]:
    directory = (repo / supplied).resolve()
    if repo != directory and repo not in directory.parents:
        raise OSError(f"directory resolves outside repository: {ascii_escape(supplied)}")
    if not directory.is_dir():
        raise OSError(f"not a directory: {ascii_escape(supplied)}")
    for candidate in sorted(directory.rglob("*")):
        if candidate.is_symlink():
            raise OSError(
                "symbolic link is not permitted in scan directory: "
                + ascii_escape(candidate.relative_to(repo).as_posix())
            )
        if candidate.is_file():
            resolved = candidate.resolve()
            if repo != resolved and repo not in resolved.parents:
                raise OSError(
                    "scan file resolves outside repository: "
                    + ascii_escape(candidate.relative_to(repo).as_posix())
                )
            yield candidate.relative_to(repo).as_posix(), candidate.read_bytes()


def render_text(findings: Sequence[Finding], scanned: int, baselined: int = 0) -> str:
    failed = sum(item.severity == "fail" for item in findings)
    warned = sum(item.severity == "warn" for item in findings)
    lines = [
        f"unicode-gate scanned={scanned} fail={failed} warn={warned} baselined={baselined}"
    ]
    for item in findings:
        position = ""
        if item.line is not None:
            position = f":{item.line}:{item.column}"
        codepoint = f" {item.codepoint} {item.name}" if item.codepoint else ""
        lines.append(
            f"{item.severity.upper()} {item.rule} {item.path}{position}{codepoint} - {item.detail}"
        )
        if item.escaped_context is not None:
            lines.append(f"  context={item.escaped_context}")
    return "\n".join(lines)


def render_json(
    findings: Sequence[Finding], scanned: int, baseline_ids: Sequence[str] = ()
) -> str:
    payload = {
        "schema_version": 1,
        "unicode_database_version": unicodedata.unidata_version,
        "scanned_files": scanned,
        "baselined_findings": len(baseline_ids),
        "baseline_ids": sorted(baseline_ids),
        "status": "FAIL" if any(item.severity == "fail" for item in findings) else "PASS",
        "findings": [asdict(item) for item in findings],
    }
    return json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Deterministic Unicode boundary gate")
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--all", action="store_true", help="scan tracked working-tree files")
    scope.add_argument("--staged", action="store_true", help="scan added and modified index blobs")
    scope.add_argument("--paths", nargs="+", metavar="PATH", help="scan explicit repository paths")
    scope.add_argument("--directory", metavar="PATH", help="recursively scan one repository directory")
    parser.add_argument("--json", action="store_true", help="emit ASCII-only JSON")
    parser.add_argument("--policy", type=pathlib.Path, help="policy JSON path")
    parser.add_argument("--baseline", type=pathlib.Path, help="exact reviewed baseline JSON")
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        repo = args.repo.resolve()
        policy_path = (args.policy or repo / "unicode_gate_policy.json").resolve()
        policy = load_policy(policy_path)
        baseline = load_baseline(args.baseline.resolve()) if args.baseline else ()
        if args.all:
            inputs = tracked_worktree_inputs(repo)
        elif args.staged:
            inputs = staged_inputs(repo)
        elif args.directory:
            inputs = directory_inputs(repo, args.directory)
        else:
            inputs = explicit_inputs(repo, args.paths)
        findings: list[Finding] = []
        baseline_ids: list[str] = []
        scanned = 0
        for path, raw in inputs:
            scanned += 1
            active, matched = apply_baseline(path, raw, scan_bytes(path, raw, policy), baseline)
            findings.extend(active)
            baseline_ids.extend(matched)
        findings.sort(key=lambda item: (
            item.path, item.line or 0, item.column or 0, item.rule, item.codepoint or ""
        ))
    except (OSError, ValueError, json.JSONDecodeError, subprocess.SubprocessError, UnicodeError) as exc:
        message = f"unicode-gate internal failure: {ascii_escape(str(exc))}"
        print(message, file=sys.stderr)
        return EXIT_GATE_ERROR
    print(
        render_json(findings, scanned, baseline_ids)
        if args.json
        else render_text(findings, scanned, len(baseline_ids))
    )
    return EXIT_FINDINGS if any(item.severity == "fail" for item in findings) else EXIT_PASS


if __name__ == "__main__":
    raise SystemExit(main())
