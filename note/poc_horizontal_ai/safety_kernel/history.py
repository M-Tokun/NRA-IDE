"""In-memory append-only event chain for deterministic shadow replay."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class HistoryEventKind(str, Enum):
    PROPOSAL = "PROPOSAL"
    OBSERVATION = "OBSERVATION"
    REPORT = "REPORT"
    RESPONSE = "RESPONSE"
    OVERRIDE = "OVERRIDE"
    DECISION = "DECISION"
    RECONCILIATION = "RECONCILIATION"


@dataclass(frozen=True, slots=True)
class HistoryEvent:
    sequence: int
    event_id: str
    kind: HistoryEventKind
    target_id: str
    source_id: str
    occurred_at: str
    payload_json: str
    previous_digest: str | None
    digest: str


def _canonical_payload(payload: Mapping[str, object]) -> str:
    return json.dumps(
        payload,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _digest_material(
    sequence: int,
    event_id: str,
    kind: HistoryEventKind,
    target_id: str,
    source_id: str,
    occurred_at: str,
    payload_json: str,
    previous_digest: str | None,
) -> bytes:
    return _canonical_payload(
        {
            "event_id": event_id,
            "kind": kind.value,
            "occurred_at": occurred_at,
            "payload_json": payload_json,
            "previous_digest": previous_digest,
            "sequence": sequence,
            "source_id": source_id,
            "target_id": target_id,
        }
    ).encode("utf-8")


class AppendOnlyHistoryLedger:
    def __init__(self) -> None:
        self._events: list[HistoryEvent] = []
        self._event_ids: set[str] = set()

    @property
    def events(self) -> tuple[HistoryEvent, ...]:
        return tuple(self._events)

    def append(
        self,
        *,
        event_id: str,
        kind: HistoryEventKind,
        target_id: str,
        source_id: str,
        occurred_at: str,
        payload: Mapping[str, object],
    ) -> HistoryEvent:
        if not event_id or event_id in self._event_ids:
            raise ValueError("event_id must be non-empty and unique")
        if not target_id or not source_id or not occurred_at:
            raise ValueError("target_id, source_id, and occurred_at are required")
        payload_json = _canonical_payload(payload)
        sequence = len(self._events)
        previous_digest = self._events[-1].digest if self._events else None
        digest = hashlib.sha256(
            _digest_material(
                sequence,
                event_id,
                kind,
                target_id,
                source_id,
                occurred_at,
                payload_json,
                previous_digest,
            )
        ).hexdigest()
        event = HistoryEvent(
            sequence=sequence,
            event_id=event_id,
            kind=kind,
            target_id=target_id,
            source_id=source_id,
            occurred_at=occurred_at,
            payload_json=payload_json,
            previous_digest=previous_digest,
            digest=digest,
        )
        self._events.append(event)
        self._event_ids.add(event_id)
        return event

    @staticmethod
    def verify(events: tuple[HistoryEvent, ...]) -> bool:
        previous_digest = None
        seen: set[str] = set()
        for sequence, event in enumerate(events):
            if event.sequence != sequence or event.event_id in seen:
                return False
            if event.previous_digest != previous_digest:
                return False
            expected = hashlib.sha256(
                _digest_material(
                    event.sequence,
                    event.event_id,
                    event.kind,
                    event.target_id,
                    event.source_id,
                    event.occurred_at,
                    event.payload_json,
                    event.previous_digest,
                )
            ).hexdigest()
            if expected != event.digest:
                return False
            seen.add(event.event_id)
            previous_digest = event.digest
        return True
