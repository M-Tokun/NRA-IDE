"""Placement-gated trusted entry point for persistent boundary assessment."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
import hashlib
import secrets
from typing import Callable, Iterable, Mapping

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from ..safety_kernel.boundary import AxisEvidence, BoundaryAssessment
from ..safety_kernel.response_integrity import ResponseIntegrityState
from .deployment_boundary import (
    DeploymentBoundaryAssessment,
    RuntimePlacement,
    assess_runtime_placement,
)
from .auth import derive_subkey
from .authority_manifest import assess_authority_manifest_quorum
from .irreversible_latch_store import PersistentIrreversibleLatchStore
from .execution_gate import (
    BoundaryExecutionReport,
    BoundaryExecutor,
    BoundaryExecutionIntent,
    WitnessBoundExecutionCapability,
    _create_execution_capability,
    assess_execution_authorization_quorum,
)
from .latch_checkpoint import (
    CreateOnlyLatchCheckpointStore,
    synchronize_latch_checkpoints,
)
from .latch_witness import (
    assess_latch_witness_quorum,
    genesis_latch_head,
    verify_signed_latch_checkpoint,
)
from .nonce_store import PersistentNonceStore
from .root_policy import (
    PinnedPolicyRoot,
    RootPolicyCheckpointStore,
    assess_root_policy_quorum,
)
from .trust_bundle import VerifiedTrustBundle, verify_signed_trust_bundle


_ADMISSION_TOKEN = object()
_CHALLENGE_TOKEN = object()


class BoundaryAdmissionChallenge:
    """One-use, process-local challenge for a fresh witness round."""

    __slots__ = ("_nonce", "_consumed")

    def __init__(self, nonce: str, *, _token: object | None = None) -> None:
        if _token is not _CHALLENGE_TOKEN:
            raise ValueError("admission challenge must be created by factory")
        self._nonce = nonce
        self._consumed = False

    @property
    def nonce(self) -> str:
        return self._nonce

    def ensure_available(self) -> None:
        if self._consumed:
            raise ValueError("BOUNDARY_ADMISSION_CHALLENGE_REUSED")

    def consume(self) -> None:
        self.ensure_available()
        self._consumed = True


def create_boundary_admission_challenge() -> BoundaryAdmissionChallenge:
    return BoundaryAdmissionChallenge(
        secrets.token_hex(32),
        _token=_CHALLENGE_TOKEN,
    )


@dataclass(frozen=True, slots=True)
class ExternalLatchWitnessEvidence:
    """Fresh, trust-bound evidence for one exact irreversible latch head."""

    signed_trust_bundle_json: str
    signed_latch_checkpoint_json: str
    signed_witness_attestations: tuple[str, ...]
    minimum_principals: int
    signature_max_age: timedelta
    signed_authority_manifest_attestations: tuple[str, ...] = ()
    minimum_authority_attester_principals: int = 0
    signed_root_policy_endorsements: tuple[str, ...] = ()


class AdmittedBoundaryRuntime:
    """Own the latch store after structural deployment checks have passed."""

    def __init__(
        self,
        *,
        placement: RuntimePlacement,
        deployment_assessment: DeploymentBoundaryAssessment,
        latch_store: PersistentIrreversibleLatchStore,
        checkpoint_stores: tuple[CreateOnlyLatchCheckpointStore, ...],
        latch_store_id: str,
        external_witness_current: bool,
        trust_bundle: VerifiedTrustBundle | None = None,
        execution_authorization_signature_max_age: timedelta | None = None,
        execution_authorization_store: PersistentNonceStore | None = None,
        minimum_execution_authorizer_principals: int | None = None,
        execution_executor: BoundaryExecutor | None = None,
        hard_invariant_checker: (
            Callable[[BoundaryExecutionIntent, bytes], tuple[str, ...]] | None
        ) = None,
        _admission_token: object | None = None,
    ) -> None:
        if _admission_token is not _ADMISSION_TOKEN:
            raise ValueError("boundary runtime must be created by admission")
        if not deployment_assessment.path_separated:
            raise ValueError("boundary runtime placement was not admitted")
        if (
            not isinstance(trust_bundle, VerifiedTrustBundle)
            or not isinstance(execution_authorization_signature_max_age, timedelta)
            or execution_authorization_signature_max_age <= timedelta(0)
            or not isinstance(minimum_execution_authorizer_principals, int)
            or isinstance(minimum_execution_authorizer_principals, bool)
            or minimum_execution_authorizer_principals < 2
        ):
            raise ValueError("execution authorization policy was not admitted")
        self.placement = placement
        self.deployment_assessment = deployment_assessment
        self._latch_store = latch_store
        self._checkpoint_stores = checkpoint_stores
        self.latch_store_id = latch_store_id
        self._external_witness_current = external_witness_current
        self._trust_bundle = trust_bundle
        self._execution_authorization_signature_max_age = (
            execution_authorization_signature_max_age
        )
        self._execution_authorization_store = execution_authorization_store
        self._minimum_execution_authorizer_principals = (
            minimum_execution_authorizer_principals
        )
        if execution_executor is not None and not callable(
            getattr(execution_executor, "execute", None)
        ):
            raise ValueError("EXECUTION_EXECUTOR_INVALID")
        self._execution_executor = execution_executor
        if hard_invariant_checker is not None and not callable(hard_invariant_checker):
            raise ValueError("EXECUTION_HARD_INVARIANT_CHECKER_INVALID")
        self._hard_invariant_checker = hard_invariant_checker
        self._runtime_identity = object()
        self._assessment_epoch = 0
        self._closed = False

    @property
    def external_witness_current(self) -> bool:
        return self._external_witness_current

    def __enter__(self) -> "AdmittedBoundaryRuntime":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        if not self._closed:
            self._closed = True
            self._latch_store.close()
            if self._execution_authorization_store is not None:
                self._execution_authorization_store.close()

    def assess_axes(
        self,
        *,
        target_id: str,
        axes: Iterable[AxisEvidence],
        observed_at: datetime,
    ) -> BoundaryAssessment:
        self._ensure_open()
        self._assessment_epoch += 1
        previous_head = self._latch_store.head()
        synchronize_latch_checkpoints(
            self._latch_store,
            self._checkpoint_stores,
            checkpointed_at=observed_at,
        )
        assessment = self._latch_store.assess_axes(
            target_id=target_id,
            axes=axes,
            observed_at=observed_at,
        )
        synchronize_latch_checkpoints(
            self._latch_store,
            self._checkpoint_stores,
            checkpointed_at=observed_at,
        )
        if self._latch_store.head() != previous_head:
            self._external_witness_current = False
        return assessment

    def prepare_execution(
        self,
        signed_authorization_jsons: tuple[str, ...],
    ) -> WitnessBoundExecutionCapability:
        """Stage one: bind an intent to the currently witnessed runtime state."""
        self._ensure_open()
        if not self._external_witness_current:
            raise ValueError("EXTERNAL_LATCH_WITNESS_NOT_CURRENT")
        if self._execution_authorization_store is None:
            raise ValueError("EXECUTION_AUTHORIZATION_STORE_REQUIRED")
        authorization_quorum, reasons = assess_execution_authorization_quorum(
            signed_authorization_jsons,
            trust_bundle=self._trust_bundle,
            minimum_principals=self._minimum_execution_authorizer_principals,
            signature_max_age=self._execution_authorization_signature_max_age,
        )
        if authorization_quorum is None:
            raise ValueError(",".join(reasons))
        authorization = authorization_quorum.authorization
        current_head = self._latch_store.head()
        if (
            authorization.latch_store_id != self.latch_store_id
            or authorization.expected_latch_head != current_head
        ):
            raise ValueError("EXECUTION_AUTHORIZATION_STATE_MISMATCH")
        if self._latch_store.latched_axis_names(authorization.intent.target_id):
            raise ValueError("EXECUTION_TARGET_IRREVERSIBLY_LATCHED")
        return _create_execution_capability(
            runtime_identity=self._runtime_identity,
            intent=authorization.intent,
            authorization_quorum=authorization_quorum,
            assessment_epoch=self._assessment_epoch,
            latch_head=current_head,
        )

    def execute_authorized_action(
        self,
        capability: WitnessBoundExecutionCapability,
        intent: BoundaryExecutionIntent,
        action: bytes,
    ) -> BoundaryExecutionReport:
        """Stage two: bind exact bytes, consume, execute, and journal outcome."""
        self._ensure_open()
        if not isinstance(capability, WitnessBoundExecutionCapability):
            raise ValueError("invalid execution capability")
        if capability._runtime_identity is not self._runtime_identity:
            raise ValueError("EXECUTION_CAPABILITY_RUNTIME_MISMATCH")
        capability.ensure_available()
        capability.consume()
        if not isinstance(intent, BoundaryExecutionIntent):
            raise ValueError("invalid execution intent")
        intent.validate()
        if capability._intent != intent:
            raise ValueError("EXECUTION_CAPABILITY_INTENT_MISMATCH")
        if (
            not isinstance(action, bytes)
            or not action
            or len(action) > 1024 * 1024
        ):
            raise ValueError("EXECUTION_ACTION_INVALID")
        if hashlib.sha256(action).hexdigest() != intent.action_digest:
            raise ValueError("EXECUTION_ACTION_DIGEST_MISMATCH")
        if self._hard_invariant_checker is not None:
            violations = self._hard_invariant_checker(intent, action)
            if not isinstance(violations, tuple) or not all(
                isinstance(reason, str) and reason for reason in violations
            ):
                raise ValueError("EXECUTION_HARD_INVARIANT_CHECKER_INVALID")
            if violations:
                raise ValueError(
                    "EXECUTION_HARD_INVARIANT_VIOLATION:" + ",".join(violations)
                )
        if self._execution_executor is None:
            raise ValueError("EXECUTION_EXECUTOR_NOT_CONFIGURED")
        if not self._external_witness_current:
            raise ValueError("EXTERNAL_LATCH_WITNESS_NOT_CURRENT")
        if capability._assessment_epoch != self._assessment_epoch:
            raise ValueError("EXECUTION_CAPABILITY_STALE")
        current_head = self._latch_store.head()
        if capability._latch_head != current_head:
            self._external_witness_current = False
            raise ValueError("EXECUTION_CAPABILITY_LATCH_HEAD_MISMATCH")
        authorization_quorum = capability._authorization_quorum
        authorization = authorization_quorum.authorization
        current = datetime.now(timezone.utc)
        if current >= authorization.valid_until:
            raise ValueError("EXECUTION_AUTHORIZATION_EXPIRED")
        assert self._execution_authorization_store is not None
        prepared = self._execution_authorization_store.consume_and_prepare_execution(
            request_id=f"execution-authorization:{authorization.authorization_id}",
            nonce=authorization.authorization_nonce,
            issued_at=authorization.authorized_at,
            request_digest=authorization.authorization_payload_sha256,
            consumed_at=current,
            intent_id=intent.intent_id,
            target_id=intent.target_id,
            action_digest=intent.action_digest,
            postcondition_subject=intent.postcondition_subject,
            postcondition_field=intent.postcondition_field,
            required_postcondition_value=intent.required_postcondition_value,
            authorizer_principal_ids=authorization_quorum.principal_ids,
        )
        if not prepared.accepted or prepared.attempt_id is None:
            raise ValueError(",".join(prepared.reason_codes))
        attempt_id = prepared.attempt_id
        started_at = datetime.now(timezone.utc)
        started = self._execution_authorization_store.record_execution_event(
            attempt_id=attempt_id,
            state="STARTED",
            observed_at=started_at,
        )
        if not started.accepted:
            raise ValueError(",".join(started.reason_codes))
        try:
            result = self._execution_executor.execute(
                action,
                attempt_id=attempt_id,
                intent=intent,
            )
            if (
                not isinstance(result, bytes)
                or len(result) > 1024 * 1024
            ):
                raise ValueError("EXECUTION_RESULT_INVALID")
        except Exception as error:
            unknown = self._execution_authorization_store.record_execution_event(
                attempt_id=attempt_id,
                state="OUTCOME_UNKNOWN",
                observed_at=datetime.now(timezone.utc),
            )
            if not unknown.accepted:
                raise ValueError(",".join(unknown.reason_codes)) from error
            raise ValueError("EXECUTION_OUTCOME_UNKNOWN") from error
        completed_at = datetime.now(timezone.utc)
        result_sha256 = hashlib.sha256(result).hexdigest()
        succeeded = self._execution_authorization_store.record_execution_event(
            attempt_id=attempt_id,
            state="EXECUTOR_RETURNED",
            observed_at=completed_at,
            result_digest=result_sha256,
        )
        if not succeeded.accepted:
            raise ValueError("EXECUTION_OUTCOME_UNKNOWN")
        return BoundaryExecutionReport(
            intent=intent,
            attempt_id=attempt_id,
            started_at=started_at,
            completed_at=completed_at,
            latch_head=current_head,
            authorization_id=authorization.authorization_id,
            authorizer_principal_ids=authorization_quorum.principal_ids,
            result=result,
            result_sha256=result_sha256,
            response_integrity_state=(
                ResponseIntegrityState.COMPLETED_UNVERIFIED
            ),
        )

    def _ensure_open(self) -> None:
        if self._closed:
            raise ValueError("BOUNDARY_RUNTIME_CLOSED")


def admit_boundary_runtime(
    *,
    placement: RuntimePlacement,
    latch_integrity_key: bytes,
    latch_store_id: str,
    admission_challenge: BoundaryAdmissionChallenge | None = None,
    external_witness_evidence: ExternalLatchWitnessEvidence | None = None,
    pinned_root_keys: Mapping[str, Ed25519PublicKey] | None = None,
    trust_bundle_signature_max_age: timedelta | None = None,
    now: datetime | None = None,
    minimum_execution_authorizer_principals: int = 2,
    execution_executor: BoundaryExecutor | None = None,
    hard_invariant_checker: (
        Callable[[BoundaryExecutionIntent, bytes], tuple[str, ...]] | None
    ) = None,
    pinned_policy_roots: Mapping[str, PinnedPolicyRoot] | None = None,
    minimum_policy_root_principals: int = 2,
    root_policy_signature_max_age: timedelta | None = None,
) -> AdmittedBoundaryRuntime:
    """Open the trusted boundary runtime only after structural placement passes."""
    if not _valid_latch_store_id(latch_store_id):
        raise ValueError("invalid latch_store_id")
    if (
        not isinstance(minimum_execution_authorizer_principals, int)
        or isinstance(minimum_execution_authorizer_principals, bool)
        or minimum_execution_authorizer_principals < 2
    ):
        raise ValueError("EXECUTION_AUTHORIZATION_QUORUM_CONFIG_INVALID")
    assessment = assess_runtime_placement(placement)
    if not assessment.path_separated:
        structural_reasons = tuple(
            reason
            for reason in assessment.reason_codes
            if reason != "OS_IDENTITY_SEPARATION_NOT_ATTESTED"
        )
        raise ValueError(",".join(structural_reasons))
    if (
        placement.execution_authorization_database_path is not None
        and not assessment.execution_authority_domains_separated
    ):
        authority_reasons = tuple(
            reason
            for reason in assessment.reason_codes
            if reason.startswith("PLACEMENT_")
            and (
                "AUTHORITY" in reason
                or reason == "PLACEMENT_ROOT_POLICY_CHECKPOINT_REQUIRED"
            )
        )
        raise ValueError(",".join(authority_reasons))
    if not isinstance(admission_challenge, BoundaryAdmissionChallenge):
        raise ValueError("BOUNDARY_ADMISSION_CHALLENGE_REQUIRED")
    admission_challenge.ensure_available()
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        raise ValueError("boundary runtime admission time must be timezone-aware")
    verified_trust_bundle = None
    if external_witness_evidence is not None:
        if not isinstance(external_witness_evidence, ExternalLatchWitnessEvidence):
            raise ValueError("LATCH_EXTERNAL_WITNESS_EVIDENCE_INVALID")
        if (
            not isinstance(pinned_root_keys, Mapping)
            or not pinned_root_keys
            or not isinstance(trust_bundle_signature_max_age, timedelta)
            or trust_bundle_signature_max_age <= timedelta(0)
        ):
            raise ValueError("TRUST_BUNDLE_VERIFICATION_POLICY_INVALID")
        trust_verification = verify_signed_trust_bundle(
            external_witness_evidence.signed_trust_bundle_json,
            pinned_root_keys=pinned_root_keys,
            signature_max_age=trust_bundle_signature_max_age,
            now=current,
        )
        if trust_verification.bundle is None:
            raise ValueError(",".join(trust_verification.reason_codes))
        verified_trust_bundle = trust_verification.bundle
        if placement.execution_authorization_database_path is not None:
            if (
                not external_witness_evidence.signed_root_policy_endorsements
                or not isinstance(pinned_policy_roots, Mapping)
                or not pinned_policy_roots
                or not isinstance(root_policy_signature_max_age, timedelta)
                or root_policy_signature_max_age <= timedelta(0)
            ):
                raise ValueError("ROOT_POLICY_EVIDENCE_REQUIRED")
            root_policy_quorum = assess_root_policy_quorum(
                external_witness_evidence.signed_root_policy_endorsements,
                pinned_policy_roots=pinned_policy_roots,
                primary_root_keys=pinned_root_keys,
                trust_bundle=verified_trust_bundle,
                admission_challenge=admission_challenge.nonce,
                minimum_principals=minimum_policy_root_principals,
                signature_max_age=root_policy_signature_max_age,
                now=current,
            )
            if not root_policy_quorum.satisfied:
                raise ValueError(",".join(root_policy_quorum.reason_codes))
            if placement.root_policy_checkpoint_database_path is None:
                raise ValueError("ROOT_POLICY_CHECKPOINT_REQUIRED")
            with RootPolicyCheckpointStore(
                placement.root_policy_checkpoint_database_path
            ) as root_policy_checkpoint:
                checkpoint_result = root_policy_checkpoint.accept(
                    external_witness_evidence.signed_root_policy_endorsements,
                    verified_trust_bundle,
                    pinned_policy_roots=pinned_policy_roots,
                    primary_root_keys=pinned_root_keys,
                    admission_challenge=admission_challenge.nonce,
                    minimum_principals=minimum_policy_root_principals,
                    signature_max_age=root_policy_signature_max_age,
                    now=current,
                )
            if not checkpoint_result.accepted:
                raise ValueError(",".join(checkpoint_result.reason_codes))
            if (
                not isinstance(
                    external_witness_evidence.signed_authority_manifest_attestations,
                    tuple,
                )
                or not external_witness_evidence.signed_authority_manifest_attestations
                or not isinstance(
                    external_witness_evidence.minimum_authority_attester_principals,
                    int,
                )
                or isinstance(
                    external_witness_evidence.minimum_authority_attester_principals,
                    bool,
                )
                or external_witness_evidence.minimum_authority_attester_principals
                < 2
            ):
                raise ValueError("AUTHORITY_MANIFEST_EVIDENCE_REQUIRED")
            authority_quorum = assess_authority_manifest_quorum(
                external_witness_evidence.signed_authority_manifest_attestations,
                placement=placement,
                trust_bundle=verified_trust_bundle,
                minimum_principals=(
                    external_witness_evidence.minimum_authority_attester_principals
                ),
                signature_max_age=external_witness_evidence.signature_max_age,
                now=current,
            )
            if not authority_quorum.satisfied:
                raise ValueError(",".join(authority_quorum.reason_codes))
            assessment = replace(
                assessment,
                authority_domain_separation_verified=True,
                reason_codes=tuple(
                    reason
                    for reason in assessment.reason_codes
                    if reason != "AUTHORITY_DOMAIN_SEPARATION_NOT_ATTESTED"
                ),
            )
    store = PersistentIrreversibleLatchStore(
        placement.latch_database_path,
        latch_integrity_key,
    )
    checkpoint_key = derive_subkey(
        latch_integrity_key,
        "irreversible-latch-checkpoint-v1",
    )
    checkpoint_stores = tuple(
        CreateOnlyLatchCheckpointStore(root, checkpoint_key)
        for root in placement.witness_roots
    )
    execution_authorization_store = None
    try:
        synchronize_latch_checkpoints(
            store,
            checkpoint_stores,
            checkpointed_at=current,
        )
        head = store.head()
        expected_checkpoint_head = (
            genesis_latch_head(latch_store_id) if head is None else head
        )
        if external_witness_evidence is None:
            reason = (
                "LATCH_EXTERNAL_GENESIS_REQUIRED"
                if head is None
                else "LATCH_EXTERNAL_WITNESS_REQUIRED"
            )
            raise ValueError(reason)
        evidence = external_witness_evidence
        if verified_trust_bundle is None:
            raise ValueError("TRUST_BUNDLE_VERIFICATION_REQUIRED")
        verified_checkpoint, checkpoint_reasons = (
            verify_signed_latch_checkpoint(
                evidence.signed_latch_checkpoint_json,
                trust_bundle=verified_trust_bundle,
                signature_max_age=evidence.signature_max_age,
                now=current,
            )
        )
        if verified_checkpoint is None:
            raise ValueError(",".join(checkpoint_reasons))
        if (
            verified_checkpoint.latch_store_id != latch_store_id
            or verified_checkpoint.head != expected_checkpoint_head
        ):
            raise ValueError("LATCH_WITNESS_STATE_MISMATCH")
        quorum = assess_latch_witness_quorum(
            evidence.signed_witness_attestations,
            signed_latch_checkpoint_json=(
                evidence.signed_latch_checkpoint_json
            ),
            trust_bundle=verified_trust_bundle,
            minimum_principals=evidence.minimum_principals,
            signature_max_age=evidence.signature_max_age,
            expected_admission_challenge=admission_challenge.nonce,
            now=current,
        )
        if not quorum.satisfied:
            raise ValueError(",".join(quorum.reason_codes))
        external_witness_current = True
        if placement.execution_authorization_database_path is not None:
            execution_authorization_store = PersistentNonceStore(
                placement.execution_authorization_database_path,
                derive_subkey(
                    latch_integrity_key,
                    "execution-authorization-nonce-v1",
                ),
            )
        admission_challenge.consume()
        return AdmittedBoundaryRuntime(
            placement=placement,
            deployment_assessment=assessment,
            latch_store=store,
            checkpoint_stores=checkpoint_stores,
            latch_store_id=latch_store_id,
            external_witness_current=external_witness_current,
            trust_bundle=verified_trust_bundle,
            execution_authorization_signature_max_age=(
                evidence.signature_max_age
            ),
            execution_authorization_store=execution_authorization_store,
            minimum_execution_authorizer_principals=(
                minimum_execution_authorizer_principals
            ),
            execution_executor=execution_executor,
            hard_invariant_checker=hard_invariant_checker,
            _admission_token=_ADMISSION_TOKEN,
        )
    except Exception:
        if execution_authorization_store is not None:
            execution_authorization_store.close()
        store.close()
        raise


def _valid_latch_store_id(value: object) -> bool:
    return (
        isinstance(value, str)
        and 0 < len(value) <= 128
        and not any(character.isspace() for character in value)
    )
