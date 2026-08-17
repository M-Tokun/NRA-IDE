"""Persistent trusted-side owner of per-target irreversible boundary latches."""

from __future__ import annotations

import hashlib
import hmac
import json
import sqlite3
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from ..safety_kernel.boundary import (
    AxisEvidence,
    BoundaryAssessment,
    evaluate_axes,
)
from ..safety_kernel.states import TargetBoundaryState


_LATCHING_STATES = {
    TargetBoundaryState.IRREVERSIBLE_TRANSITION,
    TargetBoundaryState.RUPTURE_BOUNDARY,
}


@dataclass(frozen=True, slots=True)
class IrreversibleLatchHead:
    sequence: int
    previous_mac: str | None
    row_mac: str


class PersistentIrreversibleLatchStore:
    """Evaluate axes and atomically retain every irreversible transition."""

    def __init__(self, database_path: Path, integrity_key: bytes) -> None:
        if database_path.is_symlink():
            raise ValueError("latch database must not be a symlink")
        if not database_path.parent.exists():
            raise ValueError("latch database parent must already exist")
        _validate_key(integrity_key)
        self.database_path = database_path
        self._integrity_key = integrity_key
        self._connection = sqlite3.connect(database_path, timeout=5.0)
        self._connection.execute("PRAGMA synchronous=FULL")
        self._connection.execute("PRAGMA journal_mode=DELETE")
        self._initialize()
        integrity_reasons = self.verify()
        if integrity_reasons:
            self.close()
            raise ValueError(",".join(integrity_reasons))

    def __enter__(self) -> "PersistentIrreversibleLatchStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        self._connection.close()

    def assess_axes(
        self,
        *,
        target_id: str,
        axes: Iterable[AxisEvidence],
        observed_at: datetime,
    ) -> BoundaryAssessment:
        """Apply stored latches, classify, and persist newly crossed latches."""
        try:
            axis_values = tuple(axes)
        except TypeError as error:
            raise ValueError("invalid irreversible latch assessment input") from error
        if (
            not isinstance(target_id, str)
            or not target_id
            or len(target_id) > 256
            or not isinstance(observed_at, datetime)
            or observed_at.tzinfo is None
            or not all(isinstance(axis, AxisEvidence) for axis in axis_values)
        ):
            raise ValueError("invalid irreversible latch assessment input")

        try:
            self._connection.execute("BEGIN IMMEDIATE")
            integrity_reasons = self.verify()
            if integrity_reasons:
                self._connection.rollback()
                raise ValueError(",".join(integrity_reasons))

            latched_names = {
                str(row[0])
                for row in self._connection.execute(
                    "SELECT axis_name FROM irreversible_latch WHERE target_id = ?",
                    (target_id,),
                ).fetchall()
            }
            effective_axes = tuple(
                (
                    replace(
                        axis,
                        irreversible_latched=axis.name in latched_names,
                    )
                    if isinstance(axis.name, str)
                    and isinstance(axis.irreversible_latched, bool)
                    else axis
                )
                for axis in axis_values
            )
            assessment = evaluate_axes(effective_axes)

            row = self._connection.execute(
                "SELECT sequence, row_mac FROM irreversible_latch "
                "ORDER BY sequence DESC LIMIT 1"
            ).fetchone()
            sequence = 1 if row is None else int(row[0]) + 1
            previous_mac = None if row is None else str(row[1])
            latched_at = observed_at.astimezone(timezone.utc).isoformat()

            for axis_assessment in assessment.axes:
                if (
                    axis_assessment.target_state not in _LATCHING_STATES
                    or axis_assessment.name in latched_names
                ):
                    continue
                fields = {
                    "axis_name": axis_assessment.name,
                    "latched_at": latched_at,
                    "previous_mac": previous_mac,
                    "sequence": sequence,
                    "target_id": target_id,
                    "trigger_state": axis_assessment.target_state.value,
                }
                row_mac = _mac(self._integrity_key, fields)
                self._connection.execute(
                    """
                    INSERT INTO irreversible_latch(
                        sequence, target_id, axis_name, trigger_state,
                        latched_at, previous_mac, row_mac
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        sequence,
                        target_id,
                        axis_assessment.name,
                        axis_assessment.target_state.value,
                        latched_at,
                        previous_mac,
                        row_mac,
                    ),
                )
                latched_names.add(axis_assessment.name)
                sequence += 1
                previous_mac = row_mac

            self._connection.commit()
            return assessment
        except sqlite3.DatabaseError as error:
            self._connection.rollback()
            raise ValueError("IRREVERSIBLE_LATCH_STORE_FAILURE") from error
        except Exception:
            self._connection.rollback()
            raise

    def verify(self) -> tuple[str, ...]:
        previous_mac = None
        try:
            rows = self._connection.execute(
                """
                SELECT sequence, target_id, axis_name, trigger_state,
                       latched_at, previous_mac, row_mac
                FROM irreversible_latch ORDER BY sequence
                """
            ).fetchall()
        except sqlite3.DatabaseError:
            return ("IRREVERSIBLE_LATCH_STORE_FAILURE",)

        valid_states = {state.value for state in _LATCHING_STATES}
        observed_keys: set[tuple[str, str]] = set()
        for expected_sequence, row in enumerate(rows, 1):
            (
                sequence,
                target_id,
                axis_name,
                trigger_state,
                latched_at,
                stored_previous,
                row_mac,
            ) = row
            key = (target_id, axis_name)
            if (
                sequence != expected_sequence
                or not isinstance(target_id, str)
                or not isinstance(axis_name, str)
                or not isinstance(trigger_state, str)
                or not isinstance(latched_at, str)
                or not isinstance(stored_previous, (str, type(None)))
                or not isinstance(row_mac, str)
                or stored_previous != previous_mac
                or not target_id
                or not axis_name
                or not latched_at
                or trigger_state not in valid_states
                or key in observed_keys
            ):
                return ("IRREVERSIBLE_LATCH_CHAIN_INVALID",)
            fields = {
                "axis_name": axis_name,
                "latched_at": latched_at,
                "previous_mac": stored_previous,
                "sequence": sequence,
                "target_id": target_id,
                "trigger_state": trigger_state,
            }
            if not hmac.compare_digest(row_mac, _mac(self._integrity_key, fields)):
                return ("IRREVERSIBLE_LATCH_CHAIN_INVALID",)
            observed_keys.add(key)
            previous_mac = row_mac
        return ()

    def latched_axis_names(self, target_id: str) -> frozenset[str]:
        """Axis names permanently latched for target_id; never resettable."""
        if not isinstance(target_id, str) or not target_id:
            raise ValueError("target_id must be a nonempty string")
        reasons = self.verify()
        if reasons:
            raise ValueError(",".join(reasons))
        rows = self._connection.execute(
            "SELECT axis_name FROM irreversible_latch WHERE target_id = ?",
            (target_id,),
        ).fetchall()
        return frozenset(str(row[0]) for row in rows)

    def head(self) -> IrreversibleLatchHead | None:
        reasons = self.verify()
        if reasons:
            raise ValueError(",".join(reasons))
        row = self._connection.execute(
            "SELECT sequence, previous_mac, row_mac FROM irreversible_latch "
            "ORDER BY sequence DESC LIMIT 1"
        ).fetchone()
        if row is None:
            return None
        return IrreversibleLatchHead(int(row[0]), row[1], str(row[2]))

    def head_at(self, sequence: int) -> IrreversibleLatchHead | None:
        if (
            not isinstance(sequence, int)
            or isinstance(sequence, bool)
            or sequence <= 0
        ):
            raise ValueError("latch sequence must be positive")
        reasons = self.verify()
        if reasons:
            raise ValueError(",".join(reasons))
        row = self._connection.execute(
            "SELECT sequence, previous_mac, row_mac FROM irreversible_latch "
            "WHERE sequence = ?",
            (sequence,),
        ).fetchone()
        if row is None:
            return None
        return IrreversibleLatchHead(int(row[0]), row[1], str(row[2]))

    def _initialize(self) -> None:
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS irreversible_latch (
                sequence INTEGER PRIMARY KEY,
                target_id TEXT NOT NULL,
                axis_name TEXT NOT NULL,
                trigger_state TEXT NOT NULL,
                latched_at TEXT NOT NULL,
                previous_mac TEXT,
                row_mac TEXT NOT NULL,
                UNIQUE(target_id, axis_name)
            );
            CREATE TRIGGER IF NOT EXISTS irreversible_latch_no_update
            BEFORE UPDATE ON irreversible_latch
            BEGIN SELECT RAISE(ABORT, 'append-only irreversible latch'); END;
            CREATE TRIGGER IF NOT EXISTS irreversible_latch_no_delete
            BEFORE DELETE ON irreversible_latch
            BEGIN SELECT RAISE(ABORT, 'append-only irreversible latch'); END;
            """
        )
        self._connection.commit()


def _validate_key(key: bytes) -> None:
    if not isinstance(key, bytes) or len(key) < 32:
        raise ValueError("integrity_key must contain at least 32 bytes")


def _mac(key: bytes, fields: dict[str, object]) -> str:
    material = json.dumps(
        fields,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hmac.new(key, material, hashlib.sha256).hexdigest()
