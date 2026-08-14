"""External witness attestations for the latest trust checkpoint state."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Sequence
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .asymmetric_auth import public_key_fingerprint, sign_payload_ed25519
from .role_verification import verify_role_signed_payload
from .trust_bundle import KeyRole, VerifiedTrustBundle


@dataclass(frozen=True, slots=True)
class VerifiedCheckpointAttestation:
    attestation_id: str
    witness_principal_id: str
    witness_key_id: str
    witness_sequence: int
    trust_bundle_generation: int
    trust_bundle_sha256: str
    previous_bundle_sha256: str | None
    witnessed_at: datetime


@dataclass(frozen=True, slots=True)
class CheckpointWitnessQuorum:
    satisfied: bool
    principal_ids: tuple[str, ...]
    reason_codes: tuple[str, ...]


class CheckpointWitnessStateStore:
    """Witness-owned monotonic state that refuses to re-attest rollback."""

    def __init__(self, database_path: Path, witness_principal_id: str) -> None:
        if not witness_principal_id or len(witness_principal_id) > 128:
            raise ValueError("invalid witness principal")
        if not database_path.parent.exists():
            raise ValueError("witness database parent must already exist")
        self.database_path = database_path
        self.witness_principal_id = witness_principal_id
        self._connection = sqlite3.connect(database_path, timeout=5.0)
        self._connection.execute("PRAGMA synchronous=FULL")
        self._connection.execute("PRAGMA journal_mode=DELETE")
        self._initialize()

    def __enter__(self) -> "CheckpointWitnessStateStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        self._connection.close()

    def attest(
        self,
        trust_bundle: VerifiedTrustBundle,
        *,
        witness_key_id: str,
        witness_private_key: Ed25519PrivateKey,
        witnessed_at: datetime,
    ) -> str:
        if witnessed_at.tzinfo is None:
            raise ValueError("witnessed_at must be timezone-aware")
        current = witnessed_at.astimezone(timezone.utc)
        record = trust_bundle.record_for(witness_key_id)
        if record is None or record.principal_id != self.witness_principal_id:
            raise ValueError("CHECKPOINT_WITNESS_PRINCIPAL_MISMATCH")
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            row = self._connection.execute(
                """
                SELECT generation, signed_bundle_sha256
                FROM witnessed_checkpoint ORDER BY generation DESC LIMIT 1
                """
            ).fetchone()
            if row is None:
                if (
                    trust_bundle.generation != 1
                    or trust_bundle.previous_bundle_sha256 is not None
                ):
                    raise ValueError("WITNESS_INITIAL_GENERATION_INVALID")
                self._insert_state(trust_bundle)
            else:
                latest_generation = int(row[0])
                latest_digest = str(row[1])
                if trust_bundle.generation < latest_generation:
                    raise ValueError("WITNESS_TRUST_BUNDLE_ROLLBACK")
                if trust_bundle.generation > latest_generation + 1:
                    raise ValueError("WITNESS_TRUST_BUNDLE_GENERATION_GAP")
                if trust_bundle.generation == latest_generation:
                    if trust_bundle.signed_bundle_sha256 != latest_digest:
                        raise ValueError("WITNESS_TRUST_STATE_CONFLICT")
                else:
                    if trust_bundle.previous_bundle_sha256 != latest_digest:
                        raise ValueError("WITNESS_PREVIOUS_DIGEST_MISMATCH")
                    self._insert_state(trust_bundle)
            sequence = int(
                self._connection.execute(
                    "SELECT COALESCE(MAX(sequence), 0) + 1 FROM witness_attestation"
                ).fetchone()[0]
            )
            signed = create_checkpoint_attestation(
                trust_bundle=trust_bundle,
                attestation_id=f"{self.witness_principal_id}-{sequence}",
                witness_principal_id=self.witness_principal_id,
                witness_sequence=sequence,
                witness_key_id=witness_key_id,
                witness_private_key=witness_private_key,
                witnessed_at=current,
            )
            self._connection.execute(
                """
                INSERT INTO witness_attestation(
                    sequence, generation, signed_bundle_sha256,
                    witnessed_at, signed_attestation_json
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    sequence,
                    trust_bundle.generation,
                    trust_bundle.signed_bundle_sha256,
                    current.isoformat(),
                    signed,
                ),
            )
            self._connection.commit()
            return signed
        except (sqlite3.DatabaseError, ValueError):
            self._connection.rollback()
            raise

    def _insert_state(self, trust_bundle: VerifiedTrustBundle) -> None:
        self._connection.execute(
            """
            INSERT INTO witnessed_checkpoint(
                generation, signed_bundle_sha256, previous_bundle_sha256
            ) VALUES (?, ?, ?)
            """,
            (
                trust_bundle.generation,
                trust_bundle.signed_bundle_sha256,
                trust_bundle.previous_bundle_sha256,
            ),
        )

    def _initialize(self) -> None:
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS witnessed_checkpoint (
                generation INTEGER PRIMARY KEY,
                signed_bundle_sha256 TEXT NOT NULL UNIQUE,
                previous_bundle_sha256 TEXT
            );
            CREATE TABLE IF NOT EXISTS witness_attestation (
                sequence INTEGER PRIMARY KEY,
                generation INTEGER NOT NULL,
                signed_bundle_sha256 TEXT NOT NULL,
                witnessed_at TEXT NOT NULL,
                signed_attestation_json TEXT NOT NULL
            );
            CREATE TRIGGER IF NOT EXISTS witnessed_checkpoint_no_update
            BEFORE UPDATE ON witnessed_checkpoint
            BEGIN SELECT RAISE(ABORT, 'append-only witnessed checkpoint'); END;
            CREATE TRIGGER IF NOT EXISTS witnessed_checkpoint_no_delete
            BEFORE DELETE ON witnessed_checkpoint
            BEGIN SELECT RAISE(ABORT, 'append-only witnessed checkpoint'); END;
            CREATE TRIGGER IF NOT EXISTS witness_attestation_no_update
            BEFORE UPDATE ON witness_attestation
            BEGIN SELECT RAISE(ABORT, 'append-only witness attestation'); END;
            CREATE TRIGGER IF NOT EXISTS witness_attestation_no_delete
            BEFORE DELETE ON witness_attestation
            BEGIN SELECT RAISE(ABORT, 'append-only witness attestation'); END;
            """
        )
        self._connection.commit()


def create_checkpoint_attestation(
    *,
    trust_bundle: VerifiedTrustBundle,
    attestation_id: str,
    witness_principal_id: str,
    witness_sequence: int,
    witness_key_id: str,
    witness_private_key: Ed25519PrivateKey,
    witnessed_at: datetime,
) -> str:
    if not attestation_id or len(attestation_id) > 128:
        raise ValueError("invalid attestation_id")
    if (
        not isinstance(witness_sequence, int)
        or isinstance(witness_sequence, bool)
        or witness_sequence <= 0
    ):
        raise ValueError("witness_sequence must be positive")
    if witnessed_at.tzinfo is None:
        raise ValueError("witnessed_at must be timezone-aware")
    current = witnessed_at.astimezone(timezone.utc)
    record = trust_bundle.record_for(witness_key_id)
    if record is None:
        raise ValueError("CHECKPOINT_WITNESS_KEY_UNKNOWN")
    if record.role is not KeyRole.WITNESS_SIGNER:
        raise ValueError("CHECKPOINT_WITNESS_ROLE_MISMATCH")
    if record.principal_id != witness_principal_id:
        raise ValueError("CHECKPOINT_WITNESS_PRINCIPAL_MISMATCH")
    if not record.active_at(current):
        raise ValueError("CHECKPOINT_WITNESS_KEY_NOT_ACTIVE")
    if public_key_fingerprint(witness_private_key.public_key()) != (
        public_key_fingerprint(record.public_key)
    ):
        raise ValueError("CHECKPOINT_WITNESS_PRIVATE_KEY_MISMATCH")
    payload = _canonical_json(
        {
            "attestation_id": attestation_id,
            "previous_bundle_sha256": trust_bundle.previous_bundle_sha256,
            "schema_version": "trust-checkpoint-attestation/1.0",
            "trust_bundle_generation": trust_bundle.generation,
            "trust_bundle_sha256": trust_bundle.signed_bundle_sha256,
            "witness_principal_id": witness_principal_id,
            "witness_sequence": witness_sequence,
            "witnessed_at": current.isoformat(),
        }
    )
    return sign_payload_ed25519(
        payload,
        key_id=witness_key_id,
        private_key=witness_private_key,
        issued_at=current,
        trust_bundle_generation=trust_bundle.generation,
        trust_bundle_sha256=trust_bundle.signed_bundle_sha256,
    )


def verify_checkpoint_attestation(
    signed_attestation_json: str,
    *,
    trust_bundle: VerifiedTrustBundle,
    signature_max_age: timedelta,
    now: datetime | None = None,
) -> tuple[VerifiedCheckpointAttestation | None, tuple[str, ...]]:
    verified = verify_role_signed_payload(
        signed_attestation_json,
        trust_bundle=trust_bundle,
        required_role=KeyRole.WITNESS_SIGNER,
        signature_max_age=signature_max_age,
        require_trust_binding=True,
        now=now,
    )
    if verified.payload_json is None or verified.key_record is None:
        return None, verified.reason_codes
    try:
        data = _strict_object(verified.payload_json)
        if set(data) != {
            "attestation_id",
            "previous_bundle_sha256",
            "schema_version",
            "trust_bundle_generation",
            "trust_bundle_sha256",
            "witness_principal_id",
            "witness_sequence",
            "witnessed_at",
        }:
            raise ValueError("unexpected checkpoint attestation fields")
        if data["schema_version"] != "trust-checkpoint-attestation/1.0":
            raise ValueError("unsupported checkpoint attestation schema")
        attestation_id = _identifier(data["attestation_id"])
        principal_id = _identifier(data["witness_principal_id"])
        if principal_id != verified.key_record.principal_id:
            return None, ("CHECKPOINT_WITNESS_PRINCIPAL_MISMATCH",)
        sequence = _positive_int(data["witness_sequence"])
        generation = _positive_int(data["trust_bundle_generation"])
        digest = _digest(data["trust_bundle_sha256"])
        previous_value = data["previous_bundle_sha256"]
        previous = None if previous_value is None else _digest(previous_value)
        witnessed_at = _time(data["witnessed_at"])
    except (TypeError, ValueError, json.JSONDecodeError):
        return None, ("CHECKPOINT_ATTESTATION_INVALID",)
    return (
        VerifiedCheckpointAttestation(
            attestation_id,
            principal_id,
            verified.key_record.key_id,
            sequence,
            generation,
            digest,
            previous,
            witnessed_at,
        ),
        (),
    )


def assess_checkpoint_witness_quorum(
    signed_attestations: Sequence[str],
    *,
    trust_bundle: VerifiedTrustBundle,
    minimum_principals: int,
    signature_max_age: timedelta,
    now: datetime | None = None,
) -> CheckpointWitnessQuorum:
    if minimum_principals < 2:
        return CheckpointWitnessQuorum(
            False,
            (),
            ("CHECKPOINT_WITNESS_QUORUM_CONFIG_INVALID",),
        )
    principals: set[str] = set()
    invalid_seen = False
    state_mismatch_seen = False
    for signed in signed_attestations:
        attestation, reasons = verify_checkpoint_attestation(
            signed,
            trust_bundle=trust_bundle,
            signature_max_age=signature_max_age,
            now=now,
        )
        if attestation is None:
            invalid_seen = invalid_seen or bool(reasons)
            continue
        if (
            attestation.trust_bundle_generation != trust_bundle.generation
            or attestation.trust_bundle_sha256
            != trust_bundle.signed_bundle_sha256
            or attestation.previous_bundle_sha256
            != trust_bundle.previous_bundle_sha256
        ):
            state_mismatch_seen = True
            continue
        principals.add(attestation.witness_principal_id)
    principal_ids = tuple(sorted(principals))
    if len(principal_ids) < minimum_principals:
        reasons = ["CHECKPOINT_WITNESS_QUORUM_NOT_REACHED"]
        if invalid_seen:
            reasons.append("INVALID_CHECKPOINT_ATTESTATION_IGNORED")
        if state_mismatch_seen:
            reasons.append("CHECKPOINT_ATTESTATION_STATE_MISMATCH")
        return CheckpointWitnessQuorum(False, principal_ids, tuple(reasons))
    return CheckpointWitnessQuorum(True, principal_ids, ())


def _strict_object(text: str) -> dict[str, object]:
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


def _identifier(value: object) -> str:
    if not isinstance(value, str) or not value or len(value) > 128:
        raise ValueError("invalid identifier")
    return value


def _positive_int(value: object) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError("positive integer required")
    return value


def _digest(value: object) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError("invalid digest")
    return value


def _time(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValueError("invalid time")
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("timezone required")
    return parsed.astimezone(timezone.utc)
