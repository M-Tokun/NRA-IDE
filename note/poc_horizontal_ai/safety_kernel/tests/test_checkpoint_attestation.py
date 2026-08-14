import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

from note.poc_horizontal_ai.trusted_runtime import (
    KeyRole,
    CheckpointWitnessStateStore,
    TrustedKeySpec,
    assess_checkpoint_witness_quorum,
    create_checkpoint_attestation,
    create_signed_trust_bundle,
    sign_payload_ed25519,
    verify_signed_trust_bundle,
    verify_checkpoint_attestation,
)


class CheckpointAttestationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime.now(timezone.utc)
        self.root = Ed25519PrivateKey.generate()
        self.witness_a1 = Ed25519PrivateKey.generate()
        self.witness_a2 = Ed25519PrivateKey.generate()
        self.witness_b = Ed25519PrivateKey.generate()
        signed_bundle = create_signed_trust_bundle(
            generation=1,
            keys=tuple(
                TrustedKeySpec(
                    key_id,
                    principal_id,
                    KeyRole.WITNESS_SIGNER,
                    private.public_key(),
                    self.now - timedelta(minutes=1),
                    self.now + timedelta(days=1),
                )
                for key_id, principal_id, private in (
                    ("witness-a1", "principal-a", self.witness_a1),
                    ("witness-a2", "principal-a", self.witness_a2),
                    ("witness-b", "principal-b", self.witness_b),
                )
            ),
            root_key_id="offline-root-v1",
            root_private_key=self.root,
            issued_at=self.now,
        )
        verification = verify_signed_trust_bundle(
            signed_bundle,
            pinned_root_keys={"offline-root-v1": self.root.public_key()},
            signature_max_age=timedelta(seconds=5),
            now=self.now,
        )
        assert verification.bundle is not None
        self.signed_bundle = signed_bundle
        self.bundle = verification.bundle

    def _attestation(
        self,
        key_id: str,
        principal_id: str,
        private: Ed25519PrivateKey,
        sequence: int,
    ) -> str:
        return create_checkpoint_attestation(
            trust_bundle=self.bundle,
            attestation_id=f"attestation-{sequence}",
            witness_principal_id=principal_id,
            witness_sequence=sequence,
            witness_key_id=key_id,
            witness_private_key=private,
            witnessed_at=self.now,
        )

    def test_quorum_counts_distinct_principals(self) -> None:
        a1 = self._attestation("witness-a1", "principal-a", self.witness_a1, 1)
        a2 = self._attestation("witness-a2", "principal-a", self.witness_a2, 2)
        b = self._attestation("witness-b", "principal-b", self.witness_b, 3)
        one_principal = assess_checkpoint_witness_quorum(
            (a1, a2),
            trust_bundle=self.bundle,
            minimum_principals=2,
            signature_max_age=timedelta(seconds=5),
            now=self.now,
        )
        self.assertFalse(one_principal.satisfied)
        self.assertEqual(one_principal.principal_ids, ("principal-a",))
        two_principals = assess_checkpoint_witness_quorum(
            (a1, a2, b),
            trust_bundle=self.bundle,
            minimum_principals=2,
            signature_max_age=timedelta(seconds=5),
            now=self.now,
        )
        self.assertTrue(two_principals.satisfied)
        self.assertEqual(
            two_principals.principal_ids,
            ("principal-a", "principal-b"),
        )

    def test_invalid_and_state_mismatched_attestations_do_not_count(self) -> None:
        valid_b = self._attestation("witness-b", "principal-b", self.witness_b, 1)
        tampered = json.loads(
            self._attestation("witness-a1", "principal-a", self.witness_a1, 2)
        )
        tampered["signature_base64"] = "AAAA"
        mismatched_payload = json.dumps(
            {
                "attestation_id": "state-mismatch",
                "previous_bundle_sha256": None,
                "schema_version": "trust-checkpoint-attestation/1.0",
                "trust_bundle_generation": 2,
                "trust_bundle_sha256": "0" * 64,
                "witness_principal_id": "principal-a",
                "witness_sequence": 3,
                "witnessed_at": self.now.isoformat(),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        mismatched = sign_payload_ed25519(
            mismatched_payload,
            key_id="witness-a1",
            private_key=self.witness_a1,
            issued_at=self.now,
            trust_bundle_generation=self.bundle.generation,
            trust_bundle_sha256=self.bundle.signed_bundle_sha256,
        )
        result = assess_checkpoint_witness_quorum(
            (json.dumps(tampered), mismatched, valid_b),
            trust_bundle=self.bundle,
            minimum_principals=2,
            signature_max_age=timedelta(seconds=5),
            now=self.now,
        )
        self.assertFalse(result.satisfied)
        self.assertEqual(result.principal_ids, ("principal-b",))
        self.assertIn("INVALID_CHECKPOINT_ATTESTATION_IGNORED", result.reason_codes)
        self.assertIn("CHECKPOINT_ATTESTATION_STATE_MISMATCH", result.reason_codes)

    def test_witness_store_refreshes_current_state_and_rejects_rollback(self) -> None:
        second_signed = create_signed_trust_bundle(
            generation=2,
            keys=tuple(
                TrustedKeySpec(
                    key_id,
                    principal_id,
                    KeyRole.WITNESS_SIGNER,
                    private.public_key(),
                    self.now - timedelta(minutes=1),
                    self.now + timedelta(days=1),
                )
                for key_id, principal_id, private in (
                    ("witness-a1", "principal-a", self.witness_a1),
                    ("witness-a2", "principal-a", self.witness_a2),
                    ("witness-b", "principal-b", self.witness_b),
                )
            ),
            root_key_id="offline-root-v1",
            root_private_key=self.root,
            issued_at=self.now + timedelta(seconds=1),
            previous_signed_bundle_json=self.signed_bundle,
        )
        second_verification = verify_signed_trust_bundle(
            second_signed,
            pinned_root_keys={"offline-root-v1": self.root.public_key()},
            signature_max_age=timedelta(seconds=5),
            now=self.now + timedelta(seconds=1),
        )
        assert second_verification.bundle is not None
        with tempfile.TemporaryDirectory() as directory:
            with CheckpointWitnessStateStore(
                Path(directory) / "witness.sqlite3",
                "principal-a",
            ) as store:
                first = store.attest(
                    self.bundle,
                    witness_key_id="witness-a1",
                    witness_private_key=self.witness_a1,
                    witnessed_at=self.now,
                )
                refreshed = store.attest(
                    self.bundle,
                    witness_key_id="witness-a1",
                    witness_private_key=self.witness_a1,
                    witnessed_at=self.now + timedelta(milliseconds=1),
                )
                self.assertNotEqual(first, refreshed)
                store.attest(
                    second_verification.bundle,
                    witness_key_id="witness-a1",
                    witness_private_key=self.witness_a1,
                    witnessed_at=self.now + timedelta(seconds=1),
                )
                with self.assertRaisesRegex(
                    ValueError,
                    "WITNESS_TRUST_BUNDLE_ROLLBACK",
                ):
                    store.attest(
                        self.bundle,
                        witness_key_id="witness-a1",
                        witness_private_key=self.witness_a1,
                        witnessed_at=self.now + timedelta(seconds=2),
                    )

    def test_witness_service_runs_in_separate_process(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            root_path = temporary / "root-public.pem"
            witness_path = temporary / "witness-private.pem"
            root_path.write_bytes(
                self.root.public_key().public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )
            witness_path.write_bytes(
                self.witness_a1.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )
            witness_path.chmod(0o600)
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "note.poc_horizontal_ai.trusted_runtime.checkpoint_witness_service",
                    "--witness-database",
                    str(temporary / "witness.sqlite3"),
                    "--witness-principal-id",
                    "principal-a",
                    "--witness-key-id",
                    "witness-a1",
                    "--witness-private-key-file",
                    str(witness_path),
                    "--pinned-root-key-id",
                    "offline-root-v1",
                    "--pinned-root-public-key-file",
                    str(root_path),
                ],
                input=self.signed_bundle,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            verified, reasons = verify_checkpoint_attestation(
                completed.stdout,
                trust_bundle=self.bundle,
                signature_max_age=timedelta(seconds=5),
                now=datetime.now(timezone.utc),
            )
            self.assertEqual(reasons, ())
            self.assertIsNotNone(verified)


if __name__ == "__main__":
    unittest.main()
