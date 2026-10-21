from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from typing import Iterable, Mapping, Sequence


EXIT_PASS = 0
EXIT_FINDINGS = 1
EXIT_GATE_ERROR = 2

MISSING_RULES = {"NO_FRONTMATTER", "MISSING_KEY", "EMPTY_ID"}


class GateError(Exception):
    pass


@dataclass(frozen=True)
class Policy:
    include_prefixes: tuple[str, ...]
    extensions: tuple[str, ...]
    required_keys: tuple[str, ...]
    id_pattern: re.Pattern[str]


@dataclass(frozen=True)
class Baseline:
    exempt_paths: frozenset[str]
    known_unresolved_related: frozenset[str]


@dataclass(frozen=True)
class Finding:
    rule: str
    path: str
    detail: str


def load_policy(path: pathlib.Path) -> Policy:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        if raw["schema_version"] != 1:
            raise GateError("unsupported policy schema_version")
        return Policy(
            include_prefixes=tuple(raw["include_prefixes"]),
            extensions=tuple(raw["extensions"]),
            required_keys=tuple(raw["required_keys"]),
            id_pattern=re.compile(raw["id_pattern"]),
        )
    except (OSError, ValueError, KeyError, TypeError, re.error) as error:
        raise GateError(f"policy load failed: {error}") from error


def load_baseline(path: pathlib.Path | None) -> Baseline:
    if path is None:
        return Baseline(frozenset(), frozenset())
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return Baseline(
            exempt_paths=frozenset(raw.get("exempt_paths", [])),
            known_unresolved_related=frozenset(raw.get("known_unresolved_related", [])),
        )
    except (OSError, ValueError, AttributeError) as error:
        raise GateError(f"baseline load failed: {error}") from error


def is_target(path: str, policy: Policy) -> bool:
    return path.startswith(policy.include_prefixes) and path.endswith(policy.extensions)


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


def parse_list(value: str) -> list[str]:
    inner = value.strip()
    if inner.startswith("[") and inner.endswith("]"):
        inner = inner[1:-1]
    return [item.strip().strip("\"'") for item in inner.split(",") if item.strip()]


def check_file(
    path: str,
    text: str,
    policy: Policy,
    baseline: Baseline,
) -> tuple[list[Finding], dict[str, str] | None]:
    findings: list[Finding] = []
    frontmatter = parse_frontmatter(text)
    exempt = path in baseline.exempt_paths
    if frontmatter is None:
        if not exempt:
            findings.append(Finding("NO_FRONTMATTER", path, "frontmatter (--- block at line 1) is missing"))
        return findings, None
    for key in policy.required_keys:
        if not frontmatter.get(key):
            rule = "EMPTY_ID" if key == "id" else "MISSING_KEY"
            if not exempt:
                findings.append(Finding(rule, path, f"required key is missing or empty: {key}"))
    identifier = frontmatter.get("id", "")
    if identifier and not policy.id_pattern.fullmatch(identifier):
        findings.append(Finding("BAD_ID_FORMAT", path, f"id does not match {policy.id_pattern.pattern}: {identifier}"))
    return findings, frontmatter


def evaluate(
    changed: Iterable[str],
    contents: Mapping[str, str],
    policy: Policy,
    baseline: Baseline,
) -> list[Finding]:
    """`contents` holds every target file in the head tree; `changed` is the pushed subset."""
    parsed: dict[str, dict[str, str] | None] = {}
    owners: dict[str, list[str]] = {}
    for path, text in contents.items():
        frontmatter = parse_frontmatter(text)
        parsed[path] = frontmatter
        if frontmatter and frontmatter.get("id"):
            owners.setdefault(frontmatter["id"], []).append(path)

    findings: list[Finding] = []
    for path in sorted(set(changed)):
        if path not in contents:
            continue
        file_findings, frontmatter = check_file(path, contents[path], policy, baseline)
        findings.extend(file_findings)
        if not frontmatter:
            continue
        identifier = frontmatter.get("id", "")
        if identifier and len(owners.get(identifier, [])) > 1:
            others = [item for item in owners[identifier] if item != path]
            findings.append(Finding("DUPLICATE_ID", path, f"id {identifier} is also used by: {', '.join(others)}"))
        for reference in parse_list(frontmatter.get("related", "")):
            if reference not in owners and reference not in baseline.known_unresolved_related:
                findings.append(Finding("UNRESOLVED_RELATED", path, f"related id is not defined anywhere: {reference}"))
    return findings


def run_git(repo: pathlib.Path, *arguments: str, stdin: bytes | None = None) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *arguments],
        input=stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", "replace").strip()
        raise GateError(f"git {' '.join(arguments[:2])} failed: {message}")
    return result.stdout


def split_paths(raw: bytes) -> list[str]:
    return [item.decode("utf-8") for item in raw.split(b"\0") if item]


def read_blobs(repo: pathlib.Path, oids: Mapping[str, str]) -> dict[str, str]:
    """Read blobs by object id; `git show rev:path` fails on very long Windows paths."""
    contents: dict[str, str] = {}
    for path, oid in oids.items():
        blob = run_git(repo, "cat-file", "blob", oid)
        try:
            contents[path] = blob.decode("utf-8")
        except UnicodeDecodeError as error:
            raise GateError(f"not valid UTF-8: {path}") from error
    return contents


def collect(repo: pathlib.Path, base: str, head: str, policy: Policy) -> tuple[list[str], dict[str, str]]:
    changed = [
        item
        for item in split_paths(run_git(repo, "diff", "--name-only", "-z", "--diff-filter=AMR", base, head))
        if is_target(item, policy)
    ]
    oids: dict[str, str] = {}
    for entry in run_git(repo, "ls-tree", "-r", "-z", head).split(b"\0"):
        if not entry:
            continue
        meta, _, raw_path = entry.partition(b"\t")
        path = raw_path.decode("utf-8")
        if is_target(path, policy):
            oids[path] = meta.split()[2].decode("ascii")
    return changed, read_blobs(repo, oids)


def write_baseline(repo: pathlib.Path, policy: Policy, destination: pathlib.Path) -> int:
    """Record tracked working-tree files that currently lack required frontmatter."""
    tracked = [item for item in split_paths(run_git(repo, "ls-files", "-z")) if is_target(item, policy)]
    contents: dict[str, str] = {}
    for path in tracked:
        contents[path] = (repo / path).read_text(encoding="utf-8")
    empty = Baseline(frozenset(), frozenset())
    exempt = sorted(
        path
        for path, text in contents.items()
        if any(item.rule in MISSING_RULES for item in check_file(path, text, policy, empty)[0])
    )
    ids = {
        frontmatter["id"]
        for text in contents.values()
        if (frontmatter := parse_frontmatter(text)) and frontmatter.get("id")
    }
    unresolved = sorted(
        {
            reference
            for text in contents.values()
            if (frontmatter := parse_frontmatter(text))
            for reference in parse_list(frontmatter.get("related", ""))
            if reference not in ids
        }
    )
    payload = {
        "schema_version": 1,
        "note": "exempt_paths may lack frontmatter until edited with the owner's permission; remove a path once it has an id.",
        "exempt_paths": exempt,
        "known_unresolved_related": unresolved,
    }
    destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return len(exempt)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check that pushed Markdown records carry a unique frontmatter id.")
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--policy", type=pathlib.Path)
    parser.add_argument("--baseline", type=pathlib.Path)
    parser.add_argument("--base")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--write-baseline", type=pathlib.Path, metavar="PATH")
    arguments = parser.parse_args(argv)
    repo = arguments.repo.resolve()
    policy_path = arguments.policy or repo / "id_gate_policy.json"

    try:
        policy = load_policy(policy_path)
        if arguments.write_baseline:
            count = write_baseline(repo, policy, arguments.write_baseline)
            print(f"ID_GATE: baseline written, {count} path(s) exempt")
            return EXIT_PASS
        if not arguments.base:
            raise GateError("--base is required")
        baseline = load_baseline(arguments.baseline)
        changed, contents = collect(repo, arguments.base, arguments.head, policy)
        findings = evaluate(changed, contents, policy, baseline)
    except GateError as error:
        print(f"ID_GATE: error: {error}", file=sys.stderr)
        return EXIT_GATE_ERROR

    print(f"ID_GATE: checked {len(changed)} changed file(s) of {len(contents)} target file(s)")
    for finding in findings:
        print(json.dumps(asdict(finding)))
    if findings:
        print(f"ID_GATE: FAIL ({len(findings)} finding(s))", file=sys.stderr)
        return EXIT_FINDINGS
    print("ID_GATE: PASS")
    return EXIT_PASS


if __name__ == "__main__":
    sys.exit(main())
