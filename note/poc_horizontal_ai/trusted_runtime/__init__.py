"""Trusted-side PoC services kept outside the shadow decision kernel."""

from .anchor_store import AnchorReceipt, AuditAnchorStore, verify_anchor_receipt
from .authenticated_witness import (
    AuthenticatedWitnessQuorum,
    VerifiedWitnessAttestation,
    assess_authenticated_witness_quorum,
    create_signed_witness_attestation,
    verify_witness_attestation,
)
from .auth import (
    AuthenticatedPayloadResult,
    authenticate_payload,
    derive_subkey,
    verify_authenticated_payload,
)
from .checkpoint_attestation import (
    CheckpointWitnessStateStore,
    CheckpointWitnessQuorum,
    VerifiedCheckpointAttestation,
    assess_checkpoint_witness_quorum,
    create_checkpoint_attestation,
    verify_checkpoint_attestation,
)
from .asymmetric_auth import (
    SignedPayloadResult,
    load_ed25519_private_key,
    load_ed25519_public_key,
    public_key_fingerprint,
    sign_payload_ed25519,
    verify_signed_payload_ed25519,
)
from .nonce_store import NonceConsumeResult, PersistentNonceStore
from .runtime_admission import (
    AdmittedSigner,
    admit_file_signer,
    load_bounded_text_file,
)
from .deployment_boundary import (
    DeploymentBoundaryAssessment,
    RuntimePlacement,
    assess_runtime_placement,
)
from .observer_gateway import (
    AuthenticatedObservationResult,
    process_observation_request,
    verify_authenticated_observation,
)
from .signed_boundary import (
    SignedAnchorReceiptResult,
    SignedObservationResult,
    anchor_and_sign_bundle,
    process_signed_observation_request,
    verify_signed_anchor_receipt,
    verify_signed_observation,
)
from .role_verification import RoleSignedPayloadResult, verify_role_signed_payload
from .trust_bundle import (
    KeyRole,
    TrustedKeyRecord,
    TrustedKeySpec,
    TrustBundleVerification,
    VerifiedTrustBundle,
    create_signed_trust_bundle,
    verify_signed_trust_bundle,
)
from .trust_checkpoint import TrustBundleCheckpointStore, TrustCheckpointResult
from .trusted_verification import (
    verify_trusted_anchor_receipt,
    verify_trusted_observation,
)
from .witness_store import (
    CreateOnlyWitnessStore,
    WitnessQuorumAssessment,
    WitnessRecord,
    assess_witness_quorum,
)

__all__ = [
    "AnchorReceipt",
    "AdmittedSigner",
    "AuditAnchorStore",
    "AuthenticatedObservationResult",
    "AuthenticatedPayloadResult",
    "AuthenticatedWitnessQuorum",
    "CheckpointWitnessQuorum",
    "CheckpointWitnessStateStore",
    "CreateOnlyWitnessStore",
    "DeploymentBoundaryAssessment",
    "KeyRole",
    "NonceConsumeResult",
    "PersistentNonceStore",
    "RuntimePlacement",
    "RoleSignedPayloadResult",
    "SignedPayloadResult",
    "WitnessQuorumAssessment",
    "WitnessRecord",
    "SignedAnchorReceiptResult",
    "SignedObservationResult",
    "TrustBundleCheckpointStore",
    "TrustBundleVerification",
    "TrustCheckpointResult",
    "TrustedKeyRecord",
    "TrustedKeySpec",
    "VerifiedTrustBundle",
    "VerifiedCheckpointAttestation",
    "VerifiedWitnessAttestation",
    "authenticate_payload",
    "admit_file_signer",
    "anchor_and_sign_bundle",
    "assess_authenticated_witness_quorum",
    "assess_checkpoint_witness_quorum",
    "assess_runtime_placement",
    "assess_witness_quorum",
    "derive_subkey",
    "create_signed_trust_bundle",
    "create_checkpoint_attestation",
    "create_signed_witness_attestation",
    "load_ed25519_private_key",
    "load_ed25519_public_key",
    "load_bounded_text_file",
    "process_observation_request",
    "process_signed_observation_request",
    "public_key_fingerprint",
    "sign_payload_ed25519",
    "verify_authenticated_observation",
    "verify_authenticated_payload",
    "verify_anchor_receipt",
    "verify_signed_anchor_receipt",
    "verify_signed_observation",
    "verify_signed_payload_ed25519",
    "verify_signed_trust_bundle",
    "verify_checkpoint_attestation",
    "verify_role_signed_payload",
    "verify_witness_attestation",
    "verify_trusted_anchor_receipt",
    "verify_trusted_observation",
]
