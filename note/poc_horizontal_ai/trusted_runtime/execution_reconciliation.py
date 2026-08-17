"""Reconcile independently signed file observations with journaled intent."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import json

from .execution_observation import ExecutionFileObservationRequest, assess_execution_file_observation_quorum, verify_signed_execution_file_observation
from .nonce_store import ExecutionReconciliationResult, PersistentNonceStore
from .trust_bundle import VerifiedTrustBundle


def reconcile_execution_file_observations(
    *, journal: PersistentNonceStore, attempt_id: str,
    requested_observations: tuple[tuple[ExecutionFileObservationRequest, str], ...],
    trust_bundle: VerifiedTrustBundle, minimum_principals: int,
    signature_max_age: timedelta, observation_max_age: timedelta,
    now: datetime | None = None,
) -> ExecutionReconciliationResult:
    current = now or datetime.now(timezone.utc)
    if (
        current.tzinfo is None
        or not isinstance(requested_observations, tuple)
        or not requested_observations
        or any(
            not isinstance(item, tuple)
            or len(item) != 2
            or not isinstance(item[0], ExecutionFileObservationRequest)
            or not isinstance(item[1], str)
            for item in requested_observations
        )
        or not isinstance(minimum_principals, int)
        or isinstance(minimum_principals, bool)
        or minimum_principals < 2
        or not isinstance(signature_max_age, timedelta)
        or signature_max_age <= timedelta(0)
        or not isinstance(observation_max_age, timedelta)
        or observation_max_age <= timedelta(0)
    ):
        return ExecutionReconciliationResult(
            False,
            None,
            None,
            ("EXECUTION_RECONCILIATION_EVIDENCE_INVALID",),
        )
    evidence_digest = hashlib.sha256(json.dumps([signed for _, signed in requested_observations], ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()
    quorum, reasons = assess_execution_file_observation_quorum(requested_observations, trust_bundle=trust_bundle, minimum_principals=minimum_principals, signature_max_age=signature_max_age, observation_max_age=observation_max_age, now=current)
    if quorum is not None:
        return journal.record_execution_reconciliation(attempt_id=attempt_id, evidence_kind="QUORUM", evidence_digest=evidence_digest, observer_principal_ids=quorum.principal_ids, reconciled_at=current, observation_attempt_id=quorum.attempt_id, observation_intent_id=quorum.intent_id, observation_target_id=quorum.target_id, observation_subject=quorum.observation_subject, observation_field=quorum.observation_field, observed_value=quorum.observed_value)
    if reasons == ("EXECUTION_OBSERVATION_QUORUM_CONFLICT",):
        principals = []
        for request, signed_observation in requested_observations:
            observation, observation_reasons = verify_signed_execution_file_observation(signed_observation, request=request, trust_bundle=trust_bundle, signature_max_age=signature_max_age, observation_max_age=observation_max_age, now=current)
            if observation is None or observation_reasons:
                principals = []
                break
            principals.append(observation.observer_principal_id)
        principal_ids = tuple(sorted(set(principals)))
        if len(principal_ids) >= minimum_principals:
            return journal.record_execution_reconciliation(attempt_id=attempt_id, evidence_kind="CONFLICT", evidence_digest=evidence_digest, observer_principal_ids=principal_ids, reconciled_at=current)
    return journal.record_execution_reconciliation(attempt_id=attempt_id, evidence_kind="INSUFFICIENT", evidence_digest=evidence_digest, observer_principal_ids=(), reconciled_at=current)
