"""Calibrated thickness model for the bounded file-change PoC domain."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from math import isfinite
from typing import Mapping, Sequence

from .boundary import Thresholds
from .history import AppendOnlyHistoryLedger, HistoryEvent, HistoryEventKind
from .proposal import ActionProposal
from .thickness import (
    ThicknessEstimate,
    ThicknessEvaluation,
    ThicknessEvaluationStatus,
    ThicknessTrendState,
    evaluate_thickness_estimate,
)


class FileChangeFactType(str, Enum):
    CAPACITY_BASELINE = "CAPACITY_BASELINE"
    CHANGE_PROPOSED = "CHANGE_PROPOSED"
    CHANGE_RESOLVED = "CHANGE_RESOLVED"
    THICKNESS_LOSS = "THICKNESS_LOSS"
    THICKNESS_RECOVERY_VERIFIED = "THICKNESS_RECOVERY_VERIFIED"


_EVENT_KIND = {
    FileChangeFactType.CAPACITY_BASELINE: HistoryEventKind.OBSERVATION,
    FileChangeFactType.CHANGE_PROPOSED: HistoryEventKind.PROPOSAL,
    FileChangeFactType.CHANGE_RESOLVED: HistoryEventKind.RECONCILIATION,
    FileChangeFactType.THICKNESS_LOSS: HistoryEventKind.OBSERVATION,
    FileChangeFactType.THICKNESS_RECOVERY_VERIFIED: HistoryEventKind.RECONCILIATION,
}


@dataclass(frozen=True, slots=True)
class FileChangeFact:
    fact_type: FileChangeFactType
    request_id: str | None = None
    changed_lines: int | None = None
    files_touched: int | None = None
    capacity_units: float | None = None
    units: float | None = None

    def payload(self) -> dict[str, object]:
        if not isinstance(self.fact_type, FileChangeFactType):
            raise ValueError("fact_type must be a FileChangeFactType")
        data: dict[str, object] = {
            "schema_version": "file-change-thickness/1.0",
            "fact_type": self.fact_type.value,
        }
        if self.fact_type is FileChangeFactType.CAPACITY_BASELINE:
            _require_positive_number(self.capacity_units, "capacity_units")
            data["capacity_units"] = self.capacity_units
        elif self.fact_type is FileChangeFactType.CHANGE_PROPOSED:
            if not self.request_id:
                raise ValueError("request_id is required")
            _require_nonnegative_int(self.changed_lines, "changed_lines")
            _require_positive_int(self.files_touched, "files_touched")
            data.update(
                request_id=self.request_id,
                changed_lines=self.changed_lines,
                files_touched=self.files_touched,
            )
        elif self.fact_type is FileChangeFactType.CHANGE_RESOLVED:
            if not self.request_id:
                raise ValueError("request_id is required")
            data["request_id"] = self.request_id
        else:
            _require_positive_number(self.units, "units")
            data["units"] = self.units
        return data


@dataclass(frozen=True, slots=True)
class FileChangeThicknessContract:
    target_id: str
    axis_id: str
    model_version: str
    unit: str
    line_cost: float
    file_overhead: float
    reserve_units: float
    step_loss_units: float
    thresholds: Thresholds
    trusted_source_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not all((self.target_id, self.axis_id, self.model_version, self.unit)):
            raise ValueError("identifiers and unit must not be empty")
        values = (
            self.line_cost,
            self.file_overhead,
            self.reserve_units,
            self.step_loss_units,
        )
        if not all(
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and isfinite(value)
            and value >= 0
            for value in values
        ):
            raise ValueError("cost and reserve values must be finite and nonnegative")
        if self.line_cost == 0 and self.file_overhead == 0:
            raise ValueError("at least one proposal cost must be positive")
        if self.step_loss_units <= 0:
            raise ValueError("step_loss_units must be positive")
        if not self.trusted_source_ids or any(
            not source_id for source_id in self.trusted_source_ids
        ):
            raise ValueError("trusted_source_ids must not be empty")


def append_file_change_fact(
    ledger: AppendOnlyHistoryLedger,
    *,
    event_id: str,
    target_id: str,
    source_id: str,
    occurred_at: str,
    fact: FileChangeFact,
) -> HistoryEvent:
    return ledger.append(
        event_id=event_id,
        kind=_EVENT_KIND[fact.fact_type],
        target_id=target_id,
        source_id=source_id,
        occurred_at=occurred_at,
        payload=fact.payload(),
    )


def measure_proposal_fact(proposal: ActionProposal) -> FileChangeFact:
    """Measure change units from the decoded diff, never from AI numeric claims."""
    changed_lines = 0
    in_hunk = False
    hunk_seen = False
    for line in proposal.patch.splitlines():
        if line.startswith("@@ "):
            in_hunk = True
            hunk_seen = True
            continue
        if in_hunk and line.startswith(("+", "-")):
            changed_lines += 1
    if not hunk_seen:
        raise ValueError("unified diff hunk is required")
    return FileChangeFact(
        FileChangeFactType.CHANGE_PROPOSED,
        request_id=proposal.idempotency_key,
        changed_lines=changed_lines,
        files_touched=1,
    )


class FileChangeThicknessModel:
    domain_id = "bounded-file-change"

    def __init__(self, contract: FileChangeThicknessContract) -> None:
        self.contract = contract
        self.model_version = contract.model_version

    def evaluate(self, history: Sequence[HistoryEvent]) -> ThicknessEvaluation:
        try:
            estimate = self.estimate(history)
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            return ThicknessEvaluation(
                ThicknessEvaluationStatus.INPUT_EXCEPTION,
                None,
                None,
                (f"FILE_CHANGE_HISTORY_INVALID:{type(error).__name__}",),
            )
        return evaluate_thickness_estimate(estimate, self.contract.thresholds)

    def estimate(self, history: Sequence[HistoryEvent]) -> ThicknessEstimate:
        """Derive conservative file-change delta and tau from verified history.

        ``history`` must be a valid append-only chain with exactly one capacity
        baseline and consistent proposal, resolution, loss, and recovery facts.
        Invalid ordering or impossible recovery raises ``ValueError``. The
        returned estimate records source event identifiers and does not modify
        the ledger or the estimator contract.
        """
        events = tuple(history)
        if not AppendOnlyHistoryLedger.verify(events):
            raise ValueError("history chain is invalid")
        facts = self._parse_facts(events)
        baseline_indexes = [
            index
            for index, (_, fact) in enumerate(facts)
            if fact.fact_type is FileChangeFactType.CAPACITY_BASELINE
        ]
        if not baseline_indexes:
            raise ValueError("capacity baseline is required")
        if len(baseline_indexes) != 1:
            raise ValueError(
                "multiple capacity baselines require an explicit migration"
            )

        start = baseline_indexes[0]
        baseline_event, baseline = facts[start]
        assert baseline.capacity_units is not None
        pending: dict[str, float] = {}
        loss_units = 0.0
        loss_steps: list[float] = []
        recovery_seen = False
        source_event_ids = [baseline_event.event_id]

        for event, fact in facts[start + 1 :]:
            source_event_ids.append(event.event_id)
            if fact.fact_type is FileChangeFactType.CAPACITY_BASELINE:
                raise ValueError("unexpected baseline ordering")
            if fact.fact_type is FileChangeFactType.CHANGE_PROPOSED:
                assert fact.request_id is not None
                assert fact.changed_lines is not None
                assert fact.files_touched is not None
                if fact.request_id in pending:
                    raise ValueError("duplicate pending request")
                pending[fact.request_id] = (
                    fact.changed_lines * self.contract.line_cost
                    + fact.files_touched * self.contract.file_overhead
                )
            elif fact.fact_type is FileChangeFactType.CHANGE_RESOLVED:
                assert fact.request_id is not None
                if fact.request_id not in pending:
                    raise ValueError("resolution without pending request")
                del pending[fact.request_id]
            elif fact.fact_type is FileChangeFactType.THICKNESS_LOSS:
                assert fact.units is not None
                loss_units += fact.units
                loss_steps.append(fact.units)
                recovery_seen = False
            elif fact.fact_type is FileChangeFactType.THICKNESS_RECOVERY_VERIFIED:
                assert fact.units is not None
                if fact.units > loss_units:
                    raise ValueError("recovery exceeds observed loss")
                loss_units -= fact.units
                recovery_seen = True

        delta = sum(pending.values())
        tau = baseline.capacity_units - self.contract.reserve_units - loss_units
        trend = _classify_trend(
            loss_units=loss_units,
            loss_steps=loss_steps,
            recovery_seen=recovery_seen,
            step_loss_units=self.contract.step_loss_units,
        )
        return ThicknessEstimate(
            axis_id=self.contract.axis_id,
            delta_lower=delta,
            delta_upper=delta,
            tau_lower=tau,
            tau_upper=tau,
            unit=self.contract.unit,
            model_version=self.contract.model_version,
            source_event_ids=tuple(source_event_ids),
            trend=trend,
        )

    def _parse_facts(
        self,
        events: Sequence[HistoryEvent],
    ) -> list[tuple[HistoryEvent, FileChangeFact]]:
        parsed: list[tuple[HistoryEvent, FileChangeFact]] = []
        for event in events:
            if event.target_id != self.contract.target_id:
                continue
            payload = json.loads(event.payload_json)
            if payload.get("schema_version") != "file-change-thickness/1.0":
                continue
            if event.source_id not in self.contract.trusted_source_ids:
                raise ValueError("untrusted thickness fact source")
            fact_type = FileChangeFactType(payload["fact_type"])
            if event.kind is not _EVENT_KIND[fact_type]:
                raise ValueError("fact type and history kind mismatch")
            fact = _decode_fact(payload, fact_type)
            parsed.append((event, fact))
        return parsed


def _decode_fact(
    payload: Mapping[str, object],
    fact_type: FileChangeFactType,
) -> FileChangeFact:
    common = {"schema_version", "fact_type"}
    expected = {
        FileChangeFactType.CAPACITY_BASELINE: common | {"capacity_units"},
        FileChangeFactType.CHANGE_PROPOSED: common
        | {"request_id", "changed_lines", "files_touched"},
        FileChangeFactType.CHANGE_RESOLVED: common | {"request_id"},
        FileChangeFactType.THICKNESS_LOSS: common | {"units"},
        FileChangeFactType.THICKNESS_RECOVERY_VERIFIED: common | {"units"},
    }[fact_type]
    if set(payload) != expected:
        raise ValueError("unexpected thickness fact fields")
    fact = FileChangeFact(
        fact_type=fact_type,
        request_id=payload.get("request_id"),
        changed_lines=payload.get("changed_lines"),
        files_touched=payload.get("files_touched"),
        capacity_units=payload.get("capacity_units"),
        units=payload.get("units"),
    )
    fact.payload()
    return fact


def _classify_trend(
    *,
    loss_units: float,
    loss_steps: Sequence[float],
    recovery_seen: bool,
    step_loss_units: float,
) -> ThicknessTrendState:
    if recovery_seen:
        return ThicknessTrendState.RECOVERY_VERIFIED
    if loss_steps and loss_steps[-1] >= step_loss_units:
        return ThicknessTrendState.STEP_LOSS
    if len(loss_steps) >= 2 and loss_steps[-1] > loss_steps[-2]:
        return ThicknessTrendState.ACCELERATING_DEPLETION
    if loss_units > 0:
        return ThicknessTrendState.DEPLETING
    return ThicknessTrendState.STABLE


def _require_nonnegative_int(value: object, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")


def _require_positive_int(value: object, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")


def _require_positive_number(value: object, name: str) -> None:
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not isfinite(value)
        or value <= 0
    ):
        raise ValueError(f"{name} must be a positive finite number")
