"""Request/receipt inspection; no approval issuer or execution authority.

Trusted observations, authentication and atomic consumption must live outside
the AI process. Passing callbacks here does not create that boundary.
"""
from __future__ import annotations
import copy
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import stat
from git_manifest import ManifestError, digest, identifier, timestamp, validate_git_snapshot

def canonical_json(value):
    try:
        return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii')
    except (ValueError, TypeError, RecursionError):
        raise ManifestError('INVALID_JSON_VALUE') from None

def manifest_hash(value):
    return hashlib.sha256(canonical_json(value)).hexdigest()

def _absolute(value):
    if not isinstance(value, str) or not value or '\x00' in value or not os.path.isabs(value):
        raise ManifestError('INVALID_ABSOLUTE_PATH')
    if os.path.normcase(os.path.abspath(value)) != value:
        raise ManifestError('NON_CANONICAL_PATH')
    return value

def snapshot_file(path):
    """Pin lexical/resolved paths and content of a regular or absent file.

    Directories and leaf symlinks are unsupported. This is not atomic with any
    subsequent write; a broker must recheck and mediate actual execution.
    """
    lexical = os.path.normcase(os.path.abspath(os.fspath(path)))
    resolved = os.path.normcase(os.path.realpath(lexical))
    try:
        before = os.lstat(lexical)
    except FileNotFoundError:
        return {'path': lexical, 'realpath': resolved, 'exists': False, 'sha256': None, 'identity': None}
    if not stat.S_ISREG(before.st_mode):
        raise ManifestError('TARGET_IS_NOT_REGULAR_FILE')
    with open(lexical, 'rb') as stream:
        opened = os.fstat(stream.fileno())
        sha = hashlib.file_digest(stream, 'sha256').hexdigest()
        after_open = os.fstat(stream.fileno())
    after_path = os.lstat(lexical)
    def identity(info):
        return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns)
    # Windows lstat/fstat may expose different ctime meanings; compare within each API.
    if (before.st_ctime_ns != after_path.st_ctime_ns or opened.st_ctime_ns != after_open.st_ctime_ns
            or not (identity(before) == identity(opened) == identity(after_open) == identity(after_path))) or resolved != os.path.normcase(os.path.realpath(lexical)):
        raise ManifestError('TARGET_CHANGED_DURING_READ')
    return {'path': lexical, 'realpath': resolved, 'exists': True, 'sha256': sha, 'identity': {'device': after_path.st_dev, 'inode': after_path.st_ino}}

FIELDS = frozenset({'schema_version', 'request_id', 'session_id', 'repo_realpath', 'agents_sha256',
                    'operation', 'impact', 'plan_sha256', 'created_at', 'expires_at', 'targets', 'git'})

def validate_manifest(value, *, now, max_fetch_age=300):
    if not isinstance(value, dict) or set(value) != FIELDS or type(value['schema_version']) is not int or value['schema_version'] != 1:
        raise ManifestError('INVALID_MANIFEST_FIELDS')
    for key in ('request_id', 'session_id'):
        identifier(value[key])
    _absolute(value['repo_realpath'])
    for key in ('agents_sha256', 'plan_sha256'):
        digest(value[key])
    if not isinstance(value['impact'], str) or not value['impact'].strip():
        raise ManifestError('MISSING_IMPACT')
    created, expires, current = timestamp(value['created_at']), timestamp(value['expires_at']), timestamp(now)
    if not created <= current < expires:
        raise ManifestError('REQUEST_NOT_CURRENT')
    targets = value['targets']
    if not isinstance(targets, list):
        raise ManifestError('INVALID_TARGET_LIST')
    paths = set()
    for target in targets:
        if not isinstance(target, dict) or set(target) != {'path', 'realpath', 'exists', 'sha256', 'identity'}:
            raise ManifestError('INVALID_TARGET_FIELDS')
        path = _absolute(target['path'])
        _absolute(target['realpath'])
        if path in paths:
            raise ManifestError('DUPLICATE_TARGET')
        paths.add(path)
        if type(target['exists']) is not bool:
            raise ManifestError('INVALID_TARGET_STATE')
        if target['exists']:
            digest(target['sha256'])
            identity = target['identity']
            if (not isinstance(identity, dict) or set(identity) != {'device', 'inode'}
                    or any(type(v) is not int or v < 0 for v in identity.values())):
                raise ManifestError('INVALID_FILE_IDENTITY')
        elif target['sha256'] is not None or target['identity'] is not None:
            raise ManifestError('INVALID_TARGET_STATE')
    if value['operation'] == 'file_change':
        if not targets or value['git'] is not None:
            raise ManifestError('INVALID_FILE_REQUEST')
    elif value['operation'] == 'git_push':
        if targets:
            raise ManifestError('INVALID_GIT_REQUEST')
        validate_git_snapshot(value['git'], now=current, max_fetch_age=max_fetch_age)
    else:
        raise ManifestError('UNSUPPORTED_OPERATION')
    canonical_json(value)
    return copy.deepcopy(value)

def observe_files(approved, *, now):
    """Read contract and file paths anew; Git requires a separate collector."""
    result = validate_manifest(approved, now=now)
    if result['operation'] != 'file_change':
        raise ManifestError('GIT_COLLECTOR_REQUIRED')
    root = result['repo_realpath']
    result['repo_realpath'] = os.path.normcase(os.path.realpath(root))
    result['agents_sha256'] = snapshot_file(Path(root) / 'AGENTS.md')['sha256']
    result['targets'] = [snapshot_file(item['path']) for item in result['targets']]
    return result

@dataclass(frozen=True)
class CheckResult:
    valid: bool
    reason: str

RECEIPT_FIELDS = frozenset({'approval_id', 'request_id', 'session_id', 'manifest_sha256', 'issued_at', 'expires_at'})

def check_request(approved, current, receipt, *, now, verify_receipt=None, consume_once=None, max_fetch_age=300):
    """Exact state + authenticated claims + protected atomic one-time consume.

    Both callbacks are mandatory future broker interfaces, not implemented trust.
    Passing a JSON 'approved' flag alone never passes. True means component checks
    passed, not permission to execute an operation.
    """
    try:
        left = validate_manifest(approved, now=now, max_fetch_age=max_fetch_age)
        right = validate_manifest(current, now=now, max_fetch_age=max_fetch_age)
        bound_hash = manifest_hash(left)
        if canonical_json(left) != canonical_json(right):
            raise ManifestError('MANIFEST_CHANGED')
        if not callable(verify_receipt) or not callable(consume_once):
            raise ManifestError('TRUSTED_APPROVAL_BACKEND_REQUIRED')
        try:
            claims = verify_receipt(receipt)
        except Exception:
            raise ManifestError('APPROVAL_BACKEND_FAILURE') from None
        if not isinstance(claims, dict) or set(claims) != RECEIPT_FIELDS:
            raise ManifestError('UNVERIFIED_RECEIPT')
        identifier(claims['approval_id'])
        if claims['request_id'] != left['request_id'] or claims['session_id'] != left['session_id'] or claims['manifest_sha256'] != bound_hash:
            raise ManifestError('RECEIPT_BINDING_MISMATCH')
        issued, expires, clock = timestamp(claims['issued_at']), timestamp(claims['expires_at']), timestamp(now)
        if not left['created_at'] <= issued <= clock < expires <= left['expires_at']:
            raise ManifestError('RECEIPT_NOT_CURRENT')
        try:
            consumed = consume_once(claims['approval_id'], bound_hash)
        except Exception:
            raise ManifestError('APPROVAL_BACKEND_FAILURE') from None
        if consumed is not True:
            raise ManifestError('RECEIPT_ALREADY_USED_OR_UNAVAILABLE')
        return CheckResult(True, 'CHECKS_PASSED_NOT_EXECUTION_AUTHORITY')
    except ManifestError as exc:
        return CheckResult(False, str(exc))
    except Exception:
        return CheckResult(False, 'VALIDATION_OR_BACKEND_FAILURE')
