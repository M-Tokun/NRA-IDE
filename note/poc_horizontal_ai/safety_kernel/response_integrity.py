"""Track whether observed warnings reach verified resolution."""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Iterable

from .reconciliation import ReconciliationState


class ResponseEventType(str, Enum):
    WARNING_ACKNOWLEDGED = "WARNING_ACKNOWLEDGED"
    ACTION_STARTED = "ACTION_STARTED"
    ACTION_COMPLETED = "ACTION_COMPLETED"
    DEFERRED = "DEFERRED"
    OVERRIDDEN = "OVERRIDDEN"
    UNRESOLVED = "UNRESOLVED"
    RECURRENCE = "RECURRENCE"


class ResponseIntegrityState(str, Enum):
    NO_RESPONSE_HISTORY = "NO_RESPONSE_HISTORY"
    INPUT_EXCEPTION = "INPUT_EXCEPTION"
    ACKNOWLEDGED_UNRESOLVED = "ACKNOWLEDGED_UNRESOLVED"
    ACTION_IN_PROGRESS = "ACTION_IN_PROGRESS"
    DEFERRED = "DEFERRED"
    OVERRIDDEN = "OVERRIDDEN"
    COMPLETED_UNVERIFIED = "COMPLETED_UNVERIFIED"
    VERIFIED_RESOLVED = "VERIFIED_RESOLVED"
    RECURRENT = "RECURRENT"
    EXPIRED = "EXPIRED"


@dataclass(frozen=True, slots=True)
class ResponseEvent:
    event_id: str
    target_id: str
    warning_id: str
    event_type: ResponseEventType
    actor_id: str
    occurred_at: datetime
    expires_at: datetime | None = None
    sequence: int = 1


def assess_response_integrity(
    events: Iterable[ResponseEvent],
    reconciliation_state: ReconciliationState | None,
    *,
    now: datetime | None = None,
) -> ResponseIntegrityState:
    """Classify an immutable response-event history and reconciliation state.

    ``events`` must describe one target/warning pair with unique identifiers
    and ordering keys. ``now`` is required and must be timezone-aware whenever
    an expiry is present. Invalid input maps to ``INPUT_EXCEPTION``; completion
    is ``VERIFIED_RESOLVED`` only when reconciliation is ``MATCHED``. The
    function sorts a local copy and does not mutate the event history.
    """
    recorded = tuple(events)
    if not recorded:
        return ResponseIntegrityState.NO_RESPONSE_HISTORY
    if reconciliation_state is not None and not isinstance(
        reconciliation_state,
        ReconciliationState,
    ):
        return ResponseIntegrityState.INPUT_EXCEPTION
    if any(not _valid_event(event) for event in recorded):
        return ResponseIntegrityState.INPUT_EXCEPTION
    if len({event.event_id for event in recorded}) != len(recorded):
        return ResponseIntegrityState.INPUT_EXCEPTION
    if len({(event.target_id, event.warning_id) for event in recorded}) != 1:
        return ResponseIntegrityState.INPUT_EXCEPTION
    ordering_keys = tuple(
        (event.occurred_at, event.sequence) for event in recorded
    )
    if len(set(ordering_keys)) != len(ordering_keys):
        return ResponseIntegrityState.INPUT_EXCEPTION
    if any(event.expires_at is not None for event in recorded):
        if now is None or now.tzinfo is None:
            return ResponseIntegrityState.INPUT_EXCEPTION
        current = now.astimezone(timezone.utc)
    else:
        current = None

    ordered = sorted(
        recorded,
        key=lambda event: (event.occurred_at, event.sequence),
    )
    if any(
        event.event_type is ResponseEventType.RECURRENCE
        for event in ordered
    ):
        return ResponseIntegrityState.RECURRENT
    latest_event = ordered[-1]
    if (
        latest_event.expires_at is not None
        and current is not None
        and latest_event.expires_at.astimezone(timezone.utc) <= current
    ):
        return ResponseIntegrityState.EXPIRED
    latest = latest_event.event_type
    if latest is ResponseEventType.RECURRENCE:
        return ResponseIntegrityState.RECURRENT
    if latest is ResponseEventType.OVERRIDDEN:
        return ResponseIntegrityState.OVERRIDDEN
    if latest is ResponseEventType.DEFERRED:
        return ResponseIntegrityState.DEFERRED
    if latest is ResponseEventType.UNRESOLVED:
        return ResponseIntegrityState.ACKNOWLEDGED_UNRESOLVED
    if latest is ResponseEventType.ACTION_STARTED:
        return ResponseIntegrityState.ACTION_IN_PROGRESS
    if latest is ResponseEventType.ACTION_COMPLETED:
        if reconciliation_state is ReconciliationState.MATCHED:
            return ResponseIntegrityState.VERIFIED_RESOLVED
        return ResponseIntegrityState.COMPLETED_UNVERIFIED
    return ResponseIntegrityState.ACKNOWLEDGED_UNRESOLVED


def _valid_event(event: object) -> bool:
    if not isinstance(event, ResponseEvent):
        return False
    if (
        not event.event_id
        or not event.target_id
        or not event.warning_id
        or not event.actor_id
        or not isinstance(event.event_type, ResponseEventType)
        or not isinstance(event.sequence, int)
        or isinstance(event.sequence, bool)
        or event.sequence <= 0
        or not isinstance(event.occurred_at, datetime)
        or event.occurred_at.tzinfo is None
    ):
        return False
    if event.expires_at is not None:
        if (
            not isinstance(event.expires_at, datetime)
            or event.expires_at.tzinfo is None
            or event.expires_at <= event.occurred_at
        ):
            return False
    return True
