"""Pure Git snapshot checks. No commands, fetch, push, or approval issuance."""
from __future__ import annotations
import copy
import math
import re
from urllib.parse import urlsplit

class ManifestError(ValueError):
    """Fixed codes only; never include supplied URLs or secret-bearing values."""

def timestamp(value):
    if type(value) not in (int, float) or value < 0:
        raise ManifestError('INVALID_TIMESTAMP')
    try:
        if not math.isfinite(value):
            raise ValueError()
        return float(value)
    except (ValueError, OverflowError):
        raise ManifestError('INVALID_TIMESTAMP') from None

def identifier(value):
    if not isinstance(value, str) or re.fullmatch(r'[A-Za-z0-9_-]{1,200}', value) is None:
        raise ManifestError('INVALID_IDENTIFIER')
    return value

def digest(value):
    if not isinstance(value, str) or re.fullmatch(r'[0-9a-f]{64}', value) is None:
        raise ManifestError('INVALID_DIGEST')
    return value

def oid(value):
    if not isinstance(value, str) or re.fullmatch(r'(?:[0-9a-f]{40}|[0-9a-f]{64})', value) is None or set(value) == {'0'}:
        raise ManifestError('INVALID_OID')
    return value

def branch_ref(value):
    if not isinstance(value, str) or not value.startswith('refs/heads/'):
        raise ManifestError('INVALID_BRANCH_REF')
    name = value[len('refs/heads/'):]
    if not name or re.fullmatch(r'[A-Za-z0-9_./-]+', name) is None or '..' in name:
        raise ManifestError('INVALID_BRANCH_REF')
    if any(not p or p.startswith('.') or p.endswith(('.', '.lock')) for p in name.split('/')):
        raise ManifestError('INVALID_BRANCH_REF')
    return value

def safe_push_url(value):
    if not isinstance(value, str) or not value or value.startswith('-') or any(c.isspace() or ord(c) < 32 for c in value):
        raise ManifestError('UNSAFE_PUSH_URL')
    try:
        if '://' in value:
            p = urlsplit(value)
            if p.scheme not in {'https', 'ssh', 'file'} or p.query or p.fragment or p.password is not None:
                raise ValueError()
            if p.scheme == 'https' and p.username is not None:
                raise ValueError()
            if p.scheme != 'file' and not p.hostname:
                raise ValueError()
            if p.scheme == 'file' and (p.netloc or not p.path.startswith('/')):
                raise ValueError()
            if not p.path or p.path == '/':
                raise ValueError()
            _ = p.port
        elif re.fullmatch(r'(?:[A-Za-z0-9_.-]+@)?[A-Za-z0-9_.-]+:[A-Za-z0-9_./-]+', value) is None:
            raise ValueError()
    except ValueError:
        raise ManifestError('UNSAFE_PUSH_URL') from None
    return value

def _oids(value):
    if not isinstance(value, list):
        raise ManifestError('INVALID_COMMIT_LIST')
    result = [oid(x) for x in value]
    if len(set(result)) != len(result):
        raise ManifestError('DUPLICATE_COMMIT')
    return result

FLAGS = frozenset({'force', 'delete', 'no_verify', 'hook_bypass', 'follow_tags', 'mirror', 'all', 'tags'})
FIELDS = frozenset({'remote', 'push_urls', 'local_ref', 'remote_ref', 'refspec', 'head_oid', 'source_oid',
                    'remote_oid', 'fetched_at', 'incoming', 'outgoing', 'scope_commits', 'fast_forward', 'flags', 'extra_ref_updates'})

def validate_git_snapshot(snapshot, *, now, max_fetch_age=300):
    """Validate trusted observations, not their provenance or fetch success.

    Initially one existing branch and explicit refspec only. Outgoing is ordered
    oldest first, HEAD last. New branches require a future default-base collector.
    """
    if not isinstance(snapshot, dict) or set(snapshot) != FIELDS:
        raise ManifestError('INVALID_GIT_FIELDS')
    identifier(snapshot['remote'])
    urls = snapshot['push_urls']
    if not isinstance(urls, list) or len(urls) != 1:
        raise ManifestError('MULTIPLE_OR_MISSING_DESTINATIONS')
    safe_push_url(urls[0])
    local, remote = branch_ref(snapshot['local_ref']), branch_ref(snapshot['remote_ref'])
    if snapshot['refspec'] != local + ':' + remote:
        raise ManifestError('REFSPEC_MISMATCH')
    for field in ('head_oid', 'source_oid', 'remote_oid'):
        oid(snapshot[field])
    length = len(snapshot['head_oid'])
    if any(len(snapshot[k]) != length for k in ('source_oid', 'remote_oid')):
        raise ManifestError('OID_FORMAT_MISMATCH')
    if snapshot['head_oid'] != snapshot['source_oid']:
        raise ManifestError('SOURCE_IS_NOT_HEAD')
    current, fetched, age = timestamp(now), timestamp(snapshot['fetched_at']), timestamp(max_fetch_age)
    if age <= 0 or fetched > current or current - fetched > age:
        raise ManifestError('FETCH_NOT_FRESH')
    incoming, outgoing, scope = (_oids(snapshot[k]) for k in ('incoming', 'outgoing', 'scope_commits'))
    if incoming:
        raise ManifestError('INCOMING_COMMITS')
    if not outgoing or outgoing[-1] != snapshot['head_oid'] or snapshot['remote_oid'] in outgoing:
        raise ManifestError('INVALID_OUTGOING_COMMITS')
    if any(len(x) != length for x in outgoing + scope):
        raise ManifestError('OID_FORMAT_MISMATCH')
    if set(outgoing) != set(scope):
        raise ManifestError('OUT_OF_SCOPE_COMMITS')
    if snapshot['fast_forward'] is not True:
        raise ManifestError('NOT_FAST_FORWARD')
    flags = snapshot['flags']
    if not isinstance(flags, dict) or set(flags) != FLAGS or any(v is not False for v in flags.values()):
        raise ManifestError('UNSAFE_PUSH_FLAGS')
    if snapshot['extra_ref_updates'] != []:
        raise ManifestError('EXTRA_REF_UPDATES')
    return copy.deepcopy(snapshot)
