"""Independent-principal attestations for irreversible latch heads."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Sequence

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .asymmetric_auth import public_key_fingerprint, sign_payload_ed25519
from .irreversible_latch_store import IrreversibleLatchHead
from .role_verification import verify_role_signed_payload
from .trust_bundle import KeyRole, VerifiedTrustBundle


@dataclass(frozen=True, slots=True)
class VerifiedLatchWitnessAttestation:
    attestation_id: str
    witness_principal_id: str
    witness_key_id: str
    witness_sequence: int
    latch_store_id: str
    latch_sequence: int
    previous_latch_mac: str | None
    latch_head_mac: str
    latch_checkpoint_sha256: str
    admission_challenge: str | None
    witnessed_at: datetime


@dataclass(frozen=True, slots=True)
class LatchWitnessQuorum:
    satisfied: bool
    principal_ids: tuple[str, ...]
    reason_codes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class VerifiedSignedLatchCheckpoint:
    checkpoint_id: str
    signer_key_id: str
    latch_store_id: str
    head: IrreversibleLatchHead
    checkpointed_at: datetime


def create_signed_latch_checkpoint(
    head: IrreversibleLatchHead,
    *,
    checkpoint_id: str,
    latch_store_id: str,
    signing_key_id: str,
    signing_private_key: Ed25519PrivateKey,
    trust_bundle: VerifiedTrustBundle,
    checkpointed_at: datetime,
) -> str:
    if (
        not _identifier(checkpoint_id)
        or not _identifier(latch_store_id)
        or checkpointed_at.tzinfo is None
    ):
        raise ValueError("invalid signed latch checkpoint metadata")
    _validate_checkpoint_head(head, latch_store_id)
    _validate_role_identity(
        trust_bundle,
        key_id=signing_key_id,
        principal_id=None,
        private_key=signing_private_key,
        required_role=KeyRole.LATCH_CHECKPOINT_SIGNER,
        occurred_at=checkpointed_at,
    )
    current = checkpointed_at.astimezone(timezone.utc)
    payload = _canonical_json(
        {
            "checkpoint_id": checkpoint_id,
            "checkpointed_at": current.isoformat(),
            "latch_head_mac": head.row_mac,
            "latch_sequence": head.sequence,
            "latch_store_id": latch_store_id,
            "previous_latch_mac": head.previous_mac,
            "schema_version": "signed-latch-checkpoint/1.0",
        }
    )
    return sign_payload_ed25519(
        payload,
        key_id=signing_key_id,
        private_key=signing_private_key,
        issued_at=current,
        trust_bundle_generation=trust_bundle.generation,
        trust_bundle_sha256=trust_bundle.signed_bundle_sha256,
    )


def create_signed_latch_genesis(
    *,
    checkpoint_id: str,
    latch_store_id: str,
    signing_key_id: str,
    signing_private_key: Ed25519PrivateKey,
    trust_bundle: VerifiedTrustBundle,
    checkpointed_at: datetime,
) -> str:
    """Sign the externally registered empty state for a new latch store."""
    return create_signed_latch_checkpoint(
        genesis_latch_head(latch_store_id),
        checkpoint_id=checkpoint_id,
        latch_store_id=latch_store_id,
        signing_key_id=signing_key_id,
        signing_private_key=signing_private_key,
        trust_bundle=trust_bundle,
        checkpointed_at=checkpointed_at,
    )


def genesis_latch_head(latch_store_id: str) -> IrreversibleLatchHead:
    if not _identifier(latch_store_id):
        raise ValueError("invalid latch_store_id")
    digest = hashlib.sha256(
        _canonical_json(
            {
                "latch_store_id": latch_store_id,
                "schema_version": "irreversible-latch-genesis/1.0",
            }
        ).encode("utf-8")
    ).hexdigest()
    return IrreversibleLatchHead(0, None, digest)


def verify_signed_latch_checkpoint(
    signed_checkpoint_json: str,
    *,
    trust_bundle: VerifiedTrustBundle,
    signature_max_age: timedelta,
    now: datetime | None = None,
) -> tuple[VerifiedSignedLatchCheckpoint | None, tuple[str, ...]]:
    verified = verify_role_signed_payload(
        signed_checkpoint_json,
        trust_bundle=trust_bundle,
        required_role=KeyRole.LATCH_CHECKPOINT_SIGNER,
        signature_max_age=signature_max_age,
        require_trust_binding=True,
        now=now,
    )
    if verified.payload_json is None or verified.key_record is None:
        return None, verified.reason_codes
    try:
        data = json.loads(verified.payload_json, object_pairs_hook=_pairs_hook)
        if not isinstance(data, dict) or set(data) != {
            "checkpoint_id",
            "checkpointed_at",
            "latch_head_mac",
            "latch_sequence",
            "latch_store_id",
            "previous_latch_mac",
            "schema_version",
        }:
            raise ValueError
        if data["schema_version"] != "signed-latch-checkpoint/1.0":
            raise ValueError
        latch_store_id = data["latch_store_id"]
        head = IrreversibleLatchHead(
            data["latch_sequence"],
            data["previous_latch_mac"],
            data["latch_head_mac"],
        )
        if (
            not _identifier(data["checkpoint_id"])
            or not _identifier(latch_store_id)
        ):
            raise ValueError
        _validate_checkpoint_head(head, latch_store_id)
        return (
            VerifiedSignedLatchCheckpoint(
                data["checkpoint_id"],
                verified.key_record.key_id,
                latch_store_id,
                head,
                _time(data["checkpointed_at"]),
            ),
            (),
        )
    except (TypeError, ValueError, json.JSONDecodeError):
        return None, ("SIGNED_LATCH_CHECKPOINT_INVALID",)


class LatchCheckpointWitnessStateStore:
    """Witness-owned monotonic state that refuses to sign latch rollback."""

    def __init__(
        self,
        database_path: Path,
        witness_principal_id: str,
        latch_store_id: str,
    ) -> None:
        if database_path.is_symlink():
            raise ValueError("latch witness database must not be a symlink")
        if not database_path.parent.exists():
            raise ValueError("latch witness database parent must already exist")
        if not _identifier(witness_principal_id) or not _identifier(latch_store_id):
            raise ValueError("invalid latch witness principal")
        self.database_path = database_path
        self.witness_principal_id = witness_principal_id
        self.latch_store_id = latch_store_id
        self._connection = sqlite3.connect(database_path, timeout=5.0)
        self._connection.execute("PRAGMA synchronous=FULL")
        self._connection.execute("PRAGMA journal_mode=DELETE")
        self._initialize()
        stored_scope = self._connection.execute(
            "SELECT latch_store_id FROM witness_scope WHERE singleton = 1"
        ).fetchone()
        if stored_scope is None or stored_scope[0] != latch_store_id:
            self.close()
            raise ValueError("LATCH_WITNESS_SCOPE_MISMATCH")
        reasons = self.verify()
        if reasons:
            self.close()
            raise ValueError(",".join(reasons))

    def __enter__(self) -> "LatchCheckpointWitnessStateStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        self._connection.close()

    def attest(
        self,
        signed_checkpoints: Sequence[str],
        *,
        trust_bundle: VerifiedTrustBundle,
        checkpoint_signature_max_age: timedelta,
        witness_key_id: str,
        witness_private_key: Ed25519PrivateKey,
        witnessed_at: datetime,
        admission_challenge: str | None = None,
    ) -> str:
        signed_segment = tuple(signed_checkpoints)
        if not signed_segment or witnessed_at.tzinfo is None:
            raise ValueError("invalid latch witness request")
        verified_segment: list[VerifiedSignedLatchCheckpoint] = []
        for signed_checkpoint in signed_segment:
            verified_checkpoint, checkpoint_reasons = (
                verify_signed_latch_checkpoint(
                    signed_checkpoint,
                    trust_bundle=trust_bundle,
                    signature_max_age=checkpoint_signature_max_age,
                    now=witnessed_at,
                )
            )
            if verified_checkpoint is None:
                raise ValueError(",".join(checkpoint_reasons))
            verified_segment.append(verified_checkpoint)
        if any(
            item.latch_store_id != self.latch_store_id
            for item in verified_segment
        ):
            raise ValueError("LATCH_WITNESS_SCOPE_MISMATCH")
        segment = tuple(item.head for item in verified_segment)
        _validate_witness_identity(
            trust_bundle,
            witness_key_id=witness_key_id,
            witness_principal_id=self.witness_principal_id,
            witness_private_key=witness_private_key,
            witnessed_at=witnessed_at,
        )
        for verified_checkpoint in verified_segment:
            _validate_checkpoint_head(
                verified_checkpoint.head,
                verified_checkpoint.latch_store_id,
            )
        _validate_latch_segment_order(segment)
        if admission_challenge is not None and not _digest(admission_challenge):
            raise ValueError("invalid admission challenge")

        try:
            self._connection.execute("BEGIN IMMEDIATE")
            reasons = self.verify()
            if reasons:
                raise ValueError(",".join(reasons))
            row = self._connection.execute(
                "SELECT sequence, previous_mac, row_mac FROM witnessed_latch "
                "ORDER BY sequence DESC LIMIT 1"
            ).fetchone()
            if row is None:
                latest_sequence = -1
                expected_sequence = 0 if segment[0].sequence == 0 else 1
                expected_previous = None
            else:
                latest_sequence = int(row[0])
                latest_previous = row[1]
                latest_mac = str(row[2])
                expected_sequence = latest_sequence + 1
                expected_previous = None if latest_sequence == 0 else latest_mac

            pending: list[IrreversibleLatchHead] = []
            for head in segment:
                if head.sequence <= latest_sequence:
                    stored = self._connection.execute(
                        "SELECT previous_mac, row_mac FROM witnessed_latch "
                        "WHERE sequence = ?",
                        (head.sequence,),
                    ).fetchone()
                    if (
                        stored is None
                        and head.sequence == 0
                        and latest_sequence >= 1
                    ):
                        continue
                    if (
                        stored is None
                        or stored[0] != head.previous_mac
                        or str(stored[1]) != head.row_mac
                    ):
                        raise ValueError("LATCH_WITNESS_STATE_CONFLICT")
                    continue
                pending.append(head)

            if not pending and segment[-1].sequence < latest_sequence:
                raise ValueError("LATCH_WITNESS_ROLLBACK")

            if pending:
                for head in pending:
                    if (
                        head.sequence != expected_sequence
                        or head.previous_mac != expected_previous
                    ):
                        raise ValueError("LATCH_WITNESS_CHAIN_INVALID")
                    self._connection.execute(
                        "INSERT INTO witnessed_latch(sequence, previous_mac, row_mac) "
                        "VALUES (?, ?, ?)",
                        (head.sequence, head.previous_mac, head.row_mac),
                    )
                    expected_sequence += 1
                    expected_previous = (
                        None if head.sequence == 0 else head.row_mac
                    )

            final_head = segment[-1]
            stored = self._connection.execute(
                "SELECT row_mac FROM witnessed_latch WHERE sequence = ?",
                (final_head.sequence,),
            ).fetchone()
            if stored is None or str(stored[0]) != final_head.row_mac:
                raise ValueError("LATCH_WITNESS_STATE_CONFLICT")
            witness_sequence = int(
                self._connection.execute(
                    "SELECT COALESCE(MAX(sequence), 0) + 1 "
                    "FROM latch_witness_attestation"
                ).fetchone()[0]
            )
            signed = create_latch_witness_attestation(
                signed_segment[-1],
                attestation_id=f"{self.witness_principal_id}-{witness_sequence}",
                witness_principal_id=self.witness_principal_id,
                witness_sequence=witness_sequence,
                witness_key_id=witness_key_id,
                witness_private_key=witness_private_key,
                trust_bundle=trust_bundle,
                checkpoint_signature_max_age=checkpoint_signature_max_age,
                witnessed_at=witnessed_at,
                admission_challenge=admission_challenge,
            )
            self._connection.execute(
                """
                INSERT INTO latch_witness_attestation(
                    sequence, latch_sequence, latch_head_mac,
                    witnessed_at, signed_attestation_json
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    witness_sequence,
                    final_head.sequence,
                    final_head.row_mac,
                    witnessed_at.astimezone(timezone.utc).isoformat(),
                    signed,
                ),
            )
            self._connection.commit()
            return signed
        except (sqlite3.DatabaseError, ValueError):
            self._connection.rollback()
            raise

    def verify(self) -> tuple[str, ...]:
        try:
            rows = self._connection.execute(
                "SELECT sequence, previous_mac, row_mac "
                "FROM witnessed_latch ORDER BY sequence"
            ).fetchall()
        except sqlite3.DatabaseError:
            return ("LATCH_WITNESS_STORE_FAILURE",)
        if rows and int(rows[0][0]) == 0:
            sequence, stored_previous, row_mac = rows.pop(0)
            if (
                sequence != 0
                or stored_previous is not None
                or row_mac != genesis_latch_head(self.latch_store_id).row_mac
            ):
                return ("LATCH_WITNESS_CHAIN_INVALID",)
        previous_mac = None
        for expected_sequence, row in enumerate(rows, 1):
            sequence, stored_previous, row_mac = row
            if (
                sequence != expected_sequence
                or stored_previous != previous_mac
                or not _digest(row_mac)
                or (stored_previous is not None and not _digest(stored_previous))
            ):
                return ("LATCH_WITNESS_CHAIN_INVALID",)
            previous_mac = row_mac
        return ()

    def _initialize(self) -> None:
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS witness_scope (
                singleton INTEGER PRIMARY KEY CHECK(singleton = 1),
                latch_store_id TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS witnessed_latch (
                sequence INTEGER PRIMARY KEY,
                previous_mac TEXT,
                row_mac TEXT NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS latch_witness_attestation (
                sequence INTEGER PRIMARY KEY,
                latch_sequence INTEGER NOT NULL,
                latch_head_mac TEXT NOT NULL,
                witnessed_at TEXT NOT NULL,
                signed_attestation_json TEXT NOT NULL
            );
            CREATE TRIGGER IF NOT EXISTS witnessed_latch_no_update
            BEFORE UPDATE ON witnessed_latch
            BEGIN SELECT RAISE(ABORT, 'append-only witnessed latch'); END;
            CREATE TRIGGER IF NOT EXISTS witnessed_latch_no_delete
            BEFORE DELETE ON witnessed_latch
            BEGIN SELECT RAISE(ABORT, 'append-only witnessed latch'); END;
            CREATE TRIGGER IF NOT EXISTS latch_witness_attestation_no_update
            BEFORE UPDATE ON latch_witness_attestation
            BEGIN SELECT RAISE(ABORT, 'append-only latch attestation'); END;
            CREATE TRIGGER IF NOT EXISTS latch_witness_attestation_no_delete
            BEFORE DELETE ON latch_witness_attestation
            BEGIN SELECT RAISE(ABORT, 'append-only latch attestation'); END;
            CREATE TRIGGER IF NOT EXISTS witness_scope_no_update
            BEFORE UPDATE ON witness_scope
            BEGIN SELECT RAISE(ABORT, 'fixed latch witness scope'); END;
            CREATE TRIGGER IF NOT EXISTS witness_scope_no_delete
            BEFORE DELETE ON witness_scope
            BEGIN SELECT RAISE(ABORT, 'fixed latch witness scope'); END;
            """
        )
        self._connection.execute(
            "INSERT OR IGNORE INTO witness_scope(singleton, latch_store_id) "
            "VALUES (1, ?)",
            (self.latch_store_id,),
        )
        self._connection.commit()


def create_latch_witness_attestation(
    signed_latch_checkpoint_json: str,
    *,
    attestation_id: str,
    witness_principal_id: str,
    witness_sequence: int,
    witness_key_id: str,
    witness_private_key: Ed25519PrivateKey,
    trust_bundle: VerifiedTrustBundle,
    checkpoint_signature_max_age: timedelta,
    witnessed_at: datetime,
    admission_challenge: str | None = None,
) -> str:
    verified_checkpoint, checkpoint_reasons = verify_signed_latch_checkpoint(
        signed_latch_checkpoint_json,
        trust_bundle=trust_bundle,
        signature_max_age=checkpoint_signature_max_age,
        now=witnessed_at,
    )
    if verified_checkpoint is None:
        raise ValueError(",".join(checkpoint_reasons))
    head = verified_checkpoint.head
    checkpoint_sha256 = hashlib.sha256(
        signed_latch_checkpoint_json.encode("utf-8")
    ).hexdigest()
    if not _identifier(attestation_id) or not _identifier(witness_principal_id):
        raise ValueError("invalid latch witness attestation identity")
    if (
        not isinstance(witness_sequence, int)
        or isinstance(witness_sequence, bool)
        or witness_sequence <= 0
        or witnessed_at.tzinfo is None
    ):
        raise ValueError("invalid latch witness attestation metadata")
    if admission_challenge is not None and not _digest(admission_challenge):
        raise ValueError("invalid admission challenge")
    _validate_witness_identity(
        trust_bundle,
        witness_key_id=witness_key_id,
        witness_principal_id=witness_principal_id,
        witness_private_key=witness_private_key,
        witnessed_at=witnessed_at,
    )
    current = witnessed_at.astimezone(timezone.utc)
    payload = _canonical_json(
        {
            "admission_challenge": admission_challenge,
            "attestation_id": attestation_id,
            "latch_checkpoint_sha256": checkpoint_sha256,
            "latch_head_mac": head.row_mac,
            "latch_sequence": head.sequence,
            "latch_store_id": verified_checkpoint.latch_store_id,
            "previous_latch_mac": head.previous_mac,
            "schema_version": "latch-witness-attestation/1.1",
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


def verify_latch_witness_attestation(
    signed_attestation_json: str,
    *,
    trust_bundle: VerifiedTrustBundle,
    signature_max_age: timedelta,
    now: datetime | None = None,
) -> tuple[VerifiedLatchWitnessAttestation | None, tuple[str, ...]]:
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
        data = json.loads(verified.payload_json, object_pairs_hook=_pairs_hook)
        if not isinstance(data, dict) or set(data) != {
            "admission_challenge",
            "attestation_id",
            "latch_checkpoint_sha256",
            "latch_head_mac",
            "latch_sequence",
            "latch_store_id",
            "previous_latch_mac",
            "schema_version",
            "witness_principal_id",
            "witness_sequence",
            "witnessed_at",
        }:
            raise ValueError
        if data["schema_version"] != "latch-witness-attestation/1.1":
            raise ValueError
        principal_id = data["witness_principal_id"]
        head = IrreversibleLatchHead(
            data["latch_sequence"],
            data["previous_latch_mac"],
            data["latch_head_mac"],
        )
        if (
            not _identifier(data["attestation_id"])
            or not _identifier(principal_id)
            or principal_id != verified.key_record.principal_id
            or not _positive_int(data["witness_sequence"])
            or not _identifier(data["latch_store_id"])
            or not _digest(data["latch_checkpoint_sha256"])
            or not _digest(data["latch_head_mac"])
            or (
                data["admission_challenge"] is not None
                and not _digest(data["admission_challenge"])
            )
        ):
            raise ValueError
        _validate_checkpoint_head(head, data["latch_store_id"])
        witnessed_at = _time(data["witnessed_at"])
        return (
            VerifiedLatchWitnessAttestation(
                data["attestation_id"],
                principal_id,
                verified.key_record.key_id,
                data["witness_sequence"],
                data["latch_store_id"],
                data["latch_sequence"],
                data["previous_latch_mac"],
                data["latch_head_mac"],
                data["latch_checkpoint_sha256"],
                data["admission_challenge"],
                witnessed_at,
            ),
            (),
        )
    except (TypeError, ValueError, json.JSONDecodeError):
        return None, ("LATCH_WITNESS_ATTESTATION_INVALID",)


def assess_latch_witness_quorum(
    signed_attestations: Sequence[str],
    *,
    signed_latch_checkpoint_json: str,
    trust_bundle: VerifiedTrustBundle,
    minimum_principals: int,
    signature_max_age: timedelta,
    expected_admission_challenge: str | None = None,
    now: datetime | None = None,
) -> LatchWitnessQuorum:
    verified_checkpoint, checkpoint_reasons = verify_signed_latch_checkpoint(
        signed_latch_checkpoint_json,
        trust_bundle=trust_bundle,
        signature_max_age=signature_max_age,
        now=now,
    )
    if verified_checkpoint is None:
        return LatchWitnessQuorum(False, (), checkpoint_reasons)
    head = verified_checkpoint.head
    checkpoint_sha256 = hashlib.sha256(
        signed_latch_checkpoint_json.encode("utf-8")
    ).hexdigest()
    if minimum_principals < 2:
        return LatchWitnessQuorum(
            False,
            (),
            ("LATCH_WITNESS_QUORUM_CONFIG_INVALID",),
        )
    principals: set[str] = set()
    invalid_seen = False
    state_mismatch_seen = False
    for signed in signed_attestations:
        attestation, reasons = verify_latch_witness_attestation(
            signed,
            trust_bundle=trust_bundle,
            signature_max_age=signature_max_age,
            now=now,
        )
        if attestation is None:
            invalid_seen = invalid_seen or bool(reasons)
            continue
        if (
            attestation.latch_store_id != verified_checkpoint.latch_store_id
            or attestation.latch_sequence != head.sequence
            or attestation.previous_latch_mac != head.previous_mac
            or attestation.latch_head_mac != head.row_mac
            or attestation.latch_checkpoint_sha256 != checkpoint_sha256
            or attestation.admission_challenge != expected_admission_challenge
        ):
            state_mismatch_seen = True
            continue
        principals.add(attestation.witness_principal_id)
    principal_ids = tuple(sorted(principals))
    if len(principal_ids) < minimum_principals:
        reasons = ["LATCH_WITNESS_QUORUM_NOT_REACHED"]
        if invalid_seen:
            reasons.append("INVALID_LATCH_WITNESS_ATTESTATION_IGNORED")
        if state_mismatch_seen:
            reasons.append("LATCH_WITNESS_STATE_MISMATCH")
        return LatchWitnessQuorum(False, principal_ids, tuple(reasons))
    return LatchWitnessQuorum(True, principal_ids, ())


def _validate_witness_identity(
    trust_bundle: VerifiedTrustBundle,
    *,
    witness_key_id: str,
    witness_principal_id: str,
    witness_private_key: Ed25519PrivateKey,
    witnessed_at: datetime,
) -> None:
    _validate_role_identity(
        trust_bundle,
        key_id=witness_key_id,
        principal_id=witness_principal_id,
        private_key=witness_private_key,
        required_role=KeyRole.WITNESS_SIGNER,
        occurred_at=witnessed_at,
    )


def _validate_role_identity(
    trust_bundle: VerifiedTrustBundle,
    *,
    key_id: str,
    principal_id: str | None,
    private_key: Ed25519PrivateKey,
    required_role: KeyRole,
    occurred_at: datetime,
) -> None:
    current = occurred_at.astimezone(timezone.utc)
    record = trust_bundle.record_for(key_id)
    if record is None:
        raise ValueError("LATCH_SIGNING_KEY_UNKNOWN")
    if record.role is not required_role:
        raise ValueError("LATCH_SIGNING_ROLE_MISMATCH")
    if principal_id is not None and record.principal_id != principal_id:
        raise ValueError("LATCH_SIGNING_PRINCIPAL_MISMATCH")
    if not record.active_at(current):
        raise ValueError("LATCH_SIGNING_KEY_NOT_ACTIVE")
    if public_key_fingerprint(private_key.public_key()) != (
        public_key_fingerprint(record.public_key)
    ):
        raise ValueError("LATCH_SIGNING_PRIVATE_KEY_MISMATCH")


def _validate_head(head: IrreversibleLatchHead) -> None:
    if (
        not isinstance(head, IrreversibleLatchHead)
        or not _positive_int(head.sequence)
        or not _digest(head.row_mac)
        or (head.previous_mac is not None and not _digest(head.previous_mac))
        or (head.sequence == 1) != (head.previous_mac is None)
    ):
        raise ValueError("invalid irreversible latch head")


def _validate_checkpoint_head(
    head: IrreversibleLatchHead,
    latch_store_id: str,
) -> None:
    if head.sequence == 0:
        if head != genesis_latch_head(latch_store_id):
            raise ValueError("invalid irreversible latch genesis")
        return
    _validate_head(head)


def _validate_latch_segment_order(
    segment: Sequence[IrreversibleLatchHead],
) -> None:
    for previous, current in zip(segment, segment[1:]):
        expected_previous = (
            None if previous.sequence == 0 else previous.row_mac
        )
        if (
            current.sequence != previous.sequence + 1
            or current.previous_mac != expected_previous
        ):
            raise ValueError("LATCH_WITNESS_CHAIN_INVALID")


def _identifier(value: object) -> bool:
    return isinstance(value, str) and bool(value) and len(value) <= 128


def _positive_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _digest(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _time(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValueError
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError
    return parsed.astimezone(timezone.utc)


def _pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate field")
        result[key] = value
    return result


def _canonical_json(data: dict[str, object]) -> str:
    return json.dumps(
        data,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
