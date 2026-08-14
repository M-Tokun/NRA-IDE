"""Persistent monotonic checkpoint for root-signed trust bundles."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Mapping

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from .trust_bundle import VerifiedTrustBundle, verify_signed_trust_bundle


@dataclass(frozen=True, slots=True)
class TrustCheckpointResult:
    accepted: bool
    bundle: VerifiedTrustBundle | None
    reason_codes: tuple[str, ...]


class TrustBundleCheckpointStore:
    def __init__(self, database_path: Path) -> None:
        if not database_path.parent.exists():
            raise ValueError("checkpoint database parent must already exist")
        self.database_path = database_path
        self._connection = sqlite3.connect(database_path, timeout=5.0)
        self._connection.execute("PRAGMA synchronous=FULL")
        self._connection.execute("PRAGMA journal_mode=DELETE")
        self._initialize()

    def __enter__(self) -> "TrustBundleCheckpointStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        self._connection.close()

    def accept(
        self,
        signed_bundle_json: str,
        *,
        pinned_root_keys: Mapping[str, Ed25519PublicKey],
        signature_max_age: timedelta,
        now: datetime | None = None,
    ) -> TrustCheckpointResult:
        if signature_max_age is None or signature_max_age <= timedelta(0):
            return TrustCheckpointResult(
                False,
                None,
                ("TRUST_CHECKPOINT_FRESHNESS_REQUIRED",),
            )
        verification = verify_signed_trust_bundle(
            signed_bundle_json,
            pinned_root_keys=pinned_root_keys,
            signature_max_age=signature_max_age,
            now=now,
        )
        if verification.bundle is None:
            return TrustCheckpointResult(False, None, verification.reason_codes)
        bundle = verification.bundle
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            row = self._connection.execute(
                """
                SELECT generation, signed_bundle_sha256
                FROM trust_checkpoint ORDER BY generation DESC LIMIT 1
                """
            ).fetchone()
            if row is None:
                if bundle.generation != 1 or bundle.previous_bundle_sha256 is not None:
                    self._connection.rollback()
                    return TrustCheckpointResult(
                        False,
                        None,
                        ("TRUST_CHECKPOINT_INITIAL_GENERATION_INVALID",),
                    )
            else:
                expected_generation = int(row[0]) + 1
                previous_digest = str(row[1])
                if bundle.generation < expected_generation:
                    self._connection.rollback()
                    return TrustCheckpointResult(
                        False,
                        None,
                        ("TRUST_BUNDLE_ROLLBACK",),
                    )
                if bundle.generation > expected_generation:
                    self._connection.rollback()
                    return TrustCheckpointResult(
                        False,
                        None,
                        ("TRUST_BUNDLE_GENERATION_GAP",),
                    )
                if bundle.previous_bundle_sha256 != previous_digest:
                    self._connection.rollback()
                    return TrustCheckpointResult(
                        False,
                        None,
                        ("TRUST_BUNDLE_PREVIOUS_DIGEST_MISMATCH",),
                    )
            self._connection.execute(
                """
                INSERT INTO trust_checkpoint(
                    generation, signed_bundle_sha256, previous_bundle_sha256,
                    issued_at, signed_bundle_json
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    bundle.generation,
                    bundle.signed_bundle_sha256,
                    bundle.previous_bundle_sha256,
                    bundle.issued_at.isoformat(),
                    signed_bundle_json,
                ),
            )
            self._connection.commit()
        except sqlite3.IntegrityError:
            self._connection.rollback()
            return TrustCheckpointResult(False, None, ("TRUST_BUNDLE_ROLLBACK",))
        except sqlite3.DatabaseError:
            self._connection.rollback()
            return TrustCheckpointResult(False, None, ("TRUST_CHECKPOINT_FAILURE",))
        return TrustCheckpointResult(True, bundle, ())

    def verify(
        self,
        *,
        pinned_root_keys: Mapping[str, Ed25519PublicKey],
        signature_max_age: timedelta | None = None,
        now: datetime | None = None,
    ) -> tuple[str, ...]:
        try:
            rows = self._connection.execute(
                """
                SELECT generation, signed_bundle_sha256, previous_bundle_sha256,
                       signed_bundle_json
                FROM trust_checkpoint ORDER BY generation
                """
            ).fetchall()
        except sqlite3.DatabaseError:
            return ("TRUST_CHECKPOINT_FAILURE",)
        previous_digest = None
        for expected_generation, row in enumerate(rows, 1):
            generation, digest, stored_previous, signed_json = row
            if generation != expected_generation or stored_previous != previous_digest:
                return ("TRUST_CHECKPOINT_CHAIN_INVALID",)
            verification = verify_signed_trust_bundle(
                signed_json,
                pinned_root_keys=pinned_root_keys,
                signature_max_age=signature_max_age,
                now=now,
            )
            if verification.bundle is None:
                return ("TRUST_CHECKPOINT_SIGNATURE_INVALID",)
            bundle = verification.bundle
            if (
                bundle.generation != generation
                or bundle.signed_bundle_sha256 != digest
                or bundle.previous_bundle_sha256 != stored_previous
            ):
                return ("TRUST_CHECKPOINT_CHAIN_INVALID",)
            previous_digest = digest
        return ()

    def latest_signed_bundle(self) -> str | None:
        row = self._connection.execute(
            "SELECT signed_bundle_json FROM trust_checkpoint ORDER BY generation DESC LIMIT 1"
        ).fetchone()
        return None if row is None else str(row[0])

    def _initialize(self) -> None:
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS trust_checkpoint (
                generation INTEGER PRIMARY KEY,
                signed_bundle_sha256 TEXT NOT NULL UNIQUE,
                previous_bundle_sha256 TEXT,
                issued_at TEXT NOT NULL,
                signed_bundle_json TEXT NOT NULL
            );
            CREATE TRIGGER IF NOT EXISTS trust_checkpoint_no_update
            BEFORE UPDATE ON trust_checkpoint
            BEGIN SELECT RAISE(ABORT, 'append-only trust checkpoint'); END;
            CREATE TRIGGER IF NOT EXISTS trust_checkpoint_no_delete
            BEFORE DELETE ON trust_checkpoint
            BEGIN SELECT RAISE(ABORT, 'append-only trust checkpoint'); END;
            """
        )
        self._connection.commit()
