import hashlib
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from note.poc_horizontal_ai.trusted_runtime import (
    AdmittedSigner,
    KeyRole,
    PersistentNonceStore,
    TrustBundleCheckpointStore,
    TrustedKeySpec,
    WitnessRecord,
    assess_authenticated_witness_quorum,
    create_signed_trust_bundle,
    create_signed_witness_attestation,
    process_signed_observation_request,
    sign_payload_ed25519,
    verify_role_signed_payload,
    verify_signed_trust_bundle,
    verify_trusted_observation,
)
from note.poc_horizontal_ai.safety_kernel import (
    ObservationRequest,
    encode_observation_request,
)


class TrustBundleLifecycleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime.now(timezone.utc)
        self.root = Ed25519PrivateKey.generate()
        self.old_observer = Ed25519PrivateKey.generate()
        self.new_observer = Ed25519PrivateKey.generate()
        self.anchor = Ed25519PrivateKey.generate()

    def spec(
        self,
        key_id: str,
        principal_id: str,
        role: KeyRole,
        private: Ed25519PrivateKey,
        *,
        revoked_at: datetime | None = None,
    ) -> TrustedKeySpec:
        return TrustedKeySpec(
            key_id,
            principal_id,
            role,
            private.public_key(),
            self.now - timedelta(days=1),
            self.now + timedelta(days=30),
            revoked_at,
        )

    def generation_one(self) -> str:
        return create_signed_trust_bundle(
            generation=1,
            keys=(
                self.spec(
                    "observer-old",
                    "observer-principal",
                    KeyRole.OBSERVER_SIGNER,
                    self.old_observer,
                ),
                self.spec(
                    "anchor-key",
                    "anchor-principal",
                    KeyRole.ANCHOR_SIGNER,
                    self.anchor,
                ),
            ),
            root_key_id="offline-root-v1",
            root_private_key=self.root,
            issued_at=self.now - timedelta(seconds=2),
        )

    def generation_two(self, generation_one: str) -> str:
        return create_signed_trust_bundle(
            generation=2,
            keys=(
                self.spec(
                    "observer-old",
                    "observer-principal",
                    KeyRole.OBSERVER_SIGNER,
                    self.old_observer,
                    revoked_at=self.now - timedelta(seconds=1),
                ),
                self.spec(
                    "observer-new",
                    "observer-principal",
                    KeyRole.OBSERVER_SIGNER,
                    self.new_observer,
                ),
                self.spec(
                    "anchor-key",
                    "anchor-principal",
                    KeyRole.ANCHOR_SIGNER,
                    self.anchor,
                ),
            ),
            root_key_id="offline-root-v1",
            root_private_key=self.root,
            issued_at=self.now - timedelta(seconds=1),
            previous_signed_bundle_json=generation_one,
        )

    def test_rotation_revokes_old_key_and_preserves_role_boundary(self) -> None:
        first = self.generation_one()
        second = self.generation_two(first)
        verified = verify_signed_trust_bundle(
            second,
            pinned_root_keys={"offline-root-v1": self.root.public_key()},
            signature_max_age=timedelta(seconds=10),
            now=self.now,
        )
        self.assertEqual(verified.reason_codes, ())
        assert verified.bundle is not None
        new_record = verified.bundle.record_for("observer-new")
        assert new_record is not None
        admitted_signer = AdmittedSigner(
            new_record,
            verified.bundle,
            self.new_observer,
        )
        old_signed = sign_payload_ed25519(
            '{"observation":1}',
            key_id="observer-old",
            private_key=self.old_observer,
            issued_at=self.now,
        )
        old_result = verify_role_signed_payload(
            old_signed,
            trust_bundle=verified.bundle,
            required_role=KeyRole.OBSERVER_SIGNER,
            signature_max_age=timedelta(seconds=5),
            now=self.now,
        )
        self.assertIsNone(old_result.payload_json)
        self.assertIn("SIGNATURE_KEY_NOT_ACTIVE", old_result.reason_codes)

        new_signed = sign_payload_ed25519(
            '{"observation":1}',
            key_id="observer-new",
            private_key=self.new_observer,
            issued_at=self.now,
        )
        new_result = verify_role_signed_payload(
            new_signed,
            trust_bundle=verified.bundle,
            required_role=KeyRole.OBSERVER_SIGNER,
            signature_max_age=timedelta(seconds=5),
            now=self.now,
        )
        self.assertEqual(new_result.reason_codes, ())

        request = ObservationRequest(
            "rotated-observation-1",
            "0123456789abcdef0123456789abcdef",
            "AGENTS.md",
            41,
            self.now - timedelta(seconds=1),
        )
        with tempfile.TemporaryDirectory() as directory:
            with PersistentNonceStore(
                Path(directory) / "nonce.sqlite3",
                b"N" * 32,
            ) as nonce_store:
                signed_observation = process_signed_observation_request(
                    encode_observation_request(request),
                    repository_root=Path.cwd(),
                    observer_id="rotated-observer-v1",
                    nonce_store=nonce_store,
                    signing_key_id="observer-new",
                    signing_key=self.new_observer,
                    admitted_signer=admitted_signer,
                    request_max_age=timedelta(seconds=5),
                    now=self.now,
                )
        trusted_observation = verify_trusted_observation(
            signed_observation,
            trust_bundle=verified.bundle,
            request=request,
            repository_root=Path.cwd(),
            expected_observer_id="rotated-observer-v1",
            signature_max_age=timedelta(seconds=5),
            observation_max_age=timedelta(seconds=5),
            now=self.now,
        )
        self.assertEqual(trusted_observation.reason_codes, ())

        wrong_role = sign_payload_ed25519(
            '{"observation":1}',
            key_id="anchor-key",
            private_key=self.anchor,
            issued_at=self.now,
        )
        wrong_result = verify_role_signed_payload(
            wrong_role,
            trust_bundle=verified.bundle,
            required_role=KeyRole.OBSERVER_SIGNER,
            signature_max_age=timedelta(seconds=5),
            now=self.now,
        )
        self.assertIn("SIGNATURE_ROLE_MISMATCH", wrong_result.reason_codes)

    def test_checkpoint_rejects_rollback_gap_and_wrong_previous(self) -> None:
        first = self.generation_one()
        second = self.generation_two(first)
        third_from_first = create_signed_trust_bundle(
            generation=3,
            keys=(
                self.spec(
                    "observer-new",
                    "observer-principal",
                    KeyRole.OBSERVER_SIGNER,
                    self.new_observer,
                ),
                self.spec(
                    "anchor-key",
                    "anchor-principal",
                    KeyRole.ANCHOR_SIGNER,
                    self.anchor,
                ),
            ),
            root_key_id="offline-root-v1",
            root_private_key=self.root,
            issued_at=self.now,
            previous_signed_bundle_json=first,
        )
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "trust.sqlite3"
            with TrustBundleCheckpointStore(database) as store:
                accepted_first = store.accept(
                    first,
                    pinned_root_keys={"offline-root-v1": self.root.public_key()},
                    signature_max_age=timedelta(seconds=10),
                    now=self.now,
                )
                self.assertTrue(accepted_first.accepted)
                accepted_second = store.accept(
                    second,
                    pinned_root_keys={"offline-root-v1": self.root.public_key()},
                    signature_max_age=timedelta(seconds=10),
                    now=self.now,
                )
                self.assertTrue(accepted_second.accepted)
                rollback = store.accept(
                    first,
                    pinned_root_keys={"offline-root-v1": self.root.public_key()},
                    signature_max_age=timedelta(seconds=10),
                    now=self.now,
                )
                self.assertEqual(rollback.reason_codes, ("TRUST_BUNDLE_ROLLBACK",))
                wrong_previous = store.accept(
                    third_from_first,
                    pinned_root_keys={"offline-root-v1": self.root.public_key()},
                    signature_max_age=timedelta(seconds=10),
                    now=self.now,
                )
                self.assertEqual(
                    wrong_previous.reason_codes,
                    ("TRUST_BUNDLE_PREVIOUS_DIGEST_MISMATCH",),
                )
                self.assertEqual(
                    store.verify(
                        pinned_root_keys={
                            "offline-root-v1": self.root.public_key()
                        },
                        signature_max_age=timedelta(seconds=10),
                        now=self.now,
                    ),
                    (),
                )
                self.assertEqual(
                    store.verify(
                        pinned_root_keys={
                            "offline-root-v1": self.root.public_key()
                        },
                        signature_max_age=None,
                        now=self.now + timedelta(days=365),
                    ),
                    (),
                )
            gap_database = Path(directory) / "trust-gap.sqlite3"
            with TrustBundleCheckpointStore(gap_database) as gap_store:
                gap_store.accept(
                    first,
                    pinned_root_keys={"offline-root-v1": self.root.public_key()},
                    signature_max_age=timedelta(seconds=10),
                    now=self.now,
                )
                gap = gap_store.accept(
                    third_from_first,
                    pinned_root_keys={"offline-root-v1": self.root.public_key()},
                    signature_max_age=timedelta(seconds=10),
                    now=self.now,
                )
                self.assertEqual(
                    gap.reason_codes,
                    ("TRUST_BUNDLE_GENERATION_GAP",),
                )

    def test_same_public_key_cannot_hold_multiple_roles(self) -> None:
        with self.assertRaises(ValueError):
            create_signed_trust_bundle(
                generation=1,
                keys=(
                    self.spec(
                        "shared-observer",
                        "observer-principal",
                        KeyRole.OBSERVER_SIGNER,
                        self.old_observer,
                    ),
                    self.spec(
                        "shared-anchor",
                        "anchor-principal",
                        KeyRole.ANCHOR_SIGNER,
                        self.old_observer,
                    ),
                ),
                root_key_id="offline-root-v1",
                root_private_key=self.root,
                issued_at=self.now,
            )


class AuthenticatedWitnessIdentityTests(unittest.TestCase):
    def test_quorum_counts_distinct_principals_not_rotated_keys(self) -> None:
        now = datetime.now(timezone.utc)
        root = Ed25519PrivateKey.generate()
        witness_a1 = Ed25519PrivateKey.generate()
        witness_a2 = Ed25519PrivateKey.generate()
        witness_b = Ed25519PrivateKey.generate()
        signed_bundle = create_signed_trust_bundle(
            generation=1,
            keys=tuple(
                TrustedKeySpec(
                    key_id,
                    principal,
                    KeyRole.WITNESS_SIGNER,
                    private.public_key(),
                    now - timedelta(days=1),
                    now + timedelta(days=1),
                )
                for key_id, principal, private in (
                    ("witness-a-old", "witness-a", witness_a1),
                    ("witness-a-new", "witness-a", witness_a2),
                    ("witness-b-key", "witness-b", witness_b),
                )
            ),
            root_key_id="offline-root-v1",
            root_private_key=root,
            issued_at=now,
        )
        verified = verify_signed_trust_bundle(
            signed_bundle,
            pinned_root_keys={"offline-root-v1": root.public_key()},
            signature_max_age=timedelta(seconds=5),
            now=now,
        )
        assert verified.bundle is not None
        receipt_text = "signed anchor receipt"
        receipt_digest = hashlib.sha256(receipt_text.encode("utf-8")).hexdigest()
        head = "a" * 64
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            signed_attestations = []
            for index, (key_id, principal, private) in enumerate(
                (
                    ("witness-a-old", "witness-a", witness_a1),
                    ("witness-a-new", "witness-a", witness_a2),
                    ("witness-b-key", "witness-b", witness_b),
                ),
                1,
            ):
                record_path = temporary / f"record-{index}.json"
                record_path.write_text(receipt_text, encoding="utf-8")
                record = WitnessRecord(
                    principal,
                    head,
                    receipt_digest,
                    record_path,
                )
                key_record = verified.bundle.record_for(key_id)
                assert key_record is not None
                signed_attestations.append(
                    create_signed_witness_attestation(
                        record,
                        attestation_id=f"attestation-{index}",
                        witness_principal_id=principal,
                        witness_sequence=index,
                        witness_key_id=key_id,
                        witness_private_key=private,
                        admitted_signer=AdmittedSigner(
                            key_record,
                            verified.bundle,
                            private,
                        ),
                        witnessed_at=now,
                    )
                )
            only_a = assess_authenticated_witness_quorum(
                signed_attestations[:2],
                trust_bundle=verified.bundle,
                audit_head_digest=head,
                signed_receipt_sha256=receipt_digest,
                minimum_principals=2,
                signature_max_age=timedelta(seconds=5),
                now=now,
            )
            self.assertFalse(only_a.satisfied)
            self.assertEqual(only_a.principal_ids, ("witness-a",))
            with_b = assess_authenticated_witness_quorum(
                signed_attestations,
                trust_bundle=verified.bundle,
                audit_head_digest=head,
                signed_receipt_sha256=receipt_digest,
                minimum_principals=2,
                signature_max_age=timedelta(seconds=5),
                now=now,
            )
            self.assertTrue(with_b.satisfied)
            self.assertEqual(with_b.principal_ids, ("witness-a", "witness-b"))


if __name__ == "__main__":
    unittest.main()
