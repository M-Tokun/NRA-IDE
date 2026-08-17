"""Threshold endorsements from policy roots pinned outside the trust bundle."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
import sqlite3
from typing import Mapping
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

from .asymmetric_auth import public_key_fingerprint, sign_payload_ed25519, verify_signed_payload_ed25519
from .trust_bundle import VerifiedTrustBundle


@dataclass(frozen=True, slots=True)
class PinnedPolicyRoot:
    key_id: str
    principal_id: str
    public_key: Ed25519PublicKey


@dataclass(frozen=True, slots=True)
class RootPolicyQuorum:
    satisfied: bool
    policy_id: str | None
    policy_configuration_sha256: str | None
    trust_bundle_generation: int | None
    trust_bundle_sha256: str | None
    principal_ids: tuple[str, ...]
    reason_codes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RootPolicyRotationQuorum:
    satisfied: bool
    rotation_id: str | None
    policy_id: str | None
    previous_configuration_sha256: str | None
    next_configuration_sha256: str | None
    target_bundle_generation: int | None
    target_bundle_sha256: str | None
    previous_principal_ids: tuple[str, ...]
    next_principal_ids: tuple[str, ...]
    reason_codes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RootPolicyRotationEvidence:
    signed_approvals: tuple[str, ...]
    rotation_id: str
    policy_id: str
    previous_policy_roots: Mapping[str, PinnedPolicyRoot]
    previous_minimum_principals: int
    next_policy_roots: Mapping[str, PinnedPolicyRoot]
    next_minimum_principals: int
    primary_root_keys: Mapping[str, Ed25519PublicKey]
    admission_challenge: str
    signature_max_age: timedelta


@dataclass(frozen=True, slots=True)
class RootPolicyCheckpointResult:
    accepted: bool
    reason_codes: tuple[str, ...]


def create_signed_root_policy_endorsement(
    *,
    policy_id: str,
    endorsement_id: str,
    policy_root: PinnedPolicyRoot,
    policy_configuration_sha256: str,
    private_key: Ed25519PrivateKey,
    trust_bundle: VerifiedTrustBundle,
    admission_challenge: str,
    endorsed_at: datetime,
    valid_until: datetime,
) -> str:
    _validate_root(policy_root)
    if (
        not _identifier(policy_id)
        or not _identifier(endorsement_id)
        or not _digest(policy_configuration_sha256)
        or not _digest(admission_challenge)
        or endorsed_at.tzinfo is None
        or valid_until.tzinfo is None
        or valid_until <= endorsed_at
        or public_key_fingerprint(private_key.public_key())
        != public_key_fingerprint(policy_root.public_key)
    ):
        raise ValueError("invalid root policy endorsement")
    payload = _canonical_json({"admission_challenge": admission_challenge, "endorsed_at": _time_text(endorsed_at), "endorsement_id": endorsement_id, "policy_configuration_sha256": policy_configuration_sha256, "policy_id": policy_id, "policy_root_principal_id": policy_root.principal_id, "schema_version": "trust-bundle-root-policy-endorsement/1.2", "trust_bundle_generation": trust_bundle.generation, "trust_bundle_sha256": trust_bundle.signed_bundle_sha256, "valid_until": _time_text(valid_until)})
    return sign_payload_ed25519(payload, key_id=policy_root.key_id, private_key=private_key, issued_at=endorsed_at)


def root_policy_configuration_sha256(
    *,
    policy_id: str,
    pinned_policy_roots: Mapping[str, PinnedPolicyRoot],
    minimum_principals: int,
) -> str:
    roots = _validate_policy_roots(pinned_policy_roots)
    if (
        not _identifier(policy_id)
        or not isinstance(minimum_principals, int)
        or isinstance(minimum_principals, bool)
        or minimum_principals < 2
        or len(roots) < minimum_principals
    ):
        raise ValueError("invalid root policy configuration")
    configuration = {
        "minimum_principals": minimum_principals,
        "policy_id": policy_id,
        "roots": [
            {
                "key_id": root.key_id,
                "principal_id": root.principal_id,
                "public_key_fingerprint": public_key_fingerprint(root.public_key),
            }
            for root in sorted(roots.values(), key=lambda item: item.key_id)
        ],
        "schema_version": "root-policy-configuration/1.0",
    }
    return sha256(_canonical_json(configuration).encode("utf-8")).hexdigest()


def create_signed_root_policy_rotation_approval(
    *,
    rotation_id: str,
    approval_side: str,
    policy_id: str,
    previous_configuration_sha256: str,
    next_configuration_sha256: str,
    target_bundle: VerifiedTrustBundle,
    admission_challenge: str,
    policy_root: PinnedPolicyRoot,
    private_key: Ed25519PrivateKey,
    approved_at: datetime,
    valid_until: datetime,
) -> str:
    _validate_root(policy_root)
    if (
        not _identifier(rotation_id)
        or approval_side not in {"PREVIOUS", "NEXT"}
        or not _identifier(policy_id)
        or not _digest(previous_configuration_sha256)
        or not _digest(next_configuration_sha256)
        or previous_configuration_sha256 == next_configuration_sha256
        or not _digest(admission_challenge)
        or target_bundle.generation <= 1
        or target_bundle.previous_bundle_sha256 is None
        or approved_at.tzinfo is None
        or valid_until.tzinfo is None
        or valid_until <= approved_at
        or public_key_fingerprint(private_key.public_key())
        != public_key_fingerprint(policy_root.public_key)
    ):
        raise ValueError("invalid root policy rotation approval")
    payload = _canonical_json(
        {
            "admission_challenge": admission_challenge,
            "approval_side": approval_side,
            "approved_at": _time_text(approved_at),
            "next_configuration_sha256": next_configuration_sha256,
            "policy_id": policy_id,
            "policy_root_principal_id": policy_root.principal_id,
            "previous_configuration_sha256": previous_configuration_sha256,
            "rotation_id": rotation_id,
            "schema_version": "root-policy-rotation-approval/1.0",
            "target_bundle_generation": target_bundle.generation,
            "target_bundle_sha256": target_bundle.signed_bundle_sha256,
            "valid_until": _time_text(valid_until),
        }
    )
    return sign_payload_ed25519(
        payload,
        key_id=policy_root.key_id,
        private_key=private_key,
        issued_at=approved_at,
    )


def assess_root_policy_rotation_quorum(
    signed_approvals: tuple[str, ...],
    *,
    rotation_id: str,
    policy_id: str,
    previous_policy_roots: Mapping[str, PinnedPolicyRoot],
    previous_minimum_principals: int,
    next_policy_roots: Mapping[str, PinnedPolicyRoot],
    next_minimum_principals: int,
    primary_root_keys: Mapping[str, Ed25519PublicKey],
    target_bundle: VerifiedTrustBundle,
    admission_challenge: str,
    signature_max_age: timedelta,
    now: datetime | None = None,
) -> RootPolicyRotationQuorum:
    empty = (False, None, None, None, None, None, None, (), ())
    current = now or datetime.now(timezone.utc)
    try:
        previous_roots = _validate_root_set(previous_policy_roots, primary_root_keys)
        next_roots = _validate_root_set(next_policy_roots, primary_root_keys)
        previous_digest = root_policy_configuration_sha256(
            policy_id=policy_id,
            pinned_policy_roots=previous_roots,
            minimum_principals=previous_minimum_principals,
        )
        next_digest = root_policy_configuration_sha256(
            policy_id=policy_id,
            pinned_policy_roots=next_roots,
            minimum_principals=next_minimum_principals,
        )
        _identifier(rotation_id)
        _digest(admission_challenge)
        if (
            previous_digest == next_digest
            or current.tzinfo is None
            or not isinstance(signed_approvals, tuple)
            or not signed_approvals
            or not isinstance(signature_max_age, timedelta)
            or signature_max_age <= timedelta(0)
            or target_bundle.generation <= 1
            or target_bundle.previous_bundle_sha256 is None
        ):
            raise ValueError
        combined_roots = dict(previous_roots)
        for key_id, root in next_roots.items():
            existing = combined_roots.get(key_id)
            if existing is not None and (
                existing.principal_id != root.principal_id
                or public_key_fingerprint(existing.public_key)
                != public_key_fingerprint(root.public_key)
            ):
                raise ValueError
            combined_roots[key_id] = root
    except (TypeError, ValueError):
        return RootPolicyRotationQuorum(*empty, ("ROOT_POLICY_ROTATION_CONFIG_INVALID",))

    public_keys = {key_id: root.public_key for key_id, root in combined_roots.items()}
    previous_principals = set()
    next_principals = set()
    invalid = False
    mismatch = False
    expected = (
        rotation_id,
        policy_id,
        previous_digest,
        next_digest,
        target_bundle.generation,
        target_bundle.signed_bundle_sha256,
        admission_challenge,
    )
    for signed in signed_approvals:
        verified = verify_signed_payload_ed25519(
            signed,
            trusted_public_keys=public_keys,
            max_age=signature_max_age,
            now=current,
        )
        if verified.payload_json is None or verified.key_id is None:
            invalid = True
            continue
        try:
            data = json.loads(verified.payload_json, object_pairs_hook=_pairs_hook)
            required = {
                "admission_challenge", "approval_side", "approved_at",
                "next_configuration_sha256", "policy_id",
                "policy_root_principal_id", "previous_configuration_sha256",
                "rotation_id", "schema_version", "target_bundle_generation",
                "target_bundle_sha256", "valid_until",
            }
            if not isinstance(data, dict) or set(data) != required:
                raise ValueError
            if data["schema_version"] != "root-policy-rotation-approval/1.0":
                raise ValueError
            side = data["approval_side"]
            if side not in {"PREVIOUS", "NEXT"}:
                raise ValueError
            root_set = previous_roots if side == "PREVIOUS" else next_roots
            root = root_set.get(verified.key_id)
            if root is None or data["policy_root_principal_id"] != root.principal_id:
                raise ValueError
            approved_at = _time(data["approved_at"])
            valid_until = _time(data["valid_until"])
            if valid_until <= approved_at or current.astimezone(timezone.utc) >= valid_until:
                raise ValueError
            observed = (
                _identifier(data["rotation_id"]),
                _identifier(data["policy_id"]),
                _digest(data["previous_configuration_sha256"]),
                _digest(data["next_configuration_sha256"]),
                data["target_bundle_generation"],
                _digest(data["target_bundle_sha256"]),
                _digest(data["admission_challenge"]),
            )
            if (
                not isinstance(observed[4], int)
                or isinstance(observed[4], bool)
                or observed != expected
            ):
                mismatch = True
                continue
        except (TypeError, ValueError, json.JSONDecodeError):
            invalid = True
            continue
        if side == "PREVIOUS":
            previous_principals.add(root.principal_id)
        else:
            next_principals.add(root.principal_id)

    previous_ids = tuple(sorted(previous_principals))
    next_ids = tuple(sorted(next_principals))
    reasons = []
    if len(previous_ids) < previous_minimum_principals:
        reasons.append("ROOT_POLICY_PREVIOUS_ROTATION_QUORUM_NOT_REACHED")
    if len(next_ids) < next_minimum_principals:
        reasons.append("ROOT_POLICY_NEXT_ROTATION_QUORUM_NOT_REACHED")
    if invalid:
        reasons.append("INVALID_ROOT_POLICY_ROTATION_APPROVAL_IGNORED")
    if mismatch:
        reasons.append("ROOT_POLICY_ROTATION_BINDING_MISMATCH")
    if reasons:
        return RootPolicyRotationQuorum(
            False, rotation_id, policy_id, previous_digest, next_digest,
            target_bundle.generation, target_bundle.signed_bundle_sha256,
            previous_ids, next_ids, tuple(reasons),
        )
    return RootPolicyRotationQuorum(
        True, rotation_id, policy_id, previous_digest, next_digest,
        target_bundle.generation, target_bundle.signed_bundle_sha256,
        previous_ids, next_ids, (),
    )


def assess_root_policy_quorum(signed_endorsements: tuple[str, ...], *, pinned_policy_roots: Mapping[str, PinnedPolicyRoot], primary_root_keys: Mapping[str, Ed25519PublicKey], trust_bundle: VerifiedTrustBundle, admission_challenge: str, minimum_principals: int, signature_max_age: timedelta, now: datetime | None = None) -> RootPolicyQuorum:
    current = now or datetime.now(timezone.utc)
    try:
        roots = _validate_root_set(pinned_policy_roots, primary_root_keys)
    except ValueError:
        return RootPolicyQuorum(False, None, None, None, None, (), ("ROOT_POLICY_CONFIG_INVALID",))
    if (current.tzinfo is None or not isinstance(signed_endorsements, tuple) or not signed_endorsements or not isinstance(minimum_principals, int) or isinstance(minimum_principals, bool) or minimum_principals < 2 or len({root.principal_id for root in roots.values()}) < minimum_principals or not isinstance(signature_max_age, timedelta) or signature_max_age <= timedelta(0)):
        return RootPolicyQuorum(False, None, None, None, None, (), ("ROOT_POLICY_CONFIG_INVALID",))
    try:
        _digest(admission_challenge)
    except ValueError:
        return RootPolicyQuorum(False, None, None, None, None, (), ("ROOT_POLICY_CONFIG_INVALID",))
    public_keys = {key_id: root.public_key for key_id, root in roots.items()}
    principals = set()
    agreement = None
    invalid = False
    mismatch = False
    configuration_mismatch = False
    challenge_mismatch = False
    for signed in signed_endorsements:
        verified = verify_signed_payload_ed25519(signed, trusted_public_keys=public_keys, max_age=signature_max_age, now=current)
        if verified.payload_json is None or verified.key_id is None:
            invalid = True
            continue
        root = roots[verified.key_id]
        try:
            data = json.loads(verified.payload_json, object_pairs_hook=_pairs_hook)
            if not isinstance(data, dict) or set(data) != {"admission_challenge", "endorsed_at", "endorsement_id", "policy_configuration_sha256", "policy_id", "policy_root_principal_id", "schema_version", "trust_bundle_generation", "trust_bundle_sha256", "valid_until"}:
                raise ValueError
            if data["schema_version"] != "trust-bundle-root-policy-endorsement/1.2":
                raise ValueError
            challenge = _digest(data["admission_challenge"])
            _identifier(data["endorsement_id"])
            policy_id = _identifier(data["policy_id"])
            configuration_digest = _digest(data["policy_configuration_sha256"])
            if data["policy_root_principal_id"] != root.principal_id:
                raise ValueError
            generation = data["trust_bundle_generation"]
            digest = _digest(data["trust_bundle_sha256"])
            endorsed_at = _time(data["endorsed_at"])
            valid_until = _time(data["valid_until"])
            if not isinstance(generation, int) or isinstance(generation, bool) or generation <= 0 or valid_until <= endorsed_at or current.astimezone(timezone.utc) >= valid_until:
                raise ValueError
        except (TypeError, ValueError, json.JSONDecodeError):
            invalid = True
            continue
        expected_configuration = root_policy_configuration_sha256(
            policy_id=policy_id,
            pinned_policy_roots=roots,
            minimum_principals=minimum_principals,
        )
        item_agreement = (policy_id, configuration_digest, generation, digest, challenge)
        if challenge != admission_challenge:
            challenge_mismatch = True
            continue
        if configuration_digest != expected_configuration:
            configuration_mismatch = True
            continue
        if generation != trust_bundle.generation or digest != trust_bundle.signed_bundle_sha256 or (agreement is not None and item_agreement != agreement):
            mismatch = True
            continue
        agreement = item_agreement
        principals.add(root.principal_id)
    principal_ids = tuple(sorted(principals))
    if agreement is None or len(principal_ids) < minimum_principals:
        reasons = ["ROOT_POLICY_QUORUM_NOT_REACHED"]
        if invalid:
            reasons.append("INVALID_ROOT_POLICY_ENDORSEMENT_IGNORED")
        if mismatch:
            reasons.append("ROOT_POLICY_TRUST_BUNDLE_MISMATCH")
        if configuration_mismatch:
            reasons.append("ROOT_POLICY_CONFIGURATION_MISMATCH")
        if challenge_mismatch:
            reasons.append("ROOT_POLICY_ADMISSION_CHALLENGE_MISMATCH")
        return RootPolicyQuorum(False, None, None, None, None, principal_ids, tuple(reasons))
    return RootPolicyQuorum(True, agreement[0], agreement[1], agreement[2], agreement[3], principal_ids, ())


class RootPolicyCheckpointStore:
    """Append-only accepted policy/bundle state; same head is idempotent."""

    def __init__(self, database_path: Path) -> None:
        if not database_path.parent.exists():
            raise ValueError("root policy checkpoint parent must exist")
        self._connection = sqlite3.connect(database_path, timeout=5.0)
        self._connection.execute("PRAGMA synchronous=FULL")
        self._connection.execute("PRAGMA journal_mode=DELETE")
        self._initialize()

    def __enter__(self) -> "RootPolicyCheckpointStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        self._connection.close()

    def accept(
        self,
        signed_endorsements: tuple[str, ...],
        trust_bundle: VerifiedTrustBundle,
        *,
        pinned_policy_roots: Mapping[str, PinnedPolicyRoot],
        primary_root_keys: Mapping[str, Ed25519PublicKey],
        admission_challenge: str,
        minimum_principals: int,
        signature_max_age: timedelta,
        rotation_evidence: RootPolicyRotationEvidence | None = None,
        now: datetime | None = None,
    ) -> RootPolicyCheckpointResult:
        if not isinstance(trust_bundle, VerifiedTrustBundle):
            return RootPolicyCheckpointResult(False, ("ROOT_POLICY_CHECKPOINT_INPUT_INVALID",))
        quorum = assess_root_policy_quorum(
            signed_endorsements,
            pinned_policy_roots=pinned_policy_roots,
            primary_root_keys=primary_root_keys,
            trust_bundle=trust_bundle,
            admission_challenge=admission_challenge,
            minimum_principals=minimum_principals,
            signature_max_age=signature_max_age,
            now=now,
        )
        if (
            not quorum.satisfied
            or quorum.policy_id is None
            or not _digest_or_false(quorum.policy_configuration_sha256)
            or quorum.trust_bundle_generation != trust_bundle.generation
            or quorum.trust_bundle_sha256 != trust_bundle.signed_bundle_sha256
            or len(quorum.principal_ids) < 2
        ):
            return RootPolicyCheckpointResult(False, ("ROOT_POLICY_CHECKPOINT_INPUT_INVALID",))
        principals_json = _canonical_json(list(quorum.principal_ids))
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            row = self._connection.execute("SELECT generation, trust_bundle_sha256, policy_id, policy_configuration_sha256, principal_ids_json FROM root_policy_checkpoint ORDER BY generation DESC LIMIT 1").fetchone()
            if row is None:
                if trust_bundle.generation != 1 or trust_bundle.previous_bundle_sha256 is not None:
                    self._connection.rollback()
                    return RootPolicyCheckpointResult(False, ("ROOT_POLICY_CHECKPOINT_INITIAL_STATE_INVALID",))
            else:
                latest_generation, latest_digest, latest_policy, latest_configuration, latest_principals = row
                if trust_bundle.generation < latest_generation:
                    self._connection.rollback()
                    return RootPolicyCheckpointResult(False, ("ROOT_POLICY_ROLLBACK",))
                if trust_bundle.generation == latest_generation:
                    if trust_bundle.signed_bundle_sha256 == latest_digest and quorum.policy_id == latest_policy and quorum.policy_configuration_sha256 == latest_configuration and principals_json == latest_principals:
                        self._connection.rollback()
                        return RootPolicyCheckpointResult(True, ())
                    self._connection.rollback()
                    return RootPolicyCheckpointResult(False, ("ROOT_POLICY_STATE_CONFLICT",))
                if trust_bundle.generation != latest_generation + 1:
                    self._connection.rollback()
                    return RootPolicyCheckpointResult(False, ("ROOT_POLICY_GENERATION_GAP",))
                if trust_bundle.previous_bundle_sha256 != latest_digest:
                    self._connection.rollback()
                    return RootPolicyCheckpointResult(False, ("ROOT_POLICY_PREVIOUS_DIGEST_MISMATCH",))
                if quorum.policy_configuration_sha256 != latest_configuration:
                    rotation = _verify_rotation_evidence(
                        rotation_evidence,
                        trust_bundle=trust_bundle,
                        now=now,
                    )
                    if not _rotation_authorizes(
                        rotation,
                        latest_policy=latest_policy,
                        latest_configuration=latest_configuration,
                        quorum=quorum,
                        trust_bundle=trust_bundle,
                    ):
                        self._connection.rollback()
                        return RootPolicyCheckpointResult(False, ("ROOT_POLICY_CONFIGURATION_CHANGE_NOT_AUTHORIZED",))
            self._connection.execute("INSERT INTO root_policy_checkpoint(generation, trust_bundle_sha256, previous_bundle_sha256, policy_id, policy_configuration_sha256, principal_ids_json) VALUES (?, ?, ?, ?, ?, ?)", (trust_bundle.generation, trust_bundle.signed_bundle_sha256, trust_bundle.previous_bundle_sha256, quorum.policy_id, quorum.policy_configuration_sha256, principals_json))
            self._connection.commit()
            return RootPolicyCheckpointResult(True, ())
        except sqlite3.DatabaseError:
            self._connection.rollback()
            return RootPolicyCheckpointResult(False, ("ROOT_POLICY_CHECKPOINT_FAILURE",))

    def _initialize(self) -> None:
        self._connection.executescript("""
            CREATE TABLE IF NOT EXISTS root_policy_checkpoint (
                generation INTEGER PRIMARY KEY,
                trust_bundle_sha256 TEXT NOT NULL UNIQUE,
                previous_bundle_sha256 TEXT,
                policy_id TEXT NOT NULL,
                policy_configuration_sha256 TEXT NOT NULL,
                principal_ids_json TEXT NOT NULL
            );
            CREATE TRIGGER IF NOT EXISTS root_policy_checkpoint_no_update
            BEFORE UPDATE ON root_policy_checkpoint
            BEGIN SELECT RAISE(ABORT, 'append-only root policy checkpoint'); END;
            CREATE TRIGGER IF NOT EXISTS root_policy_checkpoint_no_delete
            BEFORE DELETE ON root_policy_checkpoint
            BEGIN SELECT RAISE(ABORT, 'append-only root policy checkpoint'); END;
        """)
        self._connection.commit()


class RootPolicyWitnessStateStore:
    """Policy-root-owned monotonic state used before creating endorsements."""

    def __init__(self, database_path: Path, policy_root: PinnedPolicyRoot) -> None:
        _validate_root(policy_root)
        if not database_path.parent.exists():
            raise ValueError("root policy witness parent must exist")
        self.policy_root = policy_root
        self._connection = sqlite3.connect(database_path, timeout=5.0)
        self._connection.execute("PRAGMA synchronous=FULL")
        self._connection.execute("PRAGMA journal_mode=DELETE")
        self._connection.executescript("""
            CREATE TABLE IF NOT EXISTS witnessed_root_policy (
                generation INTEGER PRIMARY KEY,
                trust_bundle_sha256 TEXT NOT NULL UNIQUE,
                previous_bundle_sha256 TEXT,
                policy_id TEXT NOT NULL,
                policy_configuration_sha256 TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS root_policy_endorsement (
                sequence INTEGER PRIMARY KEY,
                generation INTEGER NOT NULL,
                trust_bundle_sha256 TEXT NOT NULL,
                endorsement_id TEXT NOT NULL UNIQUE,
                signed_endorsement_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS root_policy_rotation (
                rotation_id TEXT PRIMARY KEY,
                previous_configuration_sha256 TEXT NOT NULL,
                next_configuration_sha256 TEXT NOT NULL,
                previous_bundle_sha256 TEXT NOT NULL,
                target_bundle_generation INTEGER NOT NULL,
                target_bundle_sha256 TEXT NOT NULL UNIQUE,
                signed_approvals_sha256 TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS root_policy_rotation_approval (
                rotation_id TEXT NOT NULL,
                approval_side TEXT NOT NULL,
                policy_id TEXT NOT NULL,
                previous_configuration_sha256 TEXT NOT NULL,
                next_configuration_sha256 TEXT NOT NULL,
                target_bundle_generation INTEGER NOT NULL,
                target_bundle_sha256 TEXT NOT NULL,
                admission_challenge TEXT NOT NULL,
                signed_approval_json TEXT NOT NULL,
                PRIMARY KEY (rotation_id, approval_side)
            );
            CREATE TRIGGER IF NOT EXISTS witnessed_root_policy_no_update
            BEFORE UPDATE ON witnessed_root_policy
            BEGIN SELECT RAISE(ABORT, 'append-only root policy witness'); END;
            CREATE TRIGGER IF NOT EXISTS witnessed_root_policy_no_delete
            BEFORE DELETE ON witnessed_root_policy
            BEGIN SELECT RAISE(ABORT, 'append-only root policy witness'); END;
            CREATE TRIGGER IF NOT EXISTS root_policy_endorsement_no_update
            BEFORE UPDATE ON root_policy_endorsement
            BEGIN SELECT RAISE(ABORT, 'append-only root policy endorsement'); END;
            CREATE TRIGGER IF NOT EXISTS root_policy_endorsement_no_delete
            BEFORE DELETE ON root_policy_endorsement
            BEGIN SELECT RAISE(ABORT, 'append-only root policy endorsement'); END;
            CREATE TRIGGER IF NOT EXISTS root_policy_rotation_no_update
            BEFORE UPDATE ON root_policy_rotation
            BEGIN SELECT RAISE(ABORT, 'append-only root policy rotation'); END;
            CREATE TRIGGER IF NOT EXISTS root_policy_rotation_no_delete
            BEFORE DELETE ON root_policy_rotation
            BEGIN SELECT RAISE(ABORT, 'append-only root policy rotation'); END;
            CREATE TRIGGER IF NOT EXISTS root_policy_rotation_approval_no_update
            BEFORE UPDATE ON root_policy_rotation_approval
            BEGIN SELECT RAISE(ABORT, 'append-only root policy rotation approval'); END;
            CREATE TRIGGER IF NOT EXISTS root_policy_rotation_approval_no_delete
            BEFORE DELETE ON root_policy_rotation_approval
            BEGIN SELECT RAISE(ABORT, 'append-only root policy rotation approval'); END;
        """)
        self._connection.commit()

    def __enter__(self) -> "RootPolicyWitnessStateStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        self._connection.close()

    def endorse(self, *, policy_id: str, policy_configuration_sha256: str, endorsement_id: str, private_key: Ed25519PrivateKey, trust_bundle: VerifiedTrustBundle, admission_challenge: str, endorsed_at: datetime, valid_until: datetime) -> str:
        _digest(policy_configuration_sha256)
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            row = self._connection.execute("SELECT generation, trust_bundle_sha256, policy_id, policy_configuration_sha256 FROM witnessed_root_policy ORDER BY generation DESC LIMIT 1").fetchone()
            if row is None:
                if trust_bundle.generation != 1 or trust_bundle.previous_bundle_sha256 is not None:
                    raise ValueError("ROOT_POLICY_WITNESS_INITIAL_STATE_INVALID")
                self._insert(policy_id, policy_configuration_sha256, trust_bundle)
            else:
                generation, digest, latest_policy, latest_configuration = row
                if trust_bundle.generation < generation:
                    raise ValueError("ROOT_POLICY_WITNESS_ROLLBACK")
                if trust_bundle.generation == generation:
                    if trust_bundle.signed_bundle_sha256 != digest or policy_id != latest_policy or policy_configuration_sha256 != latest_configuration:
                        raise ValueError("ROOT_POLICY_WITNESS_STATE_CONFLICT")
                else:
                    if trust_bundle.generation != generation + 1:
                        raise ValueError("ROOT_POLICY_WITNESS_GENERATION_GAP")
                    if trust_bundle.previous_bundle_sha256 != digest:
                        raise ValueError("ROOT_POLICY_WITNESS_PREVIOUS_DIGEST_MISMATCH")
                    if policy_configuration_sha256 != latest_configuration:
                        raise ValueError("ROOT_POLICY_WITNESS_CONFIGURATION_CHANGE_NOT_AUTHORIZED")
                    self._insert(policy_id, policy_configuration_sha256, trust_bundle)
            signed = create_signed_root_policy_endorsement(policy_id=policy_id, policy_configuration_sha256=policy_configuration_sha256, endorsement_id=endorsement_id, policy_root=self.policy_root, private_key=private_key, trust_bundle=trust_bundle, admission_challenge=admission_challenge, endorsed_at=endorsed_at, valid_until=valid_until)
            existing = self._connection.execute(
                "SELECT signed_endorsement_json FROM root_policy_endorsement WHERE endorsement_id = ?",
                (endorsement_id,),
            ).fetchone()
            if existing is not None:
                if existing[0] != signed:
                    raise ValueError("ROOT_POLICY_WITNESS_ENDORSEMENT_CONFLICT")
                self._connection.commit()
                return signed
            next_sequence = self._connection.execute(
                "SELECT COALESCE(MAX(sequence), 0) + 1 FROM root_policy_endorsement"
            ).fetchone()[0]
            self._connection.execute(
                "INSERT INTO root_policy_endorsement(sequence, generation, trust_bundle_sha256, endorsement_id, signed_endorsement_json) VALUES (?, ?, ?, ?, ?)",
                (
                    next_sequence,
                    trust_bundle.generation,
                    trust_bundle.signed_bundle_sha256,
                    endorsement_id,
                    signed,
                ),
            )
            self._connection.commit()
            return signed
        except (sqlite3.DatabaseError, ValueError):
            self._connection.rollback()
            raise

    def approve_rotation(
        self,
        *,
        rotation_id: str,
        approval_side: str,
        policy_id: str,
        previous_configuration_sha256: str,
        next_configuration_sha256: str,
        private_key: Ed25519PrivateKey,
        trust_bundle: VerifiedTrustBundle,
        admission_challenge: str,
        approved_at: datetime,
        valid_until: datetime,
    ) -> str:
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            row = self._connection.execute(
                "SELECT generation, trust_bundle_sha256, policy_id, policy_configuration_sha256 FROM witnessed_root_policy ORDER BY generation DESC LIMIT 1"
            ).fetchone()
            if approval_side == "PREVIOUS" and row is None:
                raise ValueError("ROOT_POLICY_ROTATION_PREVIOUS_STATE_REQUIRED")
            if row is not None:
                generation, digest, latest_policy, latest_configuration = row
                if (
                    generation != trust_bundle.generation - 1
                    or digest != trust_bundle.previous_bundle_sha256
                    or latest_policy != policy_id
                    or latest_configuration != previous_configuration_sha256
                ):
                    raise ValueError("ROOT_POLICY_ROTATION_APPROVAL_STATE_MISMATCH")
            existing = self._connection.execute(
                "SELECT policy_id, previous_configuration_sha256, next_configuration_sha256, target_bundle_generation, target_bundle_sha256, admission_challenge, signed_approval_json FROM root_policy_rotation_approval WHERE rotation_id = ? AND approval_side = ?",
                (rotation_id, approval_side),
            ).fetchone()
            binding = (
                policy_id,
                previous_configuration_sha256,
                next_configuration_sha256,
                trust_bundle.generation,
                trust_bundle.signed_bundle_sha256,
                admission_challenge,
            )
            if existing is not None:
                if existing[:6] != binding:
                    raise ValueError("ROOT_POLICY_ROTATION_APPROVAL_CONFLICT")
                self._connection.rollback()
                return existing[6]
            signed = create_signed_root_policy_rotation_approval(
                rotation_id=rotation_id,
                approval_side=approval_side,
                policy_id=policy_id,
                previous_configuration_sha256=previous_configuration_sha256,
                next_configuration_sha256=next_configuration_sha256,
                target_bundle=trust_bundle,
                admission_challenge=admission_challenge,
                policy_root=self.policy_root,
                private_key=private_key,
                approved_at=approved_at,
                valid_until=valid_until,
            )
            self._connection.execute(
                "INSERT INTO root_policy_rotation_approval(rotation_id, approval_side, policy_id, previous_configuration_sha256, next_configuration_sha256, target_bundle_generation, target_bundle_sha256, admission_challenge, signed_approval_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    rotation_id,
                    approval_side,
                    *binding,
                    signed,
                ),
            )
            self._connection.commit()
            return signed
        except (sqlite3.DatabaseError, ValueError):
            self._connection.rollback()
            raise

    def bootstrap_rotation(
        self,
        *,
        rotation_evidence: RootPolicyRotationEvidence,
        policy_configuration_sha256: str,
        endorsement_id: str,
        private_key: Ed25519PrivateKey,
        trust_bundle: VerifiedTrustBundle,
        admission_challenge: str,
        endorsed_at: datetime,
        valid_until: datetime,
    ) -> str:
        rotation = _verify_rotation_evidence(
            rotation_evidence,
            trust_bundle=trust_bundle,
            now=endorsed_at,
        )
        if (
            not rotation.satisfied
            or rotation.policy_id != rotation_evidence.policy_id
            or rotation.next_configuration_sha256
            != policy_configuration_sha256
            or rotation.target_bundle_generation != trust_bundle.generation
            or rotation.target_bundle_sha256 != trust_bundle.signed_bundle_sha256
            or rotation_evidence.admission_challenge != admission_challenge
            or not _root_is_committed_member(
                self.policy_root,
                rotation_evidence.next_policy_roots,
            )
        ):
            raise ValueError("ROOT_POLICY_WITNESS_ROTATION_INVALID")
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            if self._connection.execute(
                "SELECT 1 FROM witnessed_root_policy LIMIT 1"
            ).fetchone() is not None:
                raise ValueError("ROOT_POLICY_WITNESS_BOOTSTRAP_NOT_EMPTY")
            self._insert_rotation(
                rotation,
                rotation_evidence,
                trust_bundle,
            )
            self._insert(
                rotation_evidence.policy_id,
                policy_configuration_sha256,
                trust_bundle,
            )
            signed = create_signed_root_policy_endorsement(
                policy_id=rotation_evidence.policy_id,
                policy_configuration_sha256=policy_configuration_sha256,
                endorsement_id=endorsement_id,
                policy_root=self.policy_root,
                private_key=private_key,
                trust_bundle=trust_bundle,
                admission_challenge=admission_challenge,
                endorsed_at=endorsed_at,
                valid_until=valid_until,
            )
            self._insert_endorsement(endorsement_id, trust_bundle, signed)
            self._connection.commit()
            return signed
        except (sqlite3.DatabaseError, ValueError):
            self._connection.rollback()
            raise

    def rotate_retained(
        self,
        *,
        rotation_evidence: RootPolicyRotationEvidence,
        policy_configuration_sha256: str,
        endorsement_id: str,
        private_key: Ed25519PrivateKey,
        trust_bundle: VerifiedTrustBundle,
        admission_challenge: str,
        endorsed_at: datetime,
        valid_until: datetime,
    ) -> str:
        rotation = _verify_rotation_evidence(
            rotation_evidence,
            trust_bundle=trust_bundle,
            now=endorsed_at,
        )
        if (
            not rotation.satisfied
            or rotation.policy_id != rotation_evidence.policy_id
            or rotation.next_configuration_sha256
            != policy_configuration_sha256
            or rotation.target_bundle_generation != trust_bundle.generation
            or rotation.target_bundle_sha256 != trust_bundle.signed_bundle_sha256
            or rotation_evidence.admission_challenge != admission_challenge
            or not _root_is_committed_member(
                self.policy_root,
                rotation_evidence.previous_policy_roots,
            )
            or not _root_is_committed_member(
                self.policy_root,
                rotation_evidence.next_policy_roots,
            )
        ):
            raise ValueError("ROOT_POLICY_WITNESS_ROTATION_INVALID")
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            row = self._connection.execute(
                "SELECT generation, trust_bundle_sha256, policy_id, policy_configuration_sha256 FROM witnessed_root_policy ORDER BY generation DESC LIMIT 1"
            ).fetchone()
            if row is None:
                raise ValueError("ROOT_POLICY_WITNESS_RETAINED_STATE_REQUIRED")
            generation, digest, latest_policy, latest_configuration = row
            if (
                generation != trust_bundle.generation - 1
                or digest != trust_bundle.previous_bundle_sha256
                or latest_policy != rotation_evidence.policy_id
                or latest_configuration
                != rotation.previous_configuration_sha256
            ):
                raise ValueError("ROOT_POLICY_WITNESS_ROTATION_STATE_MISMATCH")
            self._insert_rotation(
                rotation,
                rotation_evidence,
                trust_bundle,
            )
            self._insert(
                rotation_evidence.policy_id,
                policy_configuration_sha256,
                trust_bundle,
            )
            signed = create_signed_root_policy_endorsement(
                policy_id=rotation_evidence.policy_id,
                policy_configuration_sha256=policy_configuration_sha256,
                endorsement_id=endorsement_id,
                policy_root=self.policy_root,
                private_key=private_key,
                trust_bundle=trust_bundle,
                admission_challenge=admission_challenge,
                endorsed_at=endorsed_at,
                valid_until=valid_until,
            )
            self._insert_endorsement(endorsement_id, trust_bundle, signed)
            self._connection.commit()
            return signed
        except (sqlite3.DatabaseError, ValueError):
            self._connection.rollback()
            raise

    def _insert(self, policy_id: str, policy_configuration_sha256: str, trust_bundle: VerifiedTrustBundle) -> None:
        self._connection.execute("INSERT INTO witnessed_root_policy(generation, trust_bundle_sha256, previous_bundle_sha256, policy_id, policy_configuration_sha256) VALUES (?, ?, ?, ?, ?)", (trust_bundle.generation, trust_bundle.signed_bundle_sha256, trust_bundle.previous_bundle_sha256, policy_id, policy_configuration_sha256))

    def _insert_rotation(self, rotation: RootPolicyRotationQuorum, rotation_evidence: RootPolicyRotationEvidence, trust_bundle: VerifiedTrustBundle) -> None:
        self._connection.execute(
            "INSERT INTO root_policy_rotation(rotation_id, previous_configuration_sha256, next_configuration_sha256, previous_bundle_sha256, target_bundle_generation, target_bundle_sha256, signed_approvals_sha256) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                rotation.rotation_id,
                rotation.previous_configuration_sha256,
                rotation.next_configuration_sha256,
                trust_bundle.previous_bundle_sha256,
                rotation.target_bundle_generation,
                rotation.target_bundle_sha256,
                _signed_approvals_sha256(rotation_evidence.signed_approvals),
            ),
        )

    def _insert_endorsement(self, endorsement_id: str, trust_bundle: VerifiedTrustBundle, signed: str) -> None:
        next_sequence = self._connection.execute(
            "SELECT COALESCE(MAX(sequence), 0) + 1 FROM root_policy_endorsement"
        ).fetchone()[0]
        self._connection.execute(
            "INSERT INTO root_policy_endorsement(sequence, generation, trust_bundle_sha256, endorsement_id, signed_endorsement_json) VALUES (?, ?, ?, ?, ?)",
            (
                next_sequence,
                trust_bundle.generation,
                trust_bundle.signed_bundle_sha256,
                endorsement_id,
                signed,
            ),
        )


def _validate_root_set(roots: Mapping[str, PinnedPolicyRoot], primary: Mapping[str, Ed25519PublicKey]) -> dict[str, PinnedPolicyRoot]:
    if not isinstance(primary, Mapping) or not primary:
        raise ValueError
    result = _validate_policy_roots(roots)
    primary_fingerprints = {public_key_fingerprint(key) for key in primary.values()}
    for root in result.values():
        fingerprint = public_key_fingerprint(root.public_key)
        if fingerprint in primary_fingerprints:
            raise ValueError
    return result


def _rotation_authorizes(
    rotation: RootPolicyRotationQuorum | None,
    *,
    latest_policy: str,
    latest_configuration: str,
    quorum: RootPolicyQuorum,
    trust_bundle: VerifiedTrustBundle,
) -> bool:
    return (
        isinstance(rotation, RootPolicyRotationQuorum)
        and rotation.satisfied
        and rotation.policy_id == latest_policy == quorum.policy_id
        and rotation.previous_configuration_sha256 == latest_configuration
        and rotation.next_configuration_sha256 == quorum.policy_configuration_sha256
        and rotation.target_bundle_generation == trust_bundle.generation
        and rotation.target_bundle_sha256 == trust_bundle.signed_bundle_sha256
    )


def _verify_rotation_evidence(
    evidence: RootPolicyRotationEvidence | None,
    *,
    trust_bundle: VerifiedTrustBundle,
    now: datetime | None,
) -> RootPolicyRotationQuorum:
    if not isinstance(evidence, RootPolicyRotationEvidence):
        return RootPolicyRotationQuorum(
            False, None, None, None, None, None, None, (), (),
            ("ROOT_POLICY_ROTATION_EVIDENCE_REQUIRED",),
        )
    return assess_root_policy_rotation_quorum(
        evidence.signed_approvals,
        rotation_id=evidence.rotation_id,
        policy_id=evidence.policy_id,
        previous_policy_roots=evidence.previous_policy_roots,
        previous_minimum_principals=evidence.previous_minimum_principals,
        next_policy_roots=evidence.next_policy_roots,
        next_minimum_principals=evidence.next_minimum_principals,
        primary_root_keys=evidence.primary_root_keys,
        target_bundle=trust_bundle,
        admission_challenge=evidence.admission_challenge,
        signature_max_age=evidence.signature_max_age,
        now=now,
    )


def _root_is_committed_member(
    policy_root: PinnedPolicyRoot,
    roots: Mapping[str, PinnedPolicyRoot],
) -> bool:
    try:
        committed = _validate_policy_roots(roots).get(policy_root.key_id)
    except ValueError:
        return False
    return (
        committed is not None
        and committed.principal_id == policy_root.principal_id
        and public_key_fingerprint(committed.public_key)
        == public_key_fingerprint(policy_root.public_key)
    )


def _signed_approvals_sha256(signed_approvals: tuple[str, ...]) -> str:
    return sha256(
        _canonical_json(sorted(signed_approvals)).encode("utf-8")
    ).hexdigest()


def _validate_policy_roots(roots: Mapping[str, PinnedPolicyRoot]) -> dict[str, PinnedPolicyRoot]:
    if not isinstance(roots, Mapping) or not roots:
        raise ValueError
    result = dict(roots)
    fingerprints = set()
    principals = set()
    for key_id, root in result.items():
        _validate_root(root)
        fingerprint = public_key_fingerprint(root.public_key)
        if key_id != root.key_id or fingerprint in fingerprints or root.principal_id in principals:
            raise ValueError
        fingerprints.add(fingerprint)
        principals.add(root.principal_id)
    return result


def _validate_root(root: object) -> None:
    if not isinstance(root, PinnedPolicyRoot) or not _identifier(root.key_id) or not _identifier(root.principal_id) or not isinstance(root.public_key, Ed25519PublicKey):
        raise ValueError


def _identifier(value: object) -> str:
    if not isinstance(value, str) or not 0 < len(value) <= 128 or any(character.isspace() for character in value):
        raise ValueError
    return value


def _digest(value: object) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise ValueError
    return value


def _digest_or_false(value: object) -> bool:
    try:
        _digest(value)
        return True
    except ValueError:
        return False


def _time(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValueError
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError
    return parsed.astimezone(timezone.utc)


def _time_text(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def _pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError
        result[key] = value
    return result


def _canonical_json(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
