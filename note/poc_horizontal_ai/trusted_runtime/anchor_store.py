"""Append-only authenticated audit-head anchor store for the PoC."""

from __future__ import annotations

import hashlib
import hmac
import json
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, TypeVar


_SHA256 = re.compile(r"[0-9a-f]{64}")
_T = TypeVar("_T")


@dataclass(frozen=True, slots=True)
class AnchorReceipt:
    sequence: int
    anchor_id: str
    audit_head_digest: str
    event_count: int
    bundle_sha256: str
    anchored_at: str
    previous_receipt_mac: str | None
    receipt_mac: str


class AuditAnchorStore:
    def __init__(self, database_path: Path, integrity_key: bytes) -> None:
        if not database_path.parent.exists():
            raise ValueError("anchor database parent must already exist")
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

    def __enter__(self) -> "AuditAnchorStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        self._connection.close()

    def append(
        self,
        *,
        anchor_id: str,
        audit_head_digest: str,
        event_count: int,
        bundle_sha256: str,
        anchored_at: datetime,
    ) -> AnchorReceipt:
        return self.append_finalized(
            anchor_id=anchor_id,
            audit_head_digest=audit_head_digest,
            event_count=event_count,
            bundle_sha256=bundle_sha256,
            anchored_at=anchored_at,
            finalizer=lambda receipt: receipt,
        )

    def append_finalized(
        self,
        *,
        anchor_id: str,
        audit_head_digest: str,
        event_count: int,
        bundle_sha256: str,
        anchored_at: datetime,
        finalizer: Callable[[AnchorReceipt], _T],
    ) -> _T:
        if (
            not anchor_id
            or len(anchor_id) > 128
            or not _SHA256.fullmatch(audit_head_digest)
            or not _SHA256.fullmatch(bundle_sha256)
            or not isinstance(event_count, int)
            or isinstance(event_count, bool)
            or event_count <= 0
            or anchored_at.tzinfo is None
        ):
            raise ValueError("invalid audit anchor input")
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            integrity_reasons = self.verify()
            if integrity_reasons:
                self._connection.rollback()
                raise ValueError(",".join(integrity_reasons))
            row = self._connection.execute(
                "SELECT sequence, receipt_mac FROM audit_anchor ORDER BY sequence DESC LIMIT 1"
            ).fetchone()
            sequence = 1 if row is None else int(row[0]) + 1
            previous = None if row is None else str(row[1])
            fields = {
                "anchor_id": anchor_id,
                "anchored_at": anchored_at.astimezone(timezone.utc).isoformat(),
                "audit_head_digest": audit_head_digest,
                "bundle_sha256": bundle_sha256,
                "event_count": event_count,
                "previous_receipt_mac": previous,
                "sequence": sequence,
            }
            receipt_mac = _mac(self._integrity_key, fields)
            self._connection.execute(
                """
                INSERT INTO audit_anchor(
                    sequence, anchor_id, audit_head_digest, event_count,
                    bundle_sha256, anchored_at, previous_receipt_mac, receipt_mac
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    sequence,
                    anchor_id,
                    audit_head_digest,
                    event_count,
                    bundle_sha256,
                    fields["anchored_at"],
                    previous,
                    receipt_mac,
                ),
            )
            receipt = AnchorReceipt(
                sequence,
                anchor_id,
                audit_head_digest,
                event_count,
                bundle_sha256,
                fields["anchored_at"],
                previous,
                receipt_mac,
            )
            finalized = finalizer(receipt)
            self._connection.commit()
        except sqlite3.IntegrityError as error:
            self._connection.rollback()
            raise ValueError("anchor_id or audit_head_digest already anchored") from error
        except Exception:
            self._connection.rollback()
            raise
        return finalized

    def verify(self) -> tuple[str, ...]:
        previous = None
        try:
            rows = self._connection.execute(
                """
                SELECT sequence, anchor_id, audit_head_digest, event_count,
                       bundle_sha256, anchored_at, previous_receipt_mac, receipt_mac
                FROM audit_anchor ORDER BY sequence
                """
            ).fetchall()
        except sqlite3.DatabaseError:
            return ("ANCHOR_STORE_FAILURE",)
        for expected_sequence, row in enumerate(rows, 1):
            (
                sequence,
                anchor_id,
                audit_head_digest,
                event_count,
                bundle_sha256,
                anchored_at,
                stored_previous,
                receipt_mac,
            ) = row
            if sequence != expected_sequence or stored_previous != previous:
                return ("ANCHOR_CHAIN_INVALID",)
            fields = {
                "anchor_id": anchor_id,
                "anchored_at": anchored_at,
                "audit_head_digest": audit_head_digest,
                "bundle_sha256": bundle_sha256,
                "event_count": event_count,
                "previous_receipt_mac": stored_previous,
                "sequence": sequence,
            }
            if not hmac.compare_digest(
                receipt_mac,
                _mac(self._integrity_key, fields),
            ):
                return ("ANCHOR_CHAIN_INVALID",)
            previous = receipt_mac
        return ()

    def _initialize(self) -> None:
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS audit_anchor (
                sequence INTEGER PRIMARY KEY,
                anchor_id TEXT NOT NULL UNIQUE,
                audit_head_digest TEXT NOT NULL UNIQUE,
                event_count INTEGER NOT NULL,
                bundle_sha256 TEXT NOT NULL,
                anchored_at TEXT NOT NULL,
                previous_receipt_mac TEXT,
                receipt_mac TEXT NOT NULL
            );
            CREATE TRIGGER IF NOT EXISTS audit_anchor_no_update
            BEFORE UPDATE ON audit_anchor
            BEGIN SELECT RAISE(ABORT, 'append-only audit anchor'); END;
            CREATE TRIGGER IF NOT EXISTS audit_anchor_no_delete
            BEFORE DELETE ON audit_anchor
            BEGIN SELECT RAISE(ABORT, 'append-only audit anchor'); END;
            """
        )
        self._connection.commit()


def verify_anchor_receipt(receipt: AnchorReceipt, integrity_key: bytes) -> bool:
    try:
        _validate_key(integrity_key)
        fields = {
            "anchor_id": receipt.anchor_id,
            "anchored_at": receipt.anchored_at,
            "audit_head_digest": receipt.audit_head_digest,
            "bundle_sha256": receipt.bundle_sha256,
            "event_count": receipt.event_count,
            "previous_receipt_mac": receipt.previous_receipt_mac,
            "sequence": receipt.sequence,
        }
        return hmac.compare_digest(receipt.receipt_mac, _mac(integrity_key, fields))
    except (AttributeError, TypeError, ValueError):
        return False


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
