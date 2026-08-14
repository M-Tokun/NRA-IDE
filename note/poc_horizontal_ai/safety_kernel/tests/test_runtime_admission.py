import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from note.poc_horizontal_ai.trusted_runtime import (
    KeyRole,
    TrustedKeySpec,
    admit_file_signer,
    create_checkpoint_attestation,
    create_signed_trust_bundle,
    sign_payload_ed25519,
    verify_role_signed_payload,
    verify_signed_trust_bundle,
)


class RuntimeAdmissionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime.now(timezone.utc)
        self.root = Ed25519PrivateKey.generate()
        self.signer = Ed25519PrivateKey.generate()
        self.witness_a = Ed25519PrivateKey.generate()
        self.witness_b = Ed25519PrivateKey.generate()

    def _write_private(self, path: Path, key: Ed25519PrivateKey) -> None:
        path.write_bytes(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
        path.chmod(0o600)

    def _write_root_public(self, path: Path) -> None:
        path.write_bytes(
            self.root.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

    def _bundle(self, role: KeyRole = KeyRole.OBSERVER_SIGNER) -> str:
        return create_signed_trust_bundle(
            generation=1,
            keys=(
                TrustedKeySpec(
                    "runtime-key-v1",
                    "runtime-principal",
                    role,
                    self.signer.public_key(),
                    self.now - timedelta(minutes=1),
                    self.now + timedelta(days=1),
                ),
                TrustedKeySpec(
                    "checkpoint-witness-a",
                    "checkpoint-principal-a",
                    KeyRole.WITNESS_SIGNER,
                    self.witness_a.public_key(),
                    self.now - timedelta(minutes=1),
                    self.now + timedelta(days=1),
                ),
                TrustedKeySpec(
                    "checkpoint-witness-b",
                    "checkpoint-principal-b",
                    KeyRole.WITNESS_SIGNER,
                    self.witness_b.public_key(),
                    self.now - timedelta(minutes=1),
                    self.now + timedelta(days=1),
                ),
            ),
            root_key_id="offline-root-v1",
            root_private_key=self.root,
            issued_at=self.now,
        )

    def _attestations(self, signed_bundle: str) -> tuple[str, str]:
        verification = verify_signed_trust_bundle(
            signed_bundle,
            pinned_root_keys={"offline-root-v1": self.root.public_key()},
            signature_max_age=timedelta(seconds=5),
            now=self.now,
        )
        assert verification.bundle is not None
        return tuple(
            create_checkpoint_attestation(
                trust_bundle=verification.bundle,
                attestation_id=f"checkpoint-attestation-{index}",
                witness_principal_id=principal,
                witness_sequence=1,
                witness_key_id=key_id,
                witness_private_key=private,
                witnessed_at=self.now,
            )
            for index, (key_id, principal, private) in enumerate(
                (
                    (
                        "checkpoint-witness-a",
                        "checkpoint-principal-a",
                        self.witness_a,
                    ),
                    (
                        "checkpoint-witness-b",
                        "checkpoint-principal-b",
                        self.witness_b,
                    ),
                ),
                1,
            )
        )

    def test_admission_reuses_checkpoint_and_binds_signed_payload(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            bundle_path = temporary / "trust-bundle.json"
            root_path = temporary / "root-public.pem"
            signer_path = temporary / "signer-private.pem"
            signed_bundle = self._bundle()
            bundle_path.write_text(signed_bundle, encoding="utf-8")
            self._write_root_public(root_path)
            self._write_private(signer_path, self.signer)
            arguments = {
                "signed_bundle_path": bundle_path,
                "checkpoint_database_path": temporary / "trust.sqlite3",
                "pinned_root_key_id": "offline-root-v1",
                "pinned_root_public_key_path": root_path,
                "signing_key_id": "runtime-key-v1",
                "signing_key_path": signer_path,
                "required_role": KeyRole.OBSERVER_SIGNER,
                "bundle_max_age": timedelta(seconds=10),
                "signed_checkpoint_attestations": self._attestations(
                    signed_bundle
                ),
                "minimum_checkpoint_witness_principals": 2,
                "checkpoint_attestation_max_age": timedelta(seconds=10),
                "now": self.now,
            }
            admitted = admit_file_signer(**arguments)
            admitted_again = admit_file_signer(**arguments)
            self.assertEqual(
                admitted.trust_bundle.signed_bundle_sha256,
                admitted_again.trust_bundle.signed_bundle_sha256,
            )
            signed = admitted.sign_payload('{"observed":true}', issued_at=self.now)
            envelope = json.loads(signed)
            self.assertEqual(envelope["schema_version"], "signed-payload/1.1")
            self.assertEqual(envelope["trust_bundle_generation"], 1)
            verified = verify_role_signed_payload(
                signed,
                trust_bundle=admitted.trust_bundle,
                required_role=KeyRole.OBSERVER_SIGNER,
                signature_max_age=timedelta(seconds=5),
                require_trust_binding=True,
                now=self.now,
            )
            self.assertEqual(verified.reason_codes, ())

    def test_admission_rejects_role_and_private_key_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            bundle_path = temporary / "trust-bundle.json"
            root_path = temporary / "root-public.pem"
            signer_path = temporary / "signer-private.pem"
            signed_bundle = self._bundle(KeyRole.ANCHOR_SIGNER)
            bundle_path.write_text(signed_bundle, encoding="utf-8")
            self._write_root_public(root_path)
            self._write_private(signer_path, self.signer)
            common = {
                "signed_bundle_path": bundle_path,
                "pinned_root_key_id": "offline-root-v1",
                "pinned_root_public_key_path": root_path,
                "signing_key_id": "runtime-key-v1",
                "signing_key_path": signer_path,
                "bundle_max_age": timedelta(seconds=10),
                "signed_checkpoint_attestations": self._attestations(
                    signed_bundle
                ),
                "minimum_checkpoint_witness_principals": 2,
                "checkpoint_attestation_max_age": timedelta(seconds=10),
                "now": self.now,
            }
            with self.assertRaisesRegex(ValueError, "SIGNER_ROLE_MISMATCH"):
                admit_file_signer(
                    checkpoint_database_path=temporary / "role.sqlite3",
                    required_role=KeyRole.OBSERVER_SIGNER,
                    **common,
                )
            self.assertFalse((temporary / "role.sqlite3").exists())
            wrong_path = temporary / "wrong-private.pem"
            self._write_private(wrong_path, Ed25519PrivateKey.generate())
            common["signing_key_path"] = wrong_path
            with self.assertRaisesRegex(
                ValueError,
                "SIGNER_PRIVATE_KEY_MISMATCH",
            ):
                admit_file_signer(
                    checkpoint_database_path=temporary / "key.sqlite3",
                    required_role=KeyRole.ANCHOR_SIGNER,
                    **common,
                )
            self.assertFalse((temporary / "key.sqlite3").exists())

    def test_admission_rejects_revoked_key_before_checkpoint_update(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            root_path = temporary / "root-public.pem"
            signer_path = temporary / "signer-private.pem"
            bundle_path = temporary / "revoked-bundle.json"
            self._write_root_public(root_path)
            self._write_private(signer_path, self.signer)
            signed_bundle = create_signed_trust_bundle(
                generation=1,
                keys=(
                    TrustedKeySpec(
                        "runtime-key-v1",
                        "runtime-principal",
                        KeyRole.OBSERVER_SIGNER,
                        self.signer.public_key(),
                        self.now - timedelta(minutes=1),
                        self.now + timedelta(days=1),
                        self.now - timedelta(seconds=1),
                    ),
                    TrustedKeySpec(
                        "checkpoint-witness-a",
                        "checkpoint-principal-a",
                        KeyRole.WITNESS_SIGNER,
                        self.witness_a.public_key(),
                        self.now - timedelta(minutes=1),
                        self.now + timedelta(days=1),
                    ),
                    TrustedKeySpec(
                        "checkpoint-witness-b",
                        "checkpoint-principal-b",
                        KeyRole.WITNESS_SIGNER,
                        self.witness_b.public_key(),
                        self.now - timedelta(minutes=1),
                        self.now + timedelta(days=1),
                    ),
                ),
                root_key_id="offline-root-v1",
                root_private_key=self.root,
                issued_at=self.now,
            )
            bundle_path.write_text(signed_bundle, encoding="utf-8")
            checkpoint_path = temporary / "revoked.sqlite3"
            with self.assertRaisesRegex(ValueError, "SIGNER_KEY_NOT_ACTIVE"):
                admit_file_signer(
                    signed_bundle_path=bundle_path,
                    checkpoint_database_path=checkpoint_path,
                    pinned_root_key_id="offline-root-v1",
                    pinned_root_public_key_path=root_path,
                    signing_key_id="runtime-key-v1",
                    signing_key_path=signer_path,
                    required_role=KeyRole.OBSERVER_SIGNER,
                    bundle_max_age=timedelta(seconds=10),
                    signed_checkpoint_attestations=self._attestations(
                        signed_bundle
                    ),
                    minimum_checkpoint_witness_principals=2,
                    checkpoint_attestation_max_age=timedelta(seconds=10),
                    now=self.now,
                )
            self.assertFalse(checkpoint_path.exists())

    def test_admission_rejects_insufficient_external_quorum_before_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            bundle_path = temporary / "trust-bundle.json"
            root_path = temporary / "root-public.pem"
            signer_path = temporary / "signer-private.pem"
            signed_bundle = self._bundle()
            bundle_path.write_text(signed_bundle, encoding="utf-8")
            self._write_root_public(root_path)
            self._write_private(signer_path, self.signer)
            checkpoint_path = temporary / "insufficient.sqlite3"
            with self.assertRaisesRegex(
                ValueError,
                "CHECKPOINT_WITNESS_QUORUM_NOT_REACHED",
            ):
                admit_file_signer(
                    signed_bundle_path=bundle_path,
                    checkpoint_database_path=checkpoint_path,
                    pinned_root_key_id="offline-root-v1",
                    pinned_root_public_key_path=root_path,
                    signing_key_id="runtime-key-v1",
                    signing_key_path=signer_path,
                    required_role=KeyRole.OBSERVER_SIGNER,
                    bundle_max_age=timedelta(seconds=10),
                    signed_checkpoint_attestations=self._attestations(
                        signed_bundle
                    )[:1],
                    minimum_checkpoint_witness_principals=2,
                    checkpoint_attestation_max_age=timedelta(seconds=10),
                    now=self.now,
                )
            self.assertFalse(checkpoint_path.exists())

    def test_trusted_role_rejects_unbound_and_other_trust_state(self) -> None:
        signed_bundle = self._bundle()
        verification = verify_signed_trust_bundle(
            signed_bundle,
            pinned_root_keys={"offline-root-v1": self.root.public_key()},
            signature_max_age=timedelta(seconds=5),
            now=self.now,
        )
        assert verification.bundle is not None
        unbound = sign_payload_ed25519(
            "{}",
            key_id="runtime-key-v1",
            private_key=self.signer,
            issued_at=self.now,
        )
        missing = verify_role_signed_payload(
            unbound,
            trust_bundle=verification.bundle,
            required_role=KeyRole.OBSERVER_SIGNER,
            signature_max_age=timedelta(seconds=5),
            require_trust_binding=True,
            now=self.now,
        )
        self.assertEqual(missing.reason_codes, ("TRUST_STATE_BINDING_REQUIRED",))
        mismatched = sign_payload_ed25519(
            "{}",
            key_id="runtime-key-v1",
            private_key=self.signer,
            issued_at=self.now,
            trust_bundle_generation=1,
            trust_bundle_sha256="0" * 64,
        )
        mismatch = verify_role_signed_payload(
            mismatched,
            trust_bundle=verification.bundle,
            required_role=KeyRole.OBSERVER_SIGNER,
            signature_max_age=timedelta(seconds=5),
            require_trust_binding=True,
            now=self.now,
        )
        self.assertEqual(mismatch.reason_codes, ("TRUST_STATE_BINDING_MISMATCH",))


if __name__ == "__main__":
    unittest.main()
