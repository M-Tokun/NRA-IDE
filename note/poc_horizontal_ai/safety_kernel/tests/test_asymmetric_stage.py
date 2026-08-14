import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from note.poc_horizontal_ai.safety_kernel import (
    AppendOnlyHistoryLedger,
    HistoryEventKind,
    ObservationRequest,
    create_audit_bundle,
    encode_observation_request,
)
from note.poc_horizontal_ai.trusted_runtime import (
    AuditAnchorStore,
    CreateOnlyWitnessStore,
    KeyRole,
    PersistentNonceStore,
    RuntimePlacement,
    TrustedKeySpec,
    anchor_and_sign_bundle,
    assess_runtime_placement,
    assess_witness_quorum,
    create_checkpoint_attestation,
    create_signed_trust_bundle,
    process_signed_observation_request,
    sign_payload_ed25519,
    verify_signed_anchor_receipt,
    verify_signed_observation,
    verify_signed_payload_ed25519,
    verify_signed_trust_bundle,
)


def write_keys(directory: Path) -> tuple[Ed25519PrivateKey, Path, Path]:
    private = Ed25519PrivateKey.generate()
    private_path = directory / "signing-private.pem"
    public_path = directory / "signing-public.pem"
    private_path.write_bytes(
        private.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    public_path.write_bytes(
        private.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )
    private_path.chmod(0o600)
    public_path.chmod(0o644)
    return private, private_path, public_path


def make_bundle() -> tuple[str, str]:
    ledger = AppendOnlyHistoryLedger()
    ledger.append(
        event_id="event-1",
        kind=HistoryEventKind.OBSERVATION,
        target_id="repo-1",
        source_id="observer-v1",
        occurred_at="2026-08-13T00:00:00+00:00",
        payload={"state": "observed"},
    )
    bundle = create_audit_bundle(
        ledger.events,
        exported_at=datetime.now(timezone.utc),
    )
    return bundle, ledger.events[-1].digest


def write_trust_material(
    directory: Path,
    *,
    signer: Ed25519PrivateKey,
    key_id: str,
    role: KeyRole,
) -> tuple[Path, Path, tuple[Path, Path]]:
    now = datetime.now(timezone.utc)
    root = Ed25519PrivateKey.generate()
    witness_a = Ed25519PrivateKey.generate()
    witness_b = Ed25519PrivateKey.generate()
    root_public_path = directory / f"{key_id}-root-public.pem"
    root_public_path.write_bytes(
        root.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )
    signed_bundle = create_signed_trust_bundle(
        generation=1,
        keys=(
            TrustedKeySpec(
                key_id,
                f"{key_id}-principal",
                role,
                signer.public_key(),
                now - timedelta(minutes=1),
                now + timedelta(days=1),
            ),
            TrustedKeySpec(
                "checkpoint-witness-a",
                "checkpoint-principal-a",
                KeyRole.WITNESS_SIGNER,
                witness_a.public_key(),
                now - timedelta(minutes=1),
                now + timedelta(days=1),
            ),
            TrustedKeySpec(
                "checkpoint-witness-b",
                "checkpoint-principal-b",
                KeyRole.WITNESS_SIGNER,
                witness_b.public_key(),
                now - timedelta(minutes=1),
                now + timedelta(days=1),
            ),
        ),
        root_key_id="offline-root-v1",
        root_private_key=root,
        issued_at=now,
    )
    bundle_path = directory / f"{key_id}-trust-bundle.json"
    bundle_path.write_text(signed_bundle, encoding="utf-8")
    verified = verify_signed_trust_bundle(
        signed_bundle,
        pinned_root_keys={"offline-root-v1": root.public_key()},
        signature_max_age=timedelta(seconds=5),
        now=now,
    )
    assert verified.bundle is not None
    attestation_paths = []
    for index, (witness_key_id, principal, private) in enumerate(
        (
            ("checkpoint-witness-a", "checkpoint-principal-a", witness_a),
            ("checkpoint-witness-b", "checkpoint-principal-b", witness_b),
        ),
        1,
    ):
        attestation = create_checkpoint_attestation(
            trust_bundle=verified.bundle,
            attestation_id=f"{key_id}-checkpoint-{index}",
            witness_principal_id=principal,
            witness_sequence=1,
            witness_key_id=witness_key_id,
            witness_private_key=private,
            witnessed_at=now,
        )
        path = directory / f"{key_id}-checkpoint-{index}.json"
        path.write_text(attestation, encoding="utf-8")
        attestation_paths.append(path)
    return bundle_path, root_public_path, tuple(attestation_paths)


class Ed25519AuthenticationTests(unittest.TestCase):
    def test_public_key_verifies_but_cannot_sign(self) -> None:
        private = Ed25519PrivateKey.generate()
        now = datetime.now(timezone.utc)
        signed = sign_payload_ed25519(
            '{"value":1}',
            key_id="signer-v1",
            private_key=private,
            issued_at=now,
        )
        result = verify_signed_payload_ed25519(
            signed,
            trusted_public_keys={"signer-v1": private.public_key()},
            max_age=timedelta(seconds=5),
            now=now,
        )
        self.assertEqual(result.payload_json, '{"value":1}')
        tampered = json.loads(signed)
        tampered["payload_json"] = '{"value":2}'
        invalid = verify_signed_payload_ed25519(
            json.dumps(tampered),
            trusted_public_keys={"signer-v1": private.public_key()},
            max_age=timedelta(seconds=5),
            now=now,
        )
        self.assertIsNone(invalid.payload_json)
        self.assertIn("SIGNATURE_INVALID", invalid.reason_codes)

        wrong_key = Ed25519PrivateKey.generate().public_key()
        wrong = verify_signed_payload_ed25519(
            signed,
            trusted_public_keys={"signer-v1": wrong_key},
            max_age=timedelta(seconds=5),
            now=now,
        )
        self.assertIsNone(wrong.payload_json)
        self.assertIn("SIGNATURE_KEY_FINGERPRINT_MISMATCH", wrong.reason_codes)
        self.assertIn("SIGNATURE_INVALID", wrong.reason_codes)


class SignedObservationTests(unittest.TestCase):
    def test_observation_is_signed_and_replay_consumption_persists(self) -> None:
        private = Ed25519PrivateKey.generate()
        now = datetime.now(timezone.utc)
        request = ObservationRequest(
            "signed-observation-1",
            "0123456789abcdef0123456789abcdef",
            "AGENTS.md",
            31,
            now - timedelta(seconds=1),
        )
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "nonce.sqlite3"
            with PersistentNonceStore(database, b"L" * 32) as store:
                signed = process_signed_observation_request(
                    encode_observation_request(request),
                    repository_root=Path.cwd(),
                    observer_id="ed25519-observer-v1",
                    nonce_store=store,
                    signing_key_id="observer-signing-v1",
                    signing_key=private,
                    request_max_age=timedelta(seconds=5),
                    now=now,
                )
            verified = verify_signed_observation(
                signed,
                request=request,
                repository_root=Path.cwd(),
                expected_observer_id="ed25519-observer-v1",
                trusted_public_keys={"observer-signing-v1": private.public_key()},
                signature_max_age=timedelta(seconds=5),
                observation_max_age=timedelta(seconds=5),
                now=datetime.now(timezone.utc),
            )
            self.assertEqual(verified.reason_codes, ())
            self.assertIsNotNone(verified.evidence)

    def test_observer_signer_runs_in_separate_process(self) -> None:
        request = ObservationRequest(
            "signed-service-1",
            "fedcba9876543210fedcba9876543210",
            "AGENTS.md",
            32,
            datetime.now(timezone.utc),
        )
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            private, private_path, _ = write_keys(temporary)
            trust_bundle, root_public, checkpoint_attestations = (
                write_trust_material(
                temporary,
                signer=private,
                key_id="observer-signing-v1",
                role=KeyRole.OBSERVER_SIGNER,
                )
            )
            ledger_key = temporary / "ledger.key"
            ledger_key.write_bytes(b"Q" * 32)
            ledger_key.chmod(0o600)
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "note.poc_horizontal_ai.trusted_runtime.ed25519_observer_service",
                    "--repository-root",
                    str(Path.cwd()),
                    "--observer-id",
                    "ed25519-observer-v1",
                    "--nonce-database",
                    str(temporary / "nonce.sqlite3"),
                    "--ledger-key-file",
                    str(ledger_key),
                    "--signing-key-id",
                    "observer-signing-v1",
                    "--signing-key-file",
                    str(private_path),
                    "--trust-bundle-file",
                    str(trust_bundle),
                    "--trust-checkpoint-database",
                    str(temporary / "observer-trust.sqlite3"),
                    "--pinned-root-key-id",
                    "offline-root-v1",
                    "--pinned-root-public-key-file",
                    str(root_public),
                    "--trust-checkpoint-attestation-file",
                    str(checkpoint_attestations[0]),
                    "--trust-checkpoint-attestation-file",
                    str(checkpoint_attestations[1]),
                ],
                input=encode_observation_request(request),
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(
                json.loads(completed.stdout)["schema_version"],
                "signed-payload/1.1",
            )
            verified = verify_signed_observation(
                completed.stdout,
                request=request,
                repository_root=Path.cwd(),
                expected_observer_id="ed25519-observer-v1",
                trusted_public_keys={"observer-signing-v1": private.public_key()},
                signature_max_age=timedelta(seconds=5),
                observation_max_age=timedelta(seconds=5),
                now=datetime.now(timezone.utc),
            )
            self.assertEqual(verified.reason_codes, ())


class SignedAnchorWitnessTests(unittest.TestCase):
    def test_signed_anchor_reaches_two_witness_quorum(self) -> None:
        private = Ed25519PrivateKey.generate()
        bundle, head = make_bundle()
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            with AuditAnchorStore(temporary / "anchor.sqlite3", b"A" * 32) as store:
                signed = anchor_and_sign_bundle(
                    bundle,
                    anchor_id="anchor-v2-1",
                    anchor_store=store,
                    signing_key_id="anchor-signing-v1",
                    signing_key=private,
                )
            verified = verify_signed_anchor_receipt(
                signed,
                trusted_public_keys={"anchor-signing-v1": private.public_key()},
                signature_max_age=timedelta(seconds=5),
                expected_bundle_json=bundle,
            )
            self.assertEqual(verified.reason_codes, ())
            witness_a_root = temporary / "witness-a"
            witness_b_root = temporary / "witness-b"
            witness_a_root.mkdir()
            witness_b_root.mkdir()
            records = (
                CreateOnlyWitnessStore(witness_a_root, "witness-a").record(
                    signed,
                    trusted_public_keys={"anchor-signing-v1": private.public_key()},
                    signature_max_age=timedelta(seconds=5),
                ),
                CreateOnlyWitnessStore(witness_b_root, "witness-b").record(
                    signed,
                    trusted_public_keys={"anchor-signing-v1": private.public_key()},
                    signature_max_age=timedelta(seconds=5),
                ),
            )
            quorum = assess_witness_quorum(
                records,
                audit_head_digest=head,
                signed_receipt_sha256=hashlib.sha256(
                    signed.encode("utf-8")
                ).hexdigest(),
                minimum_witnesses=2,
            )
            self.assertTrue(quorum.satisfied)
            self.assertEqual(quorum.reason_codes, ())
            insufficient = assess_witness_quorum(
                records[:1],
                audit_head_digest=head,
                signed_receipt_sha256=hashlib.sha256(
                    signed.encode("utf-8")
                ).hexdigest(),
                minimum_witnesses=2,
            )
            self.assertFalse(insufficient.satisfied)
            self.assertEqual(
                insufficient.reason_codes,
                ("WITNESS_QUORUM_NOT_REACHED",),
            )

    def test_anchor_signer_runs_in_separate_process(self) -> None:
        bundle, _ = make_bundle()
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            private, private_path, _ = write_keys(temporary)
            trust_bundle, root_public, checkpoint_attestations = (
                write_trust_material(
                temporary,
                signer=private,
                key_id="anchor-signing-v1",
                role=KeyRole.ANCHOR_SIGNER,
                )
            )
            ledger_key = temporary / "ledger.key"
            ledger_key.write_bytes(b"R" * 32)
            ledger_key.chmod(0o600)
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "note.poc_horizontal_ai.trusted_runtime.ed25519_anchor_service",
                    "--anchor-database",
                    str(temporary / "anchor.sqlite3"),
                    "--anchor-id",
                    "anchor-service-v2-1",
                    "--ledger-key-file",
                    str(ledger_key),
                    "--signing-key-id",
                    "anchor-signing-v1",
                    "--signing-key-file",
                    str(private_path),
                    "--trust-bundle-file",
                    str(trust_bundle),
                    "--trust-checkpoint-database",
                    str(temporary / "anchor-trust.sqlite3"),
                    "--pinned-root-key-id",
                    "offline-root-v1",
                    "--pinned-root-public-key-file",
                    str(root_public),
                    "--trust-checkpoint-attestation-file",
                    str(checkpoint_attestations[0]),
                    "--trust-checkpoint-attestation-file",
                    str(checkpoint_attestations[1]),
                ],
                input=bundle,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(
                json.loads(completed.stdout)["schema_version"],
                "signed-payload/1.1",
            )
            verified = verify_signed_anchor_receipt(
                completed.stdout,
                trusted_public_keys={"anchor-signing-v1": private.public_key()},
                signature_max_age=timedelta(seconds=5),
                expected_bundle_json=bundle,
            )
            self.assertEqual(verified.reason_codes, ())


class DeploymentBoundaryTests(unittest.TestCase):
    def test_disjoint_paths_do_not_claim_os_identity_attestation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            private_path = temporary / "signing.pem"
            private_path.write_text("placeholder", encoding="utf-8")
            witness_a = temporary / "witness-a"
            witness_b = temporary / "witness-b"
            witness_a.mkdir()
            witness_b.mkdir()
            result = assess_runtime_placement(
                RuntimePlacement(
                    repository_root=Path.cwd(),
                    private_key_path=private_path,
                    nonce_database_path=temporary / "nonce.sqlite3",
                    anchor_database_path=temporary / "anchor.sqlite3",
                    witness_roots=(witness_a, witness_b),
                )
            )
            self.assertTrue(result.path_separated)
            self.assertFalse(result.os_identity_separation_verified)
            self.assertEqual(
                result.reason_codes,
                ("OS_IDENTITY_SEPARATION_NOT_ATTESTED",),
            )

    def test_repository_internal_secret_path_is_rejected(self) -> None:
        result = assess_runtime_placement(
            RuntimePlacement(
                repository_root=Path.cwd(),
                private_key_path=Path.cwd() / "secret.pem",
                nonce_database_path=Path.cwd() / "nonce.sqlite3",
                anchor_database_path=Path.cwd() / "anchor.sqlite3",
                witness_roots=(Path.cwd(), Path.cwd()),
            )
        )
        self.assertFalse(result.path_separated)
        self.assertIn("PLACEMENT_INSIDE_REPOSITORY", result.reason_codes)


if __name__ == "__main__":
    unittest.main()
