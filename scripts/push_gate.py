"""Reviewed-target checks for pre-push. A plan is data, never human approval.

No fetch, commit, push, broker callback, or approval issuance is performed here.
The caller still follows AGENTS.md's fresh-fetch and final-approval procedure.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid
import unicodedata

RULE_FILES = ("AGENTS.md", ".githooks/pre-push", "scripts/push_gate.py",
              "scripts/malware_gate.py", "scripts/malware_gate.ps1", "scripts/unicode_gate.py",
              "scripts/id_gate.py", "scripts/check_dictionary.py", "unicode_gate_policy.json",
              "unicode_gate_baseline.json", "id_gate_policy.json", "id_gate_baseline.json")
GATES = ("unicode", "malware", "id", "dictionary")
ACCEPTED = {"PASS", "WARN", "NOT_APPLICABLE"}


class GateError(ValueError):
    pass


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def git(repo, *args, absent=False):
    # Never echo raw Git arguments/stderr: remote URLs may contain credentials.
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, timeout=30)
    if result.returncode:
        if absent and result.returncode == 1:
            return b""
        raise GateError("GIT_OBSERVATION_FAILED")
    return result.stdout


def inside(repo, path):
    path = Path(path)
    if not path.is_absolute():
        path = repo / path
    resolved = path.resolve()
    if repo not in resolved.parents or path.is_symlink():
        raise GateError("PATH_OUTSIDE_REPOSITORY_OR_LINK")
    return resolved


def oid(repo, ref):
    value = git(repo, "rev-parse", "--verify", ref + "^{commit}").strip().decode("ascii")
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", value):
        raise GateError("INVALID_COMMIT_OID")
    return value


def event(repo, remote, text):
    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) != 1:
        raise GateError("SINGLE_REF_REQUIRED")
    fields = lines[0].split()
    if len(fields) != 4:
        raise GateError("MALFORMED_PRE_PUSH_INPUT")
    local_ref, source, target, old = fields
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", source) or not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", old):
        raise GateError("INVALID_UPDATE_OID")
    if set(source) == {"0"}:
        raise GateError("remote ref deletion is blocked")
    if not target.startswith("refs/heads/"):
        raise GateError("new non-branch refs or non-branch updates are blocked")
    git(repo, "check-ref-format", target)
    if source != oid(repo, "HEAD"):
        raise GateError("SOURCE_MUST_EQUAL_HEAD")
    if set(old) != {"0"}:
        result = subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", old, source], capture_output=True, timeout=30)
        if result.returncode:
            raise GateError("non-fast-forward or unresolved remote base")
    else:
        try:
            git(repo, "symbolic-ref", "--quiet", f"refs/remotes/{remote}/HEAD")
        except GateError:
            raise GateError("new branch requires a fetched remote default branch") from None
    return local_ref, source, target, old


def context(repo, remote, target, timeout_seconds):
    if type(timeout_seconds) not in (int, float) or not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
        raise GateError("EXPLICIT_POSITIVE_TIMEOUT_REQUIRED")
    if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", remote):
        raise GateError("NAMED_REMOTE_REQUIRED")
    if not target.startswith("refs/heads/"):
        raise GateError("BRANCH_TARGET_REQUIRED")
    git(repo, "check-ref-format", target)
    if Path(git(repo, "rev-parse", "--show-toplevel").decode().strip()).resolve() != repo:
        raise GateError("REPOSITORY_ROOT_REQUIRED")
    urls = git(repo, "remote", "get-url", "--push", "--all", remote).splitlines()
    if len(urls) != 1 or not urls[0]:
        raise GateError("SINGLE_DESTINATION_REQUIRED")
    head = oid(repo, "HEAD")
    tracked = f"refs/remotes/{remote}/{target[len('refs/heads/'):]}"
    old = git(repo, "rev-parse", "--verify", "--quiet", tracked, absent=True).strip().decode("ascii")
    default = None
    if old:
        base = oid(repo, tracked)
    else:
        default_ref = git(repo, "symbolic-ref", "--quiet", f"refs/remotes/{remote}/HEAD").decode().strip()
        default = oid(repo, default_ref)
        base = git(repo, "merge-base", default, head).decode().strip()
    incoming = git(repo, "rev-list", f"{head}..{old or default}").splitlines()
    if incoming:
        raise GateError("INCOMING_COMMITS_PRESENT")
    outgoing = git(repo, "rev-list", "--reverse", f"{base}..{head}").decode().splitlines()
    fetch_path = inside(repo, git(repo, "rev-parse", "--git-path", "FETCH_HEAD").decode().strip())
    fetch_raw = fetch_path.read_bytes()
    fetched_oids = {line.split(b"\t", 1)[0].decode("ascii") for line in fetch_raw.splitlines() if line}
    if (old or default) not in fetched_oids:
        raise GateError("FETCH_EVIDENCE_MISSING")
    rules = {}
    for name in RULE_FILES:
        path = inside(repo, name)
        rules[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(schema_version=1, repo=str(repo), remote=remote,
                destination_sha256=hashlib.sha256(urls[0]).hexdigest(),
                remote_ref=target, head_oid=head, source_oid=head, remote_oid=old or "0" * len(head),
                base_oid=base, default_oid=default, outgoing=outgoing,
                fetch_sha256=hashlib.sha256(fetch_raw).hexdigest(), fetched_at_ns=fetch_path.stat().st_mtime_ns,
                rules=rules, timeout_seconds=timeout_seconds,
                python_executable=sys.executable, python_version=sys.version,
                unicode_database_version=unicodedata.unidata_version)


def prepare(repo, remote, target, output, timeout_seconds):
    ctx = context(repo, remote, target, timeout_seconds)
    plan = {"plan_id": digest(ctx), "context": ctx, "is_execution_permission": False}
    path = inside(repo, output)
    path.parent.mkdir(parents=True, exist_ok=True)
    # A reviewed plan is not silently overwritten by a later preparation.
    with path.open("x", encoding="ascii", newline="\n") as handle:
        json.dump(plan, handle, ensure_ascii=True, indent=2, allow_nan=False)
        handle.write("\n")
    return plan


def load_plan(repo, path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise GateError("DUPLICATE_JSON_KEY")
            result[key] = value
        return result
    plan = json.loads(inside(repo, path).read_text(encoding="ascii"), object_pairs_hook=pairs)
    if set(plan) != {"plan_id", "context", "is_execution_permission"} or plan["is_execution_permission"] is not False:
        raise GateError("INVALID_PLAN_SCHEMA")
    if plan["plan_id"] != digest(plan["context"]):
        raise GateError("PLAN_DIGEST_MISMATCH")
    return plan


def unchanged(repo, plan):
    ctx = plan["context"]
    current = context(repo, ctx["remote"], ctx["remote_ref"], ctx["timeout_seconds"])
    if current != ctx:
        raise GateError("PLAN_OR_RULES_CHANGED")


def command(repo, args, timeout):
    try:
        return subprocess.run(args, cwd=repo, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise GateError("GATE_TIMEOUT; task output may require cleanup") from None


def payload_result(result, expected_head, expected_base=None):
    data = json.loads(result.stdout.decode("utf-8-sig"))
    if data.get("schema_version") != 1 or data.get("head") != expected_head:
        raise GateError("INVALID_GATE_RESULT_CONTEXT")
    if expected_base is not None and data.get("base") != expected_base:
        raise GateError("INVALID_GATE_RESULT_BASE")
    status = data.get("status")
    if type(data.get("scanned_files")) is not int or data["scanned_files"] < 0:
        raise GateError("INVALID_GATE_COVERAGE")
    findings = data.get("findings")
    if not isinstance(findings, list) or status not in {"PASS", "FAIL", "UNAVAILABLE"}:
        raise GateError("INVALID_GATE_RESULT")
    if (result.returncode == 0 and (status != "PASS" or findings)) or (result.returncode == 1 and (status != "FAIL" or not findings)) or result.returncode not in (0, 1):
        raise GateError("GATE_EXIT_RESULT_MISMATCH")
    if data["scanned_files"] == 0 and status == "PASS":
        data["status"] = "NOT_APPLICABLE"
        data["reason"] = "NO_TARGETS_IN_COMMIT"
    return data


def check(repo, remote, remote_url, text, plan_path):
    results = {name: {"status": "NOT_RUN", "scanned_files": 0} for name in GATES}
    report = {"schema_version": 1, "status": "UNAVAILABLE", "results": results,
              "is_execution_permission": False}
    run_dir = None
    try:
        if not text.strip():
            report.update(status="NOT_APPLICABLE", reason="NO_REF_UPDATES")
            return report
        _, source, target, old = event(repo, remote, text)
        if not plan_path:
            raise GateError("PLAN_REQUIRED")
        plan = load_plan(repo, plan_path)
        ctx = plan["context"]
        if (remote, target, source, old) != (ctx["remote"], ctx["remote_ref"], ctx["source_oid"], ctx["remote_oid"]):
            raise GateError("UPDATE_DIFFERS_FROM_PLAN")
        if hashlib.sha256(remote_url.encode()).hexdigest() != ctx["destination_sha256"]:
            raise GateError("DESTINATION_DIFFERS_FROM_PLAN")
        unchanged(repo, plan)
        report.update(plan_id=plan["plan_id"], remote=remote, remote_ref=target, head=source, base=ctx["base_oid"])
        run_dir = inside(repo, "local_reports/push_gate/" + uuid.uuid4().hex)
        run_dir.mkdir(parents=True)
        receipt = run_dir / "malware_unicode.json"
        result = command(repo, ["pwsh", "-NoProfile", "-File", "scripts/malware_gate.ps1",
                               "-Repository", str(repo), "-Base", ctx["base_oid"], "-Head", source,
                               "-ResultPath", str(receipt)], ctx["timeout_seconds"])
        data = json.loads(receipt.read_text(encoding="utf-8-sig"))
        if data.get("schema_version") != 1 or data.get("head") != source or data.get("base") != ctx["base_oid"] or data.get("exit_code") != result.returncode:
            raise GateError("INVALID_MALWARE_RECEIPT")
        for name in ("unicode", "malware"):
            item = data[name]
            if item.get("status") not in ACCEPTED | {"FAIL", "UNAVAILABLE", "NOT_RUN"} or type(item.get("scanned_files")) is not int or item["scanned_files"] < 0:
                raise GateError("INVALID_MALWARE_COVERAGE")
            if item["status"] == "NOT_APPLICABLE" and item["scanned_files"] != 0:
                raise GateError("INVALID_EMPTY_SCOPE")
            if item["status"] in ACCEPTED:
                if type(item.get("expected_files")) is not int or item["expected_files"] != item["scanned_files"]:
                    raise GateError("INCOMPLETE_GATE_COVERAGE")
                if item["status"] in {"PASS", "WARN"} and item["scanned_files"] == 0:
                    raise GateError("ZERO_SCAN_REQUIRES_EXPLICIT_EMPTY_SCOPE")
            results[name] = item
        if result.returncode != 0 or any(results[g]["status"] not in ACCEPTED for g in ("unicode", "malware")):
            raise GateError("MALWARE_OR_UNICODE_BLOCKED")
        unchanged(repo, plan)
        commands = {
            "id": [sys.executable, "-B", "scripts/id_gate.py", "--repo", str(repo), "--base", ctx["base_oid"], "--head", source, "--policy", "id_gate_policy.json", "--baseline", "id_gate_baseline.json", "--json"],
            "dictionary": [sys.executable, "-B", "scripts/check_dictionary.py", "--repo", str(repo), "--head", source, "--json"],
        }
        for name, args in commands.items():
            result = command(repo, args, ctx["timeout_seconds"])
            results[name] = payload_result(result, source, ctx["base_oid"] if name == "id" else None)
            unchanged(repo, plan)
            if results[name]["status"] not in ACCEPTED:
                raise GateError(name.upper() + "_BLOCKED")
        unchanged(repo, plan)
        report["status"] = "WARN" if any(r["status"] == "WARN" for r in results.values()) else "PASS"
    except (GateError, OSError, ValueError, TypeError, KeyError, subprocess.SubprocessError, KeyboardInterrupt) as exc:
        # Exceptions never include subprocess output, URLs or source content.
        report["reason"] = str(exc) if isinstance(exc, GateError) else "INTERRUPTED" if isinstance(exc, KeyboardInterrupt) else "GATE_INPUT_OR_EXECUTION_ERROR"
        if any(r["status"] == "FAIL" for r in results.values()):
            report["status"] = "FAIL"
    if run_dir:
        (run_dir / "result.json").write_text(json.dumps(report, ensure_ascii=True, indent=2) + "\n", encoding="ascii")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--repo", type=Path, default=Path.cwd())
    p.add_argument("--remote", required=True)
    p.add_argument("--branch", required=True, help="full refs/heads/... target")
    p.add_argument("--output", required=True)
    p.add_argument("--timeout-seconds", type=float, required=True, help="explicit trial limit; calibrate before production")
    p = sub.add_parser("check")
    p.add_argument("remote")
    p.add_argument("remote_url")
    p.add_argument("--repo", type=Path, default=Path.cwd())
    p.add_argument("--plan", default=os.environ.get("NRA_PUSH_PLAN"))
    args = parser.parse_args(argv)
    try:
        repo = args.repo.resolve()
        if args.action == "prepare":
            data = prepare(repo, args.remote, args.branch, args.output, args.timeout_seconds)
            code = 0
        else:
            data = check(repo, args.remote, args.remote_url, sys.stdin.read(), args.plan)
            code = 0 if data["status"] in ACCEPTED else 1 if data["status"] == "FAIL" else 2
    except (GateError, OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError):
        data, code = {"schema_version": 1, "status": "UNAVAILABLE", "reason": "PREPARATION_FAILED"}, 2
    print(json.dumps(data, ensure_ascii=True, indent=2, allow_nan=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
