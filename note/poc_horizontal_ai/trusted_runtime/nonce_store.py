"""Persistent one-time request and nonce ledger owned by the trusted side."""

from __future__ import annotations

import hashlib
import hmac
import json
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


_SHA256 = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True, slots=True)
class NonceConsumeResult:
    accepted: bool
    sequence: int | None
    reason_codes: tuple[str, ...]


class PersistentNonceStore:
    def __init__(self, database_path: Path, integrity_key: bytes) -> None:
        if not database_path.parent.exists():
            raise ValueError("nonce database parent must already exist")
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

    def __enter__(self) -> "PersistentNonceStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        self._connection.close()

    def consume(
        self,
        *,
        request_id: str,
        nonce: str,
        issued_at: datetime,
        request_digest: str,
        consumed_at: datetime,
    ) -> NonceConsumeResult:
        if (
            not request_id
            or len(request_id) > 128
            or len(nonce) < 16
            or len(nonce) > 128
            or issued_at.tzinfo is None
            or consumed_at.tzinfo is None
            or consumed_at < issued_at
            or not _SHA256.fullmatch(request_digest)
        ):
            return NonceConsumeResult(False, None, ("NONCE_INPUT_INVALID",))
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            integrity_reasons = self.verify()
            if integrity_reasons:
                self._connection.rollback()
                return NonceConsumeResult(False, None, integrity_reasons)
            row = self._connection.execute(
                "SELECT sequence, row_mac FROM consumed_nonce ORDER BY sequence DESC LIMIT 1"
            ).fetchone()
            sequence = 1 if row is None else int(row[0]) + 1
            previous_mac = None if row is None else str(row[1])
            fields = {
                "consumed_at": _format_time(consumed_at),
                "issued_at": _format_time(issued_at),
                "nonce": nonce,
                "previous_mac": previous_mac,
                "request_digest": request_digest,
                "request_id": request_id,
                "sequence": sequence,
            }
            row_mac = _mac(self._integrity_key, fields)
            self._connection.execute(
                """
                INSERT INTO consumed_nonce(
                    sequence, request_id, nonce, issued_at, consumed_at,
                    request_digest, previous_mac, row_mac
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    sequence,
                    request_id,
                    nonce,
                    fields["issued_at"],
                    fields["consumed_at"],
                    request_digest,
                    previous_mac,
                    row_mac,
                ),
            )
            self._connection.commit()
            return NonceConsumeResult(True, sequence, ())
        except sqlite3.IntegrityError:
            self._connection.rollback()
            return NonceConsumeResult(
                False,
                None,
                ("NONCE_OR_REQUEST_REPLAY",),
            )
        except sqlite3.DatabaseError:
            self._connection.rollback()
            return NonceConsumeResult(False, None, ("NONCE_STORE_FAILURE",))

    def verify(self) -> tuple[str, ...]:
        previous_mac = None
        try:
            rows = self._connection.execute(
                """
                SELECT sequence, request_id, nonce, issued_at, consumed_at,
                       request_digest, previous_mac, row_mac
                FROM consumed_nonce ORDER BY sequence
                """
            ).fetchall()
        except sqlite3.DatabaseError:
            return ("NONCE_STORE_FAILURE",)
        for expected_sequence, row in enumerate(rows, 1):
            (
                sequence,
                request_id,
                nonce,
                issued_at,
                consumed_at,
                request_digest,
                stored_previous,
                row_mac,
            ) = row
            if sequence != expected_sequence or stored_previous != previous_mac:
                return ("NONCE_CHAIN_INVALID",)
            fields = {
                "consumed_at": consumed_at,
                "issued_at": issued_at,
                "nonce": nonce,
                "previous_mac": stored_previous,
                "request_digest": request_digest,
                "request_id": request_id,
                "sequence": sequence,
            }
            if not hmac.compare_digest(row_mac, _mac(self._integrity_key, fields)):
                return ("NONCE_CHAIN_INVALID",)
            previous_mac = row_mac
        return ()

    def _initialize(self) -> None:
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS consumed_nonce (
                sequence INTEGER PRIMARY KEY,
                request_id TEXT NOT NULL UNIQUE,
                nonce TEXT NOT NULL UNIQUE,
                issued_at TEXT NOT NULL,
                consumed_at TEXT NOT NULL,
                request_digest TEXT NOT NULL,
                previous_mac TEXT,
                row_mac TEXT NOT NULL
            );
            CREATE TRIGGER IF NOT EXISTS consumed_nonce_no_update
            BEFORE UPDATE ON consumed_nonce
            BEGIN SELECT RAISE(ABORT, 'append-only nonce ledger'); END;
            CREATE TRIGGER IF NOT EXISTS consumed_nonce_no_delete
            BEFORE DELETE ON consumed_nonce
            BEGIN SELECT RAISE(ABORT, 'append-only nonce ledger'); END;
            """
        )
        self._connection.commit()


def _validate_key(key: bytes) -> None:
    if not isinstance(key, bytes) or len(key) < 32:
        raise ValueError("integrity_key must contain at least 32 bytes")


def _format_time(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def _mac(key: bytes, fields: dict[str, object]) -> str:
    material = json.dumps(
        fields,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hmac.new(key, material, hashlib.sha256).hexdigest()
