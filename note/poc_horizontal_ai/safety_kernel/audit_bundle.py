"""Portable history bundle whose head digest can be anchored externally."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone

from .history import AppendOnlyHistoryLedger, HistoryEvent, HistoryEventKind


_MAX_BUNDLE_BYTES = 8 * 1024 * 1024
_MAX_RECORD_BYTES = 256 * 1024


@dataclass(frozen=True, slots=True)
class AuditBundleVerification:
    events: tuple[HistoryEvent, ...] | None
    head_digest: str | None
    reason_codes: tuple[str, ...]


def create_audit_bundle(
    events: tuple[HistoryEvent, ...],
    *,
    exported_at: datetime,
) -> str:
    if exported_at.tzinfo is None:
        raise ValueError("exported_at must be timezone-aware")
    if not AppendOnlyHistoryLedger.verify(events):
        raise ValueError("history chain is invalid")
    records_jsonl = "\n".join(
        _canonical_json(
            {
                **asdict(event),
                "kind": event.kind.value,
            }
        )
        for event in events
    )
    head_digest = events[-1].digest if events else None
    return _canonical_json(
        {
            "event_count": len(events),
            "exported_at": exported_at.astimezone(timezone.utc).isoformat(),
            "head_digest": head_digest,
            "records_jsonl": records_jsonl,
            "records_sha256": _sha256(records_jsonl),
            "schema_version": "audit-bundle/1.0",
        }
    )


def verify_audit_bundle(
    bundle_json: str,
    *,
    expected_head_digest: str | None = None,
) -> AuditBundleVerification:
    """Verify an exported audit bundle and its append-only digest chain.

    ``bundle_json`` must use the exact bundle schema and bounded record format.
    ``expected_head_digest`` optionally binds the verified chain to an external
    anchor. Structural, count, chain, head, or anchor mismatches return no
    events with stable reason codes; the function performs no writes.
    """
    try:
        bundle = _strict_object(bundle_json, _MAX_BUNDLE_BYTES)
        if set(bundle) != {
            "event_count",
            "exported_at",
            "head_digest",
            "records_jsonl",
            "records_sha256",
            "schema_version",
        }:
            raise ValueError("unexpected bundle fields")
        if bundle["schema_version"] != "audit-bundle/1.0":
            raise ValueError("unsupported bundle schema")
        event_count = _strict_int(bundle["event_count"])
        if event_count < 0:
            raise ValueError("negative event_count")
        exported_at = datetime.fromisoformat(_strict_str(bundle["exported_at"]))
        if exported_at.tzinfo is None:
            raise ValueError("timezone required")
        records_jsonl = _strict_str(bundle["records_jsonl"])
        if bundle["records_sha256"] != _sha256(records_jsonl):
            return AuditBundleVerification(
                None,
                None,
                ("AUDIT_RECORDS_DIGEST_MISMATCH",),
            )
        lines = [] if not records_jsonl else records_jsonl.splitlines()
        events = tuple(
            _decode_event(_strict_object(line, _MAX_RECORD_BYTES)) for line in lines
        )
        if len(events) != event_count:
            return AuditBundleVerification(
                None,
                None,
                ("AUDIT_EVENT_COUNT_MISMATCH",),
            )
        if not AppendOnlyHistoryLedger.verify(events):
            return AuditBundleVerification(
                None,
                None,
                ("AUDIT_CHAIN_INVALID",),
            )
        actual_head = events[-1].digest if events else None
        if bundle["head_digest"] != actual_head:
            return AuditBundleVerification(
                None,
                actual_head,
                ("AUDIT_HEAD_MISMATCH",),
            )
        if expected_head_digest is not None and actual_head != expected_head_digest:
            return AuditBundleVerification(
                None,
                actual_head,
                ("AUDIT_EXTERNAL_ANCHOR_MISMATCH",),
            )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return AuditBundleVerification(None, None, ("AUDIT_BUNDLE_INVALID",))
    return AuditBundleVerification(events, actual_head, ())


def _decode_event(data: dict[str, object]) -> HistoryEvent:
    if set(data) != {
        "digest",
        "event_id",
        "kind",
        "occurred_at",
        "payload_json",
        "previous_digest",
        "sequence",
        "source_id",
        "target_id",
    }:
        raise ValueError("unexpected history event fields")
    previous_digest = data["previous_digest"]
    if previous_digest is not None and not isinstance(previous_digest, str):
        raise ValueError("invalid previous_digest")
    return HistoryEvent(
        sequence=_strict_int(data["sequence"]),
        event_id=_strict_str(data["event_id"]),
        kind=HistoryEventKind(_strict_str(data["kind"])),
        target_id=_strict_str(data["target_id"]),
        source_id=_strict_str(data["source_id"]),
        occurred_at=_strict_str(data["occurred_at"]),
        payload_json=_strict_str(data["payload_json"]),
        previous_digest=previous_digest,
        digest=_strict_str(data["digest"]),
    )


def _strict_object(text: str, max_bytes: int) -> dict[str, object]:
    if len(text.encode("utf-8")) > max_bytes:
        raise ValueError("input too large")
    def pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate field")
            result[key] = value
        return result

    data = json.loads(text, object_pairs_hook=pairs_hook)
    if not isinstance(data, dict):
        raise ValueError("object required")
    return data


def _canonical_json(data: dict[str, object]) -> str:
    return json.dumps(
        data,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _strict_str(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("string required")
    return value


def _strict_int(value: object) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError("integer required")
    return value
