"""Fail-closed signer admission bound to the latest accepted trust state."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Sequence

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .asymmetric_auth import (
    load_ed25519_private_key,
    load_ed25519_public_key,
    public_key_fingerprint,
    sign_payload_ed25519,
)
from .checkpoint_attestation import assess_checkpoint_witness_quorum
from .trust_bundle import (
    KeyRole,
    TrustedKeyRecord,
    VerifiedTrustBundle,
    verify_signed_trust_bundle,
)
from .trust_checkpoint import TrustBundleCheckpointStore


@dataclass(frozen=True, slots=True)
class AdmittedSigner:
    key_record: TrustedKeyRecord
    trust_bundle: VerifiedTrustBundle
    private_key: Ed25519PrivateKey

    def sign_payload(self, payload_json: str, *, issued_at: datetime) -> str:
        return sign_payload_ed25519(
            payload_json,
            key_id=self.key_record.key_id,
            private_key=self.private_key,
            issued_at=issued_at,
            trust_bundle_generation=self.trust_bundle.generation,
            trust_bundle_sha256=self.trust_bundle.signed_bundle_sha256,
        )


def admit_file_signer(
    *,
    signed_bundle_path: Path,
    checkpoint_database_path: Path,
    pinned_root_key_id: str,
    pinned_root_public_key_path: Path,
    signing_key_id: str,
    signing_key_path: Path,
    required_role: KeyRole,
    bundle_max_age: timedelta,
    signed_checkpoint_attestations: Sequence[str],
    minimum_checkpoint_witness_principals: int,
    checkpoint_attestation_max_age: timedelta,
    now: datetime | None = None,
) -> AdmittedSigner:
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None or bundle_max_age <= timedelta(0):
        raise ValueError("invalid signer admission time policy")
    current = current.astimezone(timezone.utc)
    signed_bundle_json = load_bounded_text_file(
        signed_bundle_path,
        512 * 1024,
    )
    pinned_root = load_ed25519_public_key(pinned_root_public_key_path)
    pinned_roots = {pinned_root_key_id: pinned_root}
    candidate = verify_signed_trust_bundle(
        signed_bundle_json,
        pinned_root_keys=pinned_roots,
        signature_max_age=None,
        now=current,
    )
    if candidate.bundle is None:
        raise ValueError(",".join(candidate.reason_codes))
    record = candidate.bundle.record_for(signing_key_id)
    if record is None:
        raise ValueError("SIGNER_KEY_UNKNOWN")
    if record.role is not required_role:
        raise ValueError("SIGNER_ROLE_MISMATCH")
    if not record.active_at(current):
        raise ValueError("SIGNER_KEY_NOT_ACTIVE")
    private_key = load_ed25519_private_key(signing_key_path)
    if public_key_fingerprint(private_key.public_key()) != public_key_fingerprint(
        record.public_key
    ):
        raise ValueError("SIGNER_PRIVATE_KEY_MISMATCH")
    quorum = assess_checkpoint_witness_quorum(
        signed_checkpoint_attestations,
        trust_bundle=candidate.bundle,
        minimum_principals=minimum_checkpoint_witness_principals,
        signature_max_age=checkpoint_attestation_max_age,
        now=current,
    )
    if not quorum.satisfied:
        raise ValueError(",".join(quorum.reason_codes))

    with TrustBundleCheckpointStore(checkpoint_database_path) as checkpoint:
        chain_reasons = checkpoint.verify(
            pinned_root_keys=pinned_roots,
            signature_max_age=None,
            now=current,
        )
        if chain_reasons:
            raise ValueError(",".join(chain_reasons))
        latest = checkpoint.latest_signed_bundle()
        if latest is None or latest != signed_bundle_json:
            accepted = checkpoint.accept(
                signed_bundle_json,
                pinned_root_keys=pinned_roots,
                signature_max_age=bundle_max_age,
                now=current,
            )
            if not accepted.accepted or accepted.bundle is None:
                raise ValueError(",".join(accepted.reason_codes))
            bundle = accepted.bundle
        else:
            bundle = candidate.bundle
    return AdmittedSigner(record, bundle, private_key)


def load_bounded_text_file(path: Path, maximum_bytes: int) -> str:
    if path.is_symlink() or not path.is_file():
        raise ValueError("trust bundle path must be a regular non-symlink file")
    size = path.stat().st_size
    if size <= 0 or size > maximum_bytes:
        raise ValueError("trust bundle file size is outside the accepted range")
    data = path.read_bytes()
    if len(data) != size:
        raise ValueError("trust bundle file changed while reading")
    return data.decode("utf-8")
