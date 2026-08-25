"""One-use execution admission bound to a witnessed latch state."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import PurePosixPath
from typing import Protocol

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from ..safety_kernel.response_integrity import ResponseIntegrityState
from .asymmetric_auth import public_key_fingerprint, sign_payload_ed25519
from .irreversible_latch_store import IrreversibleLatchHead
from .role_verification import verify_role_signed_payload
from .trust_bundle import KeyRole, VerifiedTrustBundle


_CAPABILITY_TOKEN = object()


@dataclass(frozen=True, slots=True)
class FileChangeContext:
    """Optional file-change-domain binding committed by an authorizer.

    Present (not ``None``) only for bounded file-change deployments. The
    trusted-runtime core treats it as an opaque clause for binding; the
    file-change invariant adapter requires it and reconstructs the safety
    kernel's ``ActionProposal`` from it. ``None`` keeps the intent
    domain-neutral (design doc 12.3).
    """

    resource_path: str
    change_kind: str
    action_type: str
    expected_base_sha256: str | None
    state_version: int

    def validate(self) -> None:
        """Reject malformed or internally inconsistent file-change bindings.

        Paths must remain relative and printable; modify operations require an
        exact lowercase SHA-256 base while create operations forbid one. The
        method raises ``ValueError`` on the first violation and has no side
        effect.
        """
        if (
            not isinstance(self.resource_path, str)
            or not self.resource_path
            or self.resource_path.startswith(("/", "\\"))
            or "\\" in self.resource_path
            or ":" in self.resource_path
        ):
            raise ValueError("invalid execution file_change resource_path")
        path = PurePosixPath(self.resource_path)
        if (
            path.is_absolute()
            or any(part in {"", ".", ".."} for part in path.parts)
        ):
            raise ValueError("invalid execution file_change resource_path")
        if not all(character.isprintable() for character in self.resource_path):
            raise ValueError("invalid execution file_change resource_path")

        if not isinstance(self.change_kind, str) or self.change_kind not in {
            "MODIFY",
            "CREATE",
        }:
            raise ValueError("invalid execution file_change change_kind")
        if (
            not isinstance(self.action_type, str)
            or self.action_type not in {"PROPOSE_PATCH", "PROPOSE_TEST_FILE"}
        ):
            raise ValueError("invalid execution file_change action_type")

        if (
            not isinstance(self.state_version, int)
            or isinstance(self.state_version, bool)
            or self.state_version < 0
        ):
            raise ValueError("invalid execution file_change state_version")

        if self.expected_base_sha256 is not None and (
            not isinstance(self.expected_base_sha256, str)
            or len(self.expected_base_sha256) != 64
            or any(
                character not in "0123456789abcdef"
                for character in self.expected_base_sha256
            )
        ):
            raise ValueError(
                "invalid execution file_change expected_base_sha256"
            )
        if self.change_kind == "MODIFY" and self.expected_base_sha256 is None:
            raise ValueError(
                "execution file_change MODIFY requires expected_base_sha256"
            )
        if self.change_kind == "CREATE" and self.expected_base_sha256 is not None:
            raise ValueError(
                "execution file_change CREATE must not carry expected_base_sha256"
            )


@dataclass(frozen=True, slots=True)
class BoundaryExecutionIntent:
    """Exact external-effect identity; this does not itself grant authority."""

    intent_id: str
    subject_id: str
    action_type: str
    target_id: str
    action_digest: str
    policy_version: str
    postcondition_subject: str
    postcondition_field: str
    required_postcondition_value: str
    file_change: FileChangeContext | None = None

    def validate(self) -> None:
        """Validate the exact effect identity without granting execution authority.

        Identifiers and the action digest must use their bounded canonical
        forms, the required postcondition must be non-empty, and an optional
        file-change clause is validated independently. Failure raises
        ``ValueError``; success does not execute, sign, or persist the intent.
        """
        for field_name, value in (
            ("intent_id", self.intent_id),
            ("subject_id", self.subject_id),
            ("action_type", self.action_type),
            ("target_id", self.target_id),
            ("policy_version", self.policy_version),
            ("postcondition_subject", self.postcondition_subject),
            ("postcondition_field", self.postcondition_field),
        ):
            if (
                not isinstance(value, str)
                or not value
                or len(value) > 128
                or any(character.isspace() for character in value)
            ):
                raise ValueError(f"invalid execution {field_name}")
        if (
            not isinstance(self.action_digest, str)
            or len(self.action_digest) != 64
            or any(
                character not in "0123456789abcdef"
                for character in self.action_digest
            )
        ):
            raise ValueError("invalid execution action_digest")
        if (
            not isinstance(self.required_postcondition_value, str)
            or not 0 < len(self.required_postcondition_value) <= 4096
        ):
            raise ValueError("invalid execution required_postcondition_value")
        if self.file_change is not None:
            if not isinstance(self.file_change, FileChangeContext):
                raise ValueError("invalid execution file_change")
            self.file_change.validate()


class BoundaryExecutor(Protocol):
    """Runtime-fixed executor; attempt_id is the external idempotency key."""

    def execute(
        self,
        action: bytes,
        *,
        attempt_id: str,
        intent: BoundaryExecutionIntent,
    ) -> bytes: ...


@dataclass(frozen=True, slots=True)
class SimulationOutcome:
    """A dry-run prediction; the real executor has not run yet.

    ``predicted_result_digest`` is optional: a simulator that can predict
    success without computing an exact result digest may leave it ``None``.
    """

    predicted_success: bool
    predicted_result_digest: str | None
    reason_codes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class BoundaryExecutionReport:
    """Executor return report; external reality remains unverified."""

    intent: BoundaryExecutionIntent
    attempt_id: str
    started_at: datetime
    completed_at: datetime
    latch_head: IrreversibleLatchHead | None
    authorization_id: str
    authorizer_principal_ids: tuple[str, ...]
    result: bytes
    result_sha256: str
    response_integrity_state: ResponseIntegrityState


@dataclass(frozen=True, slots=True)
class VerifiedExecutionAuthorization:
    authorization_id: str
    authorization_nonce: str
    authorizer_principal_id: str
    intent: BoundaryExecutionIntent
    latch_store_id: str
    expected_latch_head: IrreversibleLatchHead | None
    authorized_at: datetime
    valid_until: datetime
    signed_authorization_sha256: str
    authorization_payload_sha256: str


@dataclass(frozen=True, slots=True)
class VerifiedExecutionAuthorizationQuorum:
    authorization: VerifiedExecutionAuthorization
    principal_ids: tuple[str, ...]
    minimum_principals: int


class WitnessBoundExecutionCapability:
    """Process-local, one-use capability for one exact intent and runtime state."""

    __slots__ = (
        "_assessment_epoch",
        "_authorization_quorum",
        "_consumed",
        "_intent",
        "_latch_head",
        "_runtime_identity",
    )

    def __init__(
        self,
        *,
        runtime_identity: object,
        intent: BoundaryExecutionIntent,
        authorization_quorum: VerifiedExecutionAuthorizationQuorum,
        assessment_epoch: int,
        latch_head: IrreversibleLatchHead | None,
        _token: object | None = None,
    ) -> None:
        if _token is not _CAPABILITY_TOKEN:
            raise ValueError("execution capability must be created by runtime")
        self._runtime_identity = runtime_identity
        self._intent = intent
        self._authorization_quorum = authorization_quorum
        self._assessment_epoch = assessment_epoch
        self._latch_head = latch_head
        self._consumed = False

    def ensure_available(self) -> None:
        if self._consumed:
            raise ValueError("EXECUTION_CAPABILITY_REUSED")

    def consume(self) -> None:
        self.ensure_available()
        self._consumed = True


def _create_execution_capability(
    *,
    runtime_identity: object,
    intent: BoundaryExecutionIntent,
    authorization_quorum: VerifiedExecutionAuthorizationQuorum,
    assessment_epoch: int,
    latch_head: IrreversibleLatchHead | None,
) -> WitnessBoundExecutionCapability:
    intent.validate()
    return WitnessBoundExecutionCapability(
        runtime_identity=runtime_identity,
        intent=intent,
        authorization_quorum=authorization_quorum,
        assessment_epoch=assessment_epoch,
        latch_head=latch_head,
        _token=_CAPABILITY_TOKEN,
    )


def create_signed_execution_authorization(
    intent: BoundaryExecutionIntent,
    *,
    authorization_id: str,
    authorization_nonce: str,
    latch_store_id: str,
    expected_latch_head: IrreversibleLatchHead | None,
    signing_key_id: str,
    signing_private_key: Ed25519PrivateKey,
    trust_bundle: VerifiedTrustBundle,
    authorized_at: datetime,
    valid_until: datetime,
) -> str:
    intent.validate()
    if (
        not _identifier(authorization_id, 100)
        or not _identifier(latch_store_id, 128)
        or not isinstance(authorization_nonce, str)
        or not 16 <= len(authorization_nonce) <= 96
        or any(character.isspace() for character in authorization_nonce)
        or authorized_at.tzinfo is None
        or valid_until.tzinfo is None
        or not isinstance(signing_private_key, Ed25519PrivateKey)
    ):
        raise ValueError("invalid execution authorization metadata")
    authorized = authorized_at.astimezone(timezone.utc)
    expires = valid_until.astimezone(timezone.utc)
    if expires <= authorized:
        raise ValueError("execution authorization must expire after authorization")
    record = trust_bundle.record_for(signing_key_id)
    if (
        record is None
        or record.role is not KeyRole.EXECUTION_AUTHORIZER
        or not record.active_at(authorized)
        or public_key_fingerprint(record.public_key)
        != public_key_fingerprint(signing_private_key.public_key())
    ):
        raise ValueError("EXECUTION_AUTHORIZER_ROLE_OR_KEY_MISMATCH")
    payload = _canonical_json(
        {
            "authorization_id": authorization_id,
            "authorization_nonce": authorization_nonce,
            "authorized_at": authorized.isoformat(),
            "expected_latch_head": _encode_head(expected_latch_head),
            "intent": {
                "action_digest": intent.action_digest,
                "action_type": intent.action_type,
                "file_change": _encode_file_change(intent.file_change),
                "policy_version": intent.policy_version,
                "postcondition_field": intent.postcondition_field,
                "postcondition_subject": intent.postcondition_subject,
                "required_postcondition_value": (
                    intent.required_postcondition_value
                ),
                "intent_id": intent.intent_id,
                "subject_id": intent.subject_id,
                "target_id": intent.target_id,
            },
            "latch_store_id": latch_store_id,
            "schema_version": "boundary-execution-authorization/1.4",
            "valid_until": expires.isoformat(),
        }
    )
    return sign_payload_ed25519(
        payload,
        key_id=signing_key_id,
        private_key=signing_private_key,
        issued_at=authorized,
        trust_bundle_generation=trust_bundle.generation,
        trust_bundle_sha256=trust_bundle.signed_bundle_sha256,
    )


def verify_signed_execution_authorization(
    signed_authorization_json: str,
    *,
    trust_bundle: VerifiedTrustBundle,
    signature_max_age: timedelta,
    now: datetime | None = None,
) -> tuple[VerifiedExecutionAuthorization | None, tuple[str, ...]]:
    """Verify a fresh execution authorization from the active authority role.

    The signed payload must bind the exact trust bundle and satisfy
    ``signature_max_age`` at timezone-aware ``now``. Schema, identity,
    authorization fields, trust state, signature, and time are validated.
    Failure returns ``None`` with reason codes and does not consume or execute
    the authorization.
    """
    current = now or datetime.now(timezone.utc)
    verified = verify_role_signed_payload(
        signed_authorization_json,
        trust_bundle=trust_bundle,
        required_role=KeyRole.EXECUTION_AUTHORIZER,
        signature_max_age=signature_max_age,
        require_trust_binding=True,
        now=current,
    )
    if verified.payload_json is None or verified.key_record is None:
        return None, verified.reason_codes
    try:
        data = json.loads(verified.payload_json, object_pairs_hook=_pairs_hook)
        if not isinstance(data, dict) or set(data) != {
            "authorization_id",
            "authorization_nonce",
            "authorized_at",
            "expected_latch_head",
            "intent",
            "latch_store_id",
            "schema_version",
            "valid_until",
        }:
            raise ValueError
        if data["schema_version"] != "boundary-execution-authorization/1.4":
            raise ValueError
        intent_data = data["intent"]
        if not isinstance(intent_data, dict) or set(intent_data) != {
            "action_digest",
            "action_type",
            "file_change",
            "policy_version",
            "postcondition_field",
            "postcondition_subject",
            "required_postcondition_value",
            "intent_id",
            "subject_id",
            "target_id",
        }:
            raise ValueError
        intent = BoundaryExecutionIntent(
            intent_id=intent_data["intent_id"],
            subject_id=intent_data["subject_id"],
            action_type=intent_data["action_type"],
            target_id=intent_data["target_id"],
            action_digest=intent_data["action_digest"],
            policy_version=intent_data["policy_version"],
            postcondition_subject=intent_data["postcondition_subject"],
            postcondition_field=intent_data["postcondition_field"],
            required_postcondition_value=(
                intent_data["required_postcondition_value"]
            ),
            file_change=_decode_file_change(intent_data["file_change"]),
        )
        intent.validate()
        authorization_id = data["authorization_id"]
        authorization_nonce = data["authorization_nonce"]
        latch_store_id = data["latch_store_id"]
        authorized_at = _time(data["authorized_at"])
        valid_until = _time(data["valid_until"])
        if (
            not _identifier(authorization_id, 100)
            or not _identifier(latch_store_id, 128)
            or not isinstance(authorization_nonce, str)
            or not 16 <= len(authorization_nonce) <= 96
            or any(character.isspace() for character in authorization_nonce)
            or valid_until <= authorized_at
            or current.astimezone(timezone.utc) < authorized_at
            or current.astimezone(timezone.utc) >= valid_until
        ):
            raise ValueError
        head = _decode_head(data["expected_latch_head"])
        return (
            VerifiedExecutionAuthorization(
                authorization_id=authorization_id,
                authorization_nonce=authorization_nonce,
                authorizer_principal_id=verified.key_record.principal_id,
                intent=intent,
                latch_store_id=latch_store_id,
                expected_latch_head=head,
                authorized_at=authorized_at,
                valid_until=valid_until,
                signed_authorization_sha256=hashlib.sha256(
                    signed_authorization_json.encode("utf-8")
                ).hexdigest(),
                authorization_payload_sha256=hashlib.sha256(
                    verified.payload_json.encode("utf-8")
                ).hexdigest(),
            ),
            (),
        )
    except (TypeError, ValueError, json.JSONDecodeError):
        return None, ("SIGNED_EXECUTION_AUTHORIZATION_INVALID",)


def assess_execution_authorization_quorum(
    signed_authorization_jsons: tuple[str, ...],
    *,
    trust_bundle: VerifiedTrustBundle,
    minimum_principals: int,
    signature_max_age: timedelta,
    now: datetime | None = None,
) -> tuple[VerifiedExecutionAuthorizationQuorum | None, tuple[str, ...]]:
    if (
        not isinstance(minimum_principals, int)
        or isinstance(minimum_principals, bool)
        or minimum_principals < 2
        or not isinstance(signed_authorization_jsons, tuple)
        or not signed_authorization_jsons
    ):
        return None, ("EXECUTION_AUTHORIZATION_QUORUM_CONFIG_INVALID",)
    verified_authorizations = []
    reasons: list[str] = []
    for signed_json in signed_authorization_jsons:
        verified, verification_reasons = verify_signed_execution_authorization(
            signed_json,
            trust_bundle=trust_bundle,
            signature_max_age=signature_max_age,
            now=now,
        )
        if verified is None:
            reasons.extend(verification_reasons)
        else:
            verified_authorizations.append(verified)
    if reasons or not verified_authorizations:
        return None, tuple(dict.fromkeys(reasons))
    first = verified_authorizations[0]
    if any(
        authorization.authorization_payload_sha256
        != first.authorization_payload_sha256
        for authorization in verified_authorizations[1:]
    ):
        return None, ("EXECUTION_AUTHORIZATION_PAYLOAD_MISMATCH",)
    principal_ids = tuple(
        sorted(
            {
                authorization.authorizer_principal_id
                for authorization in verified_authorizations
            }
        )
    )
    if len(principal_ids) < minimum_principals:
        return None, ("EXECUTION_AUTHORIZATION_QUORUM_NOT_REACHED",)
    return (
        VerifiedExecutionAuthorizationQuorum(
            authorization=first,
            principal_ids=principal_ids,
            minimum_principals=minimum_principals,
        ),
        (),
    )


_FILE_CHANGE_KEYS = frozenset(
    {
        "resource_path",
        "change_kind",
        "action_type",
        "expected_base_sha256",
        "state_version",
    }
)


def _encode_file_change(
    context: FileChangeContext | None,
) -> dict[str, object] | None:
    if context is None:
        return None
    context.validate()
    return {
        "resource_path": context.resource_path,
        "change_kind": context.change_kind,
        "action_type": context.action_type,
        "expected_base_sha256": context.expected_base_sha256,
        "state_version": context.state_version,
    }


def _decode_file_change(value: object) -> FileChangeContext | None:
    if value is None:
        return None
    if not isinstance(value, dict) or set(value) != _FILE_CHANGE_KEYS:
        raise ValueError
    context = FileChangeContext(
        resource_path=value["resource_path"],
        change_kind=value["change_kind"],
        action_type=value["action_type"],
        expected_base_sha256=value["expected_base_sha256"],
        state_version=value["state_version"],
    )
    context.validate()
    return context


def _encode_head(head: IrreversibleLatchHead | None) -> dict[str, object] | None:
    if head is None:
        return None
    _validate_head(head)
    return {
        "previous_mac": head.previous_mac,
        "row_mac": head.row_mac,
        "sequence": head.sequence,
    }


def _decode_head(value: object) -> IrreversibleLatchHead | None:
    if value is None:
        return None
    if not isinstance(value, dict) or set(value) != {
        "previous_mac",
        "row_mac",
        "sequence",
    }:
        raise ValueError
    head = IrreversibleLatchHead(
        value["sequence"], value["previous_mac"], value["row_mac"]
    )
    _validate_head(head)
    return head


def _validate_head(head: IrreversibleLatchHead) -> None:
    if (
        not isinstance(head, IrreversibleLatchHead)
        or not isinstance(head.sequence, int)
        or isinstance(head.sequence, bool)
        or head.sequence < 1
        or not _sha256(head.row_mac)
        or (head.previous_mac is not None and not _sha256(head.previous_mac))
        or (head.sequence == 1) != (head.previous_mac is None)
    ):
        raise ValueError("invalid execution authorization latch head")


def _pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate field")
        result[key] = value
    return result


def _time(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValueError
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError
    return parsed.astimezone(timezone.utc)


def _identifier(value: object, maximum: int) -> bool:
    return (
        isinstance(value, str)
        and 0 < len(value) <= maximum
        and not any(character.isspace() for character in value)
    )


def _sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _canonical_json(data: dict[str, object]) -> str:
    return json.dumps(
        data,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
