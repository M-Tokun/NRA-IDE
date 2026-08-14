# memory_store.py | Time-stamp: 26-0812-1939
"""SQLite persistence layer for horizontal-state vectors."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True, slots=True)
class StateRecord:
    record_id: int
    run_id: str
    step: int
    timestamp: str
    state: NDArray[np.float32]
    gate_mean: float
    retention_mean: float
    metadata: dict[str, Any]


class HorizontalMemoryRepository:
    """Append and retrieve horizontal states without pickled object data."""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.db_path)
        self._connection.row_factory = sqlite3.Row
        self._create_schema()

    def __enter__(self) -> HorizontalMemoryRepository:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        if exc_type is None:
            self._connection.commit()
        else:
            self._connection.rollback()
        self.close()

    def _create_schema(self) -> None:
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS horizontal_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT NOT NULL,
                step INTEGER NOT NULL CHECK(step >= 0),
                timestamp TEXT NOT NULL,
                state_blob BLOB NOT NULL,
                dtype TEXT NOT NULL,
                shape_json TEXT NOT NULL,
                gate_mean REAL NOT NULL CHECK(gate_mean BETWEEN 0.0 AND 1.0),
                retention_mean REAL NOT NULL CHECK(retention_mean BETWEEN 0.0 AND 1.0),
                metadata_json TEXT NOT NULL,
                UNIQUE(run_id, step)
            )
            """
        )
        self._connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_horizontal_states_run_step "
            "ON horizontal_states(run_id, step)"
        )
        self._connection.commit()

    def append(
        self,
        *,
        run_id: str,
        step: int,
        state: NDArray[np.floating[Any]],
        gate_mean: float,
        retention_mean: float,
        metadata: dict[str, Any],
        timestamp: str | None = None,
    ) -> int:
        """Append one state atomically and return its database identifier."""
        if not run_id:
            raise ValueError("run_id must not be empty")
        if step < 0:
            raise ValueError("step must be non-negative")
        if not 0.0 <= gate_mean <= 1.0 or not 0.0 <= retention_mean <= 1.0:
            raise ValueError("gate values must be in [0, 1]")

        contiguous = np.ascontiguousarray(state, dtype=np.float32)
        if contiguous.ndim != 1 or contiguous.size == 0:
            raise ValueError("state must be a non-empty one-dimensional array")
        if not np.isfinite(contiguous).all():
            raise ValueError("state contains a non-finite value")

        recorded_at = timestamp or datetime.now(timezone.utc).isoformat()
        metadata_json = json.dumps(metadata, ensure_ascii=False, sort_keys=True)
        with self._connection:
            cursor = self._connection.execute(
                """
                INSERT INTO horizontal_states (
                    run_id, step, timestamp, state_blob, dtype, shape_json,
                    gate_mean, retention_mean, metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    step,
                    recorded_at,
                    sqlite3.Binary(contiguous.tobytes(order="C")),
                    contiguous.dtype.str,
                    json.dumps(contiguous.shape),
                    gate_mean,
                    retention_mean,
                    metadata_json,
                ),
            )
        return int(cursor.lastrowid)

    def get_run(self, run_id: str) -> list[StateRecord]:
        rows = self._connection.execute(
            "SELECT * FROM horizontal_states WHERE run_id = ? ORDER BY step ASC",
            (run_id,),
        ).fetchall()
        return [self._decode(row) for row in rows]

    def get_latest(self, run_id: str) -> StateRecord | None:
        row = self._connection.execute(
            "SELECT * FROM horizontal_states WHERE run_id = ? "
            "ORDER BY step DESC LIMIT 1",
            (run_id,),
        ).fetchone()
        return None if row is None else self._decode(row)

    def close(self) -> None:
        self._connection.close()

    @staticmethod
    def _decode(row: sqlite3.Row) -> StateRecord:
        dtype = np.dtype(row["dtype"])
        shape = tuple(json.loads(row["shape_json"]))
        state = np.frombuffer(row["state_blob"], dtype=dtype).reshape(shape).copy()
        return StateRecord(
            record_id=int(row["id"]),
            run_id=str(row["run_id"]),
            step=int(row["step"]),
            timestamp=str(row["timestamp"]),
            state=state,
            gate_mean=float(row["gate_mean"]),
            retention_mean=float(row["retention_mean"]),
            metadata=json.loads(row["metadata_json"]),
        )

