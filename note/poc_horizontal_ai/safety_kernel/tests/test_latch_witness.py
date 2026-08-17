import hashlib
import inspect
import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

from note.poc_horizontal_ai.safety_kernel import (
    AxisEvidence,
    ResponseIntegrityState,
    TargetBoundaryState,
    Thresholds,
)

from note.poc_horizontal_ai.trusted_runtime import (
    BoundaryExecutionIntent,
    ExecutionFileObservationRequest,
    ExternalLatchWitnessEvidence,
    KeyRole,
    LatchCheckpointWitnessStateStore,
    LatchCheckpointSignerProcess,
    LatchWitnessProcess,
    PersistentNonceStore,
    PinnedPolicyRoot,
    RootPolicyCheckpointStore,
    RootPolicyRotationEvidence,
    RootPolicyWitnessProcess,
    RootPolicyWitnessStateStore,
    RuntimePlacement,
    TrustedKeySpec,
    admit_boundary_runtime,
    assess_authority_manifest_quorum,
    assess_execution_file_observation_quorum,
    assess_execution_reality_quorum,
    assess_latch_witness_quorum,
    assess_root_policy_quorum,
    assess_root_policy_rotation_quorum,
    collect_root_policy_rotation_evidence,
    create_signed_latch_checkpoint,
    create_signed_latch_genesis,
    create_signed_execution_authorization,
    create_signed_execution_reality_observation,
    create_signed_authority_manifest_attestation,
    create_signed_policy_witness_deployment_attestation,
    create_signed_root_policy_endorsement,
    create_signed_root_policy_rotation_approval,
    root_policy_configuration_sha256,
    create_signed_trust_bundle,
    create_boundary_admission_challenge,
    create_checkpoint_attestation,
    encode_execution_file_observation_request,
    verify_signed_latch_checkpoint,
    verify_signed_trust_bundle,
    verify_latch_witness_attestation,
    launch_boundary_runtime,
    reconcile_execution_file_observations,
)
from note.poc_horizontal_ai.trusted_runtime.irreversible_latch_store import (
    IrreversibleLatchHead,
    PersistentIrreversibleLatchStore,
)


class RecordingExecutor:
    def __init__(self, *, result: bytes = b'{"executed":true}', error=None):
        self.result = result
        self.error = error
        self.calls = []

    def execute(self, action, *, attempt_id, intent):
        self.calls.append((action, attempt_id, intent))
        if self.error is not None:
            raise self.error
        return self.result


class LatchWitnessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime.now(timezone.utc)
        self.root = Ed25519PrivateKey.generate()
        self.checkpoint_signer = Ed25519PrivateKey.generate()
        self.witness_a1 = Ed25519PrivateKey.generate()
        self.witness_a2 = Ed25519PrivateKey.generate()
        self.witness_b = Ed25519PrivateKey.generate()
        self.execution_authorizer = Ed25519PrivateKey.generate()
        self.execution_authorizer_b = Ed25519PrivateKey.generate()
        self.execution_observer = Ed25519PrivateKey.generate()
        self.execution_observer_b = Ed25519PrivateKey.generate()
        self.authority_attester = Ed25519PrivateKey.generate()
        self.authority_attester_b = Ed25519PrivateKey.generate()
        self.policy_root = Ed25519PrivateKey.generate()
        self.policy_root_b = Ed25519PrivateKey.generate()
        self.pinned_policy_roots = {
            "policy-root-a": PinnedPolicyRoot(
                "policy-root-a",
                "policy-principal-a",
                self.policy_root.public_key(),
            ),
            "policy-root-b": PinnedPolicyRoot(
                "policy-root-b",
                "policy-principal-b",
                self.policy_root_b.public_key(),
            ),
        }
        self.signed_bundle = create_signed_trust_bundle(
            generation=1,
            keys=tuple(
                TrustedKeySpec(
                    key_id,
                    principal_id,
                    role,
                    private.public_key(),
                    self.now - timedelta(minutes=1),
                    self.now + timedelta(days=1),
                )
                for key_id, principal_id, role, private in (
                    (
                        "latch-checkpoint-v1",
                        "boundary-principal",
                        KeyRole.LATCH_CHECKPOINT_SIGNER,
                        self.checkpoint_signer,
                    ),
                    (
                        "witness-a1",
                        "principal-a",
                        KeyRole.WITNESS_SIGNER,
                        self.witness_a1,
                    ),
                    (
                        "witness-a2",
                        "principal-a",
                        KeyRole.WITNESS_SIGNER,
                        self.witness_a2,
                    ),
                    (
                        "witness-b",
                        "principal-b",
                        KeyRole.WITNESS_SIGNER,
                        self.witness_b,
                    ),
                    (
                        "execution-authorizer-v1",
                        "external-authority-a",
                        KeyRole.EXECUTION_AUTHORIZER,
                        self.execution_authorizer,
                    ),
                    (
                        "execution-authorizer-b-v1",
                        "external-authority-b",
                        KeyRole.EXECUTION_AUTHORIZER,
                        self.execution_authorizer_b,
                    ),
                    (
                        "execution-observer-v1",
                        "external-observer-a",
                        KeyRole.OBSERVER_SIGNER,
                        self.execution_observer,
                    ),
                    (
                        "execution-observer-b-v1",
                        "external-observer-b",
                        KeyRole.OBSERVER_SIGNER,
                        self.execution_observer_b,
                    ),
                    (
                        "authority-attester-v1",
                        "authority-auditor-a",
                        KeyRole.AUTHORITY_ATTESTER,
                        self.authority_attester,
                    ),
                    (
                        "authority-attester-b-v1",
                        "authority-auditor-b",
                        KeyRole.AUTHORITY_ATTESTER,
                        self.authority_attester_b,
                    ),
                )
            ),
            root_key_id="offline-root-v1",
            root_private_key=self.root,
            issued_at=self.now,
        )
        verification = verify_signed_trust_bundle(
            self.signed_bundle,
            pinned_root_keys={"offline-root-v1": self.root.public_key()},
            signature_max_age=timedelta(seconds=5),
            now=self.now,
        )
        assert verification.bundle is not None
        self.bundle = verification.bundle
        self.head_1 = IrreversibleLatchHead(1, None, "a" * 64)
        self.head_2 = IrreversibleLatchHead(2, "a" * 64, "b" * 64)

    def admit_runtime(self, **kwargs: object):
        placement = kwargs.get("placement")
        evidence = kwargs.get("external_witness_evidence")
        if (
            isinstance(placement, RuntimePlacement)
            and placement.execution_authorization_database_path is not None
            and isinstance(evidence, ExternalLatchWitnessEvidence)
        ):
            challenge = kwargs.get("admission_challenge")
            challenge_nonce = getattr(challenge, "nonce", None)
            if not isinstance(challenge_nonce, str):
                raise ValueError("admission challenge is required")
            kwargs["external_witness_evidence"] = replace(
                evidence,
                signed_authority_manifest_attestations=(
                    self.authority_attestations(placement)
                ),
                minimum_authority_attester_principals=2,
                signed_root_policy_endorsements=(
                    self.witnessed_root_policy_endorsements(
                        placement,
                        admission_challenge=challenge_nonce,
                    )
                ),
            )
        return admit_boundary_runtime(
            pinned_root_keys={"offline-root-v1": self.root.public_key()},
            trust_bundle_signature_max_age=timedelta(seconds=5),
            pinned_policy_roots=self.pinned_policy_roots,
            minimum_policy_root_principals=2,
            root_policy_signature_max_age=timedelta(seconds=5),
            **kwargs,
        )

    def root_policy_endorsements(
        self,
        admission_challenge: str = "c" * 64,
        configuration_sha256: str | None = None,
    ) -> tuple[str, ...]:
        configuration_digest = (
            configuration_sha256
            if configuration_sha256 is not None
            else root_policy_configuration_sha256(
                policy_id="execution-root-policy-v1",
                pinned_policy_roots=self.pinned_policy_roots,
                minimum_principals=2,
            )
        )
        return tuple(
            create_signed_root_policy_endorsement(
                policy_id="execution-root-policy-v1",
                policy_configuration_sha256=configuration_digest,
                endorsement_id=f"root-policy-endorsement-{suffix}",
                policy_root=self.pinned_policy_roots[key_id],
                private_key=private_key,
                trust_bundle=self.bundle,
                admission_challenge=admission_challenge,
                endorsed_at=self.now,
                valid_until=self.now + timedelta(minutes=5),
            )
            for suffix, key_id, private_key in (
                ("a", "policy-root-a", self.policy_root),
                ("b", "policy-root-b", self.policy_root_b),
            )
        )

    def witnessed_root_policy_endorsements(
        self,
        placement: RuntimePlacement,
        *,
        trust_bundle=None,
        admission_challenge: str = "c" * 64,
        configuration_sha256: str | None = None,
    ) -> tuple[str, ...]:
        checkpoint_path = placement.root_policy_checkpoint_database_path
        if checkpoint_path is None:
            raise ValueError("root policy checkpoint path is required")
        bundle = self.bundle if trust_bundle is None else trust_bundle
        configuration_digest = (
            configuration_sha256
            if configuration_sha256 is not None
            else root_policy_configuration_sha256(
                policy_id="execution-root-policy-v1",
                pinned_policy_roots=self.pinned_policy_roots,
                minimum_principals=2,
            )
        )
        endorsements = []
        for suffix, key_id, private_key in (
            ("a", "policy-root-a", self.policy_root),
            ("b", "policy-root-b", self.policy_root_b),
        ):
            with RootPolicyWitnessStateStore(
                checkpoint_path.parent / f"root-policy-witness-{suffix}.sqlite3",
                self.pinned_policy_roots[key_id],
            ) as store:
                endorsements.append(
                    store.endorse(
                        policy_id="execution-root-policy-v1",
                        policy_configuration_sha256=configuration_digest,
                        endorsement_id=(
                            f"root-policy-endorsement-{suffix}-g{bundle.generation}-"
                            f"{admission_challenge[:16]}"
                        ),
                        private_key=private_key,
                        trust_bundle=bundle,
                        admission_challenge=admission_challenge,
                        endorsed_at=self.now + timedelta(
                            seconds=bundle.generation - 1
                        ),
                        valid_until=self.now + timedelta(minutes=5),
                    )
                )
        return tuple(endorsements)

    def authority_attestations(
        self,
        placement: RuntimePlacement,
    ) -> tuple[str, ...]:
        return tuple(
            create_signed_authority_manifest_attestation(
                placement=placement,
                manifest_id="execution-authority-manifest-v1",
                attestation_id=f"authority-attestation-{suffix}",
                signing_key_id=key_id,
                signing_private_key=private_key,
                trust_bundle=self.bundle,
                attested_at=self.now,
                valid_until=self.now + timedelta(minutes=5),
            )
            for suffix, key_id, private_key in (
                ("a", "authority-attester-v1", self.authority_attester),
                (
                    "b",
                    "authority-attester-b-v1",
                    self.authority_attester_b,
                ),
            )
        )

    def policy_witness_deployment_attestations(
        self,
        processes: tuple[RootPolicyWitnessProcess, ...],
    ) -> tuple[str, ...]:
        return tuple(
            create_signed_policy_witness_deployment_attestation(
                processes=processes,
                manifest_id="policy-witness-deployment-v1",
                attestation_id=f"policy-witness-deployment-{suffix}",
                signing_key_id=key_id,
                signing_private_key=private_key,
                trust_bundle=self.bundle,
                attested_at=self.now,
                valid_until=self.now + timedelta(minutes=5),
            )
            for suffix, key_id, private_key in (
                ("a", "authority-attester-v1", self.authority_attester),
                ("b", "authority-attester-b-v1", self.authority_attester_b),
            )
        )

    def placement(self, directory: Path) -> RuntimePlacement:
        private_key = directory / "boundary-private.key"
        private_key.write_bytes(b"not-used-by-boundary-runtime")
        witness_a = directory / "checkpoint-a"
        witness_b = directory / "checkpoint-b"
        witness_a.mkdir()
        witness_b.mkdir()
        return RuntimePlacement(
            repository_root=Path.cwd(),
            private_key_path=private_key,
            nonce_database_path=directory / "nonce.sqlite3",
            anchor_database_path=directory / "anchor.sqlite3",
            latch_database_path=directory / "latch.sqlite3",
            witness_roots=(witness_a, witness_b),
            execution_authorization_database_path=(
                directory / "execution-authorizations.sqlite3"
            ),
            execution_journal_authority_domain="journal-custodian",
            execution_integrity_key_authority_domain="key-custodian",
            observer_trust_root_authority_domains=(
                "observer-root-custodian-a",
                "observer-root-custodian-b",
            ),
            root_policy_checkpoint_database_path=(
                directory / "root-policy-checkpoint.sqlite3"
            ),
        )

    def launcher_material(
        self,
        directory: Path,
    ) -> tuple[
        LatchCheckpointSignerProcess,
        Path,
        tuple[LatchWitnessProcess, ...],
    ]:
        root_public = directory / "root-public.pem"
        signer_private = directory / "checkpoint-signer-private.pem"
        trust_bundle_path = directory / "trust-bundle.json"
        latch_integrity_key_path = directory / "latch-integrity.key"
        witness_a_private = directory / "witness-a-private.pem"
        witness_b_private = directory / "witness-b-private.pem"
        root_public.write_bytes(
            self.root.public_key().public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )
        signer_private.write_bytes(
            self.checkpoint_signer.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.PKCS8,
                serialization.NoEncryption(),
            )
        )
        trust_bundle_path.write_text(self.signed_bundle, encoding="utf-8")
        latch_integrity_key_path.write_bytes(b"L" * 32)
        for path, private_key in (
            (witness_a_private, self.witness_a1),
            (witness_b_private, self.witness_b),
        ):
            path.write_bytes(
                private_key.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.PKCS8,
                    serialization.NoEncryption(),
                )
            )
        trust_attestation_paths = []
        for principal_id, key_id, private_key in (
            ("principal-a", "witness-a1", self.witness_a1),
            ("principal-b", "witness-b", self.witness_b),
        ):
            attestation_path = directory / f"trust-{principal_id}.json"
            attestation_path.write_text(
                create_checkpoint_attestation(
                    trust_bundle=self.bundle,
                    attestation_id=f"trust-{principal_id}-1",
                    witness_principal_id=principal_id,
                    witness_sequence=1,
                    witness_key_id=key_id,
                    witness_private_key=private_key,
                    witnessed_at=self.now,
                ),
                encoding="utf-8",
            )
            trust_attestation_paths.append(attestation_path)
        signer_process = LatchCheckpointSignerProcess(
            latch_integrity_key_path=latch_integrity_key_path,
            signing_key_id="latch-checkpoint-v1",
            signing_key_path=signer_private,
            trust_bundle_path=trust_bundle_path,
            trust_checkpoint_database_path=(
                directory / "signer-trust-checkpoint.sqlite3"
            ),
            trust_checkpoint_attestation_paths=tuple(trust_attestation_paths),
        )
        processes = (
            LatchWitnessProcess(
                directory / "launcher-witness-a.sqlite3",
                "principal-a",
                "witness-a1",
                witness_a_private,
            ),
            LatchWitnessProcess(
                directory / "launcher-witness-b.sqlite3",
                "principal-b",
                "witness-b",
                witness_b_private,
            ),
        )
        return signer_process, root_public, processes

    def launch(
        self,
        placement: RuntimePlacement,
        signer_process: LatchCheckpointSignerProcess,
        root_public: Path,
        processes: tuple[LatchWitnessProcess, ...],
        execution_executor=None,
        hard_invariant_checker=None,
        policy_process_limit: int | None = None,
        policy_process_host_override: str | None = None,
        policy_process_authority_overlap: bool = False,
    ):
        policy_processes = []
        checkpoint_path = placement.root_policy_checkpoint_database_path
        if checkpoint_path is None:
            raise ValueError("root policy checkpoint path is required")
        for suffix, key_id, private_key in (
            ("a", "policy-root-a", self.policy_root),
            ("b", "policy-root-b", self.policy_root_b),
        ):
            private_path = checkpoint_path.parent / f"policy-root-{suffix}.pem"
            if not private_path.exists():
                private_path.write_bytes(
                    private_key.private_bytes(
                        serialization.Encoding.PEM,
                        serialization.PrivateFormat.PKCS8,
                        serialization.NoEncryption(),
                    )
                )
            policy_processes.append(
                RootPolicyWitnessProcess(
                    checkpoint_path.parent
                    / f"root-policy-witness-{suffix}.sqlite3",
                    self.pinned_policy_roots[key_id].principal_id,
                    key_id,
                    private_path,
                    f"policy-host-{suffix}",
                    f"policy-os-identity-{suffix}",
                    f"policy-key-custodian-{suffix}",
                    f"policy-state-custodian-{suffix}",
                )
            )
        deployment_attestations = self.policy_witness_deployment_attestations(
            tuple(policy_processes)
        )
        if policy_process_host_override is not None:
            policy_processes[0] = replace(
                policy_processes[0],
                host_identity=policy_process_host_override,
            )
        if policy_process_authority_overlap:
            policy_processes[0] = replace(
                policy_processes[0],
                key_authority_domain="journal-custodian",
            )
        if policy_process_limit is not None:
            policy_processes = policy_processes[:policy_process_limit]
        return launch_boundary_runtime(
            placement=placement,
            latch_integrity_key=b"L" * 32,
            latch_store_id="repo-latch-v1",
            checkpoint_signer_process=signer_process,
            pinned_root_key_id="offline-root-v1",
            pinned_root_public_key_path=root_public,
            witness_processes=processes,
            minimum_witness_principals=2,
            minimum_trust_checkpoint_witness_principals=2,
            minimum_execution_authorizer_principals=2,
            signed_authority_manifest_attestations=(
                self.authority_attestations(placement)
            ),
            minimum_authority_attester_principals=2,
            pinned_policy_roots=self.pinned_policy_roots,
            root_policy_id="execution-root-policy-v1",
            root_policy_witness_processes=tuple(policy_processes),
            signed_policy_witness_deployment_attestations=(
                deployment_attestations
            ),
            minimum_policy_witness_deployment_attester_principals=2,
            policy_witness_deployment_signature_max_age=timedelta(minutes=5),
            minimum_policy_root_principals=2,
            root_policy_signature_max_age=timedelta(minutes=5),
            trust_bundle_max_age=timedelta(minutes=5),
            trust_checkpoint_attestation_max_age=timedelta(minutes=5),
            checkpoint_signature_max_age=timedelta(minutes=5),
            checkpoint_signer_process_timeout=timedelta(seconds=10),
            witness_process_timeout=timedelta(seconds=10),
            root_policy_witness_process_timeout=timedelta(seconds=10),
            execution_executor=execution_executor,
            hard_invariant_checker=hard_invariant_checker,
            now=self.now,
        )

    def checkpoint(
        self,
        head: IrreversibleLatchHead,
        checkpoint_id: str,
    ) -> str:
        return create_signed_latch_checkpoint(
            head,
            checkpoint_id=checkpoint_id,
            latch_store_id="repo-latch-v1",
            signing_key_id="latch-checkpoint-v1",
            signing_private_key=self.checkpoint_signer,
            trust_bundle=self.bundle,
            checkpointed_at=self.now,
        )

    def authorize_execution(
        self,
        intent: BoundaryExecutionIntent,
        *,
        authorization_id: str,
        authorization_nonce: str,
        expected_latch_head: IrreversibleLatchHead | None,
    ) -> tuple[str, ...]:
        return tuple(
            create_signed_execution_authorization(
                intent,
                authorization_id=authorization_id,
                authorization_nonce=authorization_nonce,
                latch_store_id="repo-latch-v1",
                expected_latch_head=expected_latch_head,
                signing_key_id=key_id,
                signing_private_key=private_key,
                trust_bundle=self.bundle,
                authorized_at=self.now,
                valid_until=self.now + timedelta(minutes=1),
            )
            for key_id, private_key in (
                ("execution-authorizer-v1", self.execution_authorizer),
                ("execution-authorizer-b-v1", self.execution_authorizer_b),
            )
        )

    def attest(
        self,
        database: Path,
        principal_id: str,
        key_id: str,
        private: Ed25519PrivateKey,
        signed_checkpoints: tuple[str, ...],
        admission_challenge: str | None = None,
    ) -> str:
        with LatchCheckpointWitnessStateStore(
            database,
            principal_id,
            "repo-latch-v1",
        ) as store:
            return store.attest(
                signed_checkpoints,
                trust_bundle=self.bundle,
                checkpoint_signature_max_age=timedelta(seconds=5),
                witness_key_id=key_id,
                witness_private_key=private,
                witnessed_at=self.now,
                admission_challenge=admission_challenge,
            )

    def test_quorum_counts_distinct_witness_principals(self) -> None:
        checkpoint = self.checkpoint(self.head_1, "checkpoint-1")
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            attestation_a1 = self.attest(
                temporary / "a1.sqlite3",
                "principal-a",
                "witness-a1",
                self.witness_a1,
                (checkpoint,),
            )
            attestation_a2 = self.attest(
                temporary / "a2.sqlite3",
                "principal-a",
                "witness-a2",
                self.witness_a2,
                (checkpoint,),
            )
            attestation_b = self.attest(
                temporary / "b.sqlite3",
                "principal-b",
                "witness-b",
                self.witness_b,
                (checkpoint,),
            )
        one_principal = assess_latch_witness_quorum(
            (attestation_a1, attestation_a2),
            signed_latch_checkpoint_json=checkpoint,
            trust_bundle=self.bundle,
            minimum_principals=2,
            signature_max_age=timedelta(seconds=5),
            now=self.now,
        )
        self.assertFalse(one_principal.satisfied)
        self.assertEqual(one_principal.principal_ids, ("principal-a",))
        two_principals = assess_latch_witness_quorum(
            (attestation_a1, attestation_a2, attestation_b),
            signed_latch_checkpoint_json=checkpoint,
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

    def test_witness_store_rejects_rollback_and_generation_gap(self) -> None:
        checkpoint_1 = self.checkpoint(self.head_1, "checkpoint-1")
        checkpoint_2 = self.checkpoint(self.head_2, "checkpoint-2")
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            with LatchCheckpointWitnessStateStore(
                temporary / "witness.sqlite3",
                "principal-a",
                "repo-latch-v1",
            ) as store:
                common = {
                    "trust_bundle": self.bundle,
                    "checkpoint_signature_max_age": timedelta(seconds=5),
                    "witness_key_id": "witness-a1",
                    "witness_private_key": self.witness_a1,
                    "witnessed_at": self.now,
                }
                store.attest((checkpoint_1,), **common)
                store.attest((checkpoint_2,), **common)
                with self.assertRaisesRegex(ValueError, "LATCH_WITNESS_ROLLBACK"):
                    store.attest((checkpoint_1,), **common)

            with LatchCheckpointWitnessStateStore(
                temporary / "gap.sqlite3",
                "principal-a",
                "repo-latch-v1",
            ) as gap_store:
                with self.assertRaisesRegex(
                    ValueError,
                    "LATCH_WITNESS_CHAIN_INVALID",
                ):
                    gap_store.attest((checkpoint_2,), **common)

    def test_witness_store_requires_canonical_checkpoint_order(self) -> None:
        checkpoint_1 = self.checkpoint(self.head_1, "checkpoint-1")
        checkpoint_2 = self.checkpoint(self.head_2, "checkpoint-2")
        with tempfile.TemporaryDirectory() as directory:
            with LatchCheckpointWitnessStateStore(
                Path(directory) / "witness.sqlite3",
                "principal-a",
                "repo-latch-v1",
            ) as store:
                common = {
                    "trust_bundle": self.bundle,
                    "checkpoint_signature_max_age": timedelta(seconds=5),
                    "witness_key_id": "witness-a1",
                    "witness_private_key": self.witness_a1,
                    "witnessed_at": self.now,
                }
                store.attest((checkpoint_1,), **common)
                store.attest((checkpoint_2,), **common)
                invalid_segments = (
                    (checkpoint_2, checkpoint_1, checkpoint_2),
                    (checkpoint_1, checkpoint_1, checkpoint_2),
                )
                for segment in invalid_segments:
                    with self.subTest(segment=segment):
                        with self.assertRaisesRegex(
                            ValueError,
                            "LATCH_WITNESS_CHAIN_INVALID",
                        ):
                            store.attest(segment, **common)

                signed = store.attest(
                    (checkpoint_1, checkpoint_2),
                    **common,
                )
                verified, reasons = verify_latch_witness_attestation(
                    signed,
                    trust_bundle=self.bundle,
                    signature_max_age=timedelta(seconds=5),
                    now=self.now,
                )
                self.assertEqual(reasons, ())
                self.assertIsNotNone(verified)
                assert verified is not None
                self.assertEqual(verified.witness_sequence, 3)

    def test_genesis_cannot_be_reissued_after_nonempty_head(self) -> None:
        genesis = create_signed_latch_genesis(
            checkpoint_id="genesis",
            latch_store_id="repo-latch-v1",
            signing_key_id="latch-checkpoint-v1",
            signing_private_key=self.checkpoint_signer,
            trust_bundle=self.bundle,
            checkpointed_at=self.now,
        )
        checkpoint_1 = self.checkpoint(self.head_1, "checkpoint-1")
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "witness.sqlite3"
            self.attest(
                database,
                "principal-a",
                "witness-a1",
                self.witness_a1,
                (genesis,),
                create_boundary_admission_challenge().nonce,
            )
            self.attest(
                database,
                "principal-a",
                "witness-a1",
                self.witness_a1,
                (checkpoint_1,),
                create_boundary_admission_challenge().nonce,
            )
            with self.assertRaisesRegex(ValueError, "LATCH_WITNESS_ROLLBACK"):
                self.attest(
                    database,
                    "principal-a",
                    "witness-a1",
                    self.witness_a1,
                    (genesis,),
                    create_boundary_admission_challenge().nonce,
                )

    def test_checkpoint_signer_role_is_not_interchangeable(self) -> None:
        with self.assertRaisesRegex(ValueError, "LATCH_SIGNING_ROLE_MISMATCH"):
            create_signed_latch_checkpoint(
                self.head_1,
                checkpoint_id="wrong-role",
                latch_store_id="repo-latch-v1",
                signing_key_id="witness-a1",
                signing_private_key=self.witness_a1,
                trust_bundle=self.bundle,
                checkpointed_at=self.now,
            )
        with self.assertRaisesRegex(
            ValueError,
            "EXECUTION_AUTHORIZER_ROLE_OR_KEY_MISMATCH",
        ):
            create_signed_execution_authorization(
                BoundaryExecutionIntent(
                    "intent-role",
                    "repo-1",
                    "a" * 64,
                    "deployment.json",
                    "deployment_state",
                    "ready",
                ),
                authorization_id="authorization-role",
                authorization_nonce="authorization-nonce-role",
                latch_store_id="repo-latch-v1",
                expected_latch_head=None,
                signing_key_id="latch-checkpoint-v1",
                signing_private_key=self.checkpoint_signer,
                trust_bundle=self.bundle,
                authorized_at=self.now,
                valid_until=self.now + timedelta(minutes=1),
            )

    def test_execution_reality_observation_hides_expectation_and_needs_quorum(
        self,
    ) -> None:
        attempt_id = "d" * 64
        required_value = "required-secret-ready"
        self.assertNotIn(
            "required_postcondition_value",
            inspect.signature(
                create_signed_execution_reality_observation
            ).parameters,
        )

        def observe(
            observation_id: str,
            key_id: str,
            private_key: Ed25519PrivateKey,
            observed_value: str = "actual-ready",
        ) -> str:
            return create_signed_execution_reality_observation(
                observation_id=observation_id,
                attempt_id=attempt_id,
                intent_id="intent-observed",
                target_id="repo-1",
                observation_subject="deployment.json",
                observation_field="deployment_state",
                observed_value=observed_value,
                signing_key_id=key_id,
                signing_private_key=private_key,
                trust_bundle=self.bundle,
                observed_at=self.now,
            )

        observation_a = observe(
            "observation-a",
            "execution-observer-v1",
            self.execution_observer,
        )
        observation_b = observe(
            "observation-b",
            "execution-observer-b-v1",
            self.execution_observer_b,
        )
        self.assertNotIn(required_value, observation_a)
        quorum, reasons = assess_execution_reality_quorum(
            (observation_a, observation_b),
            trust_bundle=self.bundle,
            minimum_principals=2,
            signature_max_age=timedelta(minutes=1),
            observation_max_age=timedelta(minutes=1),
            now=self.now,
        )
        self.assertEqual(reasons, ())
        assert quorum is not None
        self.assertEqual(quorum.attempt_id, attempt_id)
        self.assertEqual(quorum.observation_field, "deployment_state")
        self.assertEqual(quorum.observed_value, "actual-ready")
        self.assertEqual(
            quorum.principal_ids,
            ("external-observer-a", "external-observer-b"),
        )

        duplicate, duplicate_reasons = assess_execution_reality_quorum(
            (observation_a, observation_a),
            trust_bundle=self.bundle,
            minimum_principals=2,
            signature_max_age=timedelta(minutes=1),
            observation_max_age=timedelta(minutes=1),
            now=self.now,
        )
        self.assertIsNone(duplicate)
        self.assertEqual(
            duplicate_reasons,
            ("EXECUTION_OBSERVATION_QUORUM_NOT_REACHED",),
        )

        conflict_b = observe(
            "observation-conflict-b",
            "execution-observer-b-v1",
            self.execution_observer_b,
            "actual-not-ready",
        )
        conflict, conflict_reasons = assess_execution_reality_quorum(
            (observation_a, conflict_b),
            trust_bundle=self.bundle,
            minimum_principals=2,
            signature_max_age=timedelta(minutes=1),
            observation_max_age=timedelta(minutes=1),
            now=self.now,
        )
        self.assertIsNone(conflict)
        self.assertEqual(
            conflict_reasons,
            ("EXECUTION_OBSERVATION_QUORUM_CONFLICT",),
        )

        with self.assertRaisesRegex(
            ValueError,
            "EXECUTION_OBSERVER_ROLE_OR_KEY_MISMATCH",
        ):
            observe(
                "observation-wrong-role",
                "execution-authorizer-v1",
                self.execution_authorizer,
            )

        tampered = observation_a.replace("actual-ready", "actual-false")
        rejected, rejected_reasons = assess_execution_reality_quorum(
            (tampered, observation_b),
            trust_bundle=self.bundle,
            minimum_principals=2,
            signature_max_age=timedelta(minutes=1),
            observation_max_age=timedelta(minutes=1),
            now=self.now,
        )
        self.assertIsNone(rejected)
        self.assertIn("SIGNATURE_PAYLOAD_DIGEST_MISMATCH", rejected_reasons)

    def test_execution_file_observer_measures_in_separate_process(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            repository = temporary / "repository"
            repository.mkdir()
            observed_file = repository / "observed.txt"
            observed_file.write_bytes(b"measured-by-observer")
            root_public = temporary / "root-public.pem"
            observer_private_a = temporary / "observer-a-private.pem"
            observer_private_b = temporary / "observer-b-private.pem"
            bundle_file = temporary / "trust-bundle.json"
            ledger_key_a = temporary / "observer-a-ledger.key"
            ledger_key_b = temporary / "observer-b-ledger.key"
            root_public.write_bytes(
                self.root.public_key().public_bytes(
                    serialization.Encoding.PEM,
                    serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )
            observer_private_a.write_bytes(
                self.execution_observer.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.PKCS8,
                    serialization.NoEncryption(),
                )
            )
            observer_private_b.write_bytes(
                self.execution_observer_b.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.PKCS8,
                    serialization.NoEncryption(),
                )
            )
            bundle_file.write_text(self.signed_bundle, encoding="utf-8")
            ledger_key_a.write_bytes(b"O" * 32)
            ledger_key_b.write_bytes(b"P" * 32)
            attestation_paths = []
            for principal_id, key_id, private_key in (
                ("principal-a", "witness-a1", self.witness_a1),
                ("principal-b", "witness-b", self.witness_b),
            ):
                path = temporary / f"trust-{principal_id}.json"
                path.write_text(
                    create_checkpoint_attestation(
                        trust_bundle=self.bundle,
                        attestation_id=f"file-observer-{principal_id}",
                        witness_principal_id=principal_id,
                        witness_sequence=1,
                        witness_key_id=key_id,
                        witness_private_key=private_key,
                        witnessed_at=self.now,
                    ),
                    encoding="utf-8",
                )
                attestation_paths.append(path)
            def request_for(suffix: str, nonce: str) -> ExecutionFileObservationRequest:
                return ExecutionFileObservationRequest(
                    observation_id=f"file-observation-{suffix}",
                    request_id=f"file-observation-request-{suffix}",
                    nonce=nonce,
                    attempt_id="e" * 64,
                    intent_id="intent-file-observation",
                    target_id="repo-1",
                    observation_subject="observed.txt",
                    observation_field="current_sha256",
                    state_version=1,
                    issued_at=self.now,
                )

            def command_for(
                suffix: str,
                key_id: str,
                private_path: Path,
                ledger_path: Path,
            ) -> list[str]:
                command = [
                    sys.executable,
                    "-m",
                    "note.poc_horizontal_ai.trusted_runtime.execution_file_observer_service",
                    "--repository-root",
                    str(repository),
                    "--observer-id",
                    f"execution-file-observer-{suffix}",
                    "--nonce-database",
                    str(temporary / f"observer-{suffix}-nonce.sqlite3"),
                    "--ledger-key-file",
                    str(ledger_path),
                    "--signing-key-id",
                    key_id,
                    "--signing-key-file",
                    str(private_path),
                    "--trust-bundle-file",
                    str(bundle_file),
                    "--trust-checkpoint-database",
                    str(temporary / f"observer-{suffix}-trust.sqlite3"),
                    "--pinned-root-key-id",
                    "offline-root-v1",
                    "--pinned-root-public-key-file",
                    str(root_public),
                ]
                for path in attestation_paths:
                    command.extend(
                        ["--trust-checkpoint-attestation-file", str(path)]
                    )
                return command

            request_a = request_for("a", "file-observation-nonce-0001-a")
            request_b = request_for("b", "file-observation-nonce-0001-b")
            request_json_a = encode_execution_file_observation_request(request_a)
            request_json_b = encode_execution_file_observation_request(request_b)
            self.assertNotIn("required_postcondition_value", request_json_a)
            command_a = command_for(
                "a",
                "execution-observer-v1",
                observer_private_a,
                ledger_key_a,
            )
            command_b = command_for(
                "b",
                "execution-observer-b-v1",
                observer_private_b,
                ledger_key_b,
            )
            completed_a = subprocess.run(
                command_a,
                input=request_json_a,
                text=True,
                capture_output=True,
                check=False,
            )
            completed_b = subprocess.run(
                command_b,
                input=request_json_b,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed_a.returncode, 0, completed_a.stdout)
            self.assertEqual(completed_b.returncode, 0, completed_b.stdout)
            quorum, reasons = assess_execution_file_observation_quorum(
                (
                    (request_a, completed_a.stdout),
                    (request_b, completed_b.stdout),
                ),
                trust_bundle=self.bundle,
                minimum_principals=2,
                signature_max_age=timedelta(minutes=1),
                observation_max_age=timedelta(minutes=1),
                now=datetime.now(timezone.utc),
            )
            self.assertEqual(reasons, ())
            assert quorum is not None
            self.assertEqual(
                quorum.observed_value,
                hashlib.sha256(observed_file.read_bytes()).hexdigest(),
            )
            self.assertEqual(
                quorum.principal_ids,
                ("external-observer-a", "external-observer-b"),
            )
            wrong_request, wrong_request_reasons = (
                assess_execution_file_observation_quorum(
                    (
                        (request_a, completed_a.stdout),
                        (request_a, completed_b.stdout),
                    ),
                    trust_bundle=self.bundle,
                    minimum_principals=2,
                    signature_max_age=timedelta(minutes=1),
                    observation_max_age=timedelta(minutes=1),
                    now=datetime.now(timezone.utc),
                )
            )
            self.assertIsNone(wrong_request)
            self.assertIn(
                "EXECUTION_OBSERVATION_ID_MISMATCH",
                wrong_request_reasons,
            )

            observed_file.write_bytes(b"changed-between-observers")
            request_b_conflict = request_for(
                "b-conflict",
                "file-observation-nonce-conflict-b",
            )
            completed_b_conflict = subprocess.run(
                command_b,
                input=encode_execution_file_observation_request(
                    request_b_conflict
                ),
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(
                completed_b_conflict.returncode,
                0,
                completed_b_conflict.stdout,
            )
            conflict, conflict_reasons = (
                assess_execution_file_observation_quorum(
                    (
                        (request_a, completed_a.stdout),
                        (request_b_conflict, completed_b_conflict.stdout),
                    ),
                    trust_bundle=self.bundle,
                    minimum_principals=2,
                    signature_max_age=timedelta(minutes=1),
                    observation_max_age=timedelta(minutes=1),
                    now=datetime.now(timezone.utc),
                )
            )
            self.assertIsNone(conflict)
            self.assertEqual(
                conflict_reasons,
                ("EXECUTION_OBSERVATION_QUORUM_CONFLICT",),
            )
            replayed = subprocess.run(
                command_a,
                input=request_json_a,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(replayed.returncode, 2)
            invalid_subject = ExecutionFileObservationRequest(
                observation_id="file-observation-invalid",
                request_id="file-observation-request-invalid",
                nonce="file-observation-nonce-invalid",
                attempt_id="f" * 64,
                intent_id="intent-file-observation",
                target_id="repo-1",
                observation_subject="../outside.txt",
                observation_field="current_sha256",
                state_version=1,
                issued_at=self.now,
            )
            with self.assertRaises(ValueError):
                encode_execution_file_observation_request(invalid_subject)

    def test_execution_reconciliation_is_persistent_and_fail_closed(self) -> None:
        required_value = hashlib.sha256(b"required-file-state").hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            with PersistentNonceStore(
                Path(directory) / "execution-journal.sqlite3",
                b"R" * 32,
            ) as journal:
                def prepare(suffix: str) -> str:
                    prepared = journal.consume_and_prepare_execution(
                        request_id=f"authorization:{suffix}",
                        nonce=f"authorization-nonce-{suffix}-0001",
                        issued_at=self.now,
                        request_digest=hashlib.sha256(
                            f"authorization-{suffix}".encode("utf-8")
                        ).hexdigest(),
                        consumed_at=self.now,
                        intent_id=f"intent-{suffix}",
                        target_id="repo-1",
                        action_digest=hashlib.sha256(
                            f"action-{suffix}".encode("utf-8")
                        ).hexdigest(),
                        postcondition_subject="observed.txt",
                        postcondition_field="current_sha256",
                        required_postcondition_value=required_value,
                        authorizer_principal_ids=(
                            "external-authority-a",
                            "external-authority-b",
                        ),
                    )
                    self.assertTrue(prepared.accepted, prepared.reason_codes)
                    assert prepared.attempt_id is not None
                    self.assertTrue(
                        journal.record_execution_event(
                            attempt_id=prepared.attempt_id,
                            state="STARTED",
                            observed_at=self.now,
                        ).accepted
                    )
                    self.assertTrue(
                        journal.record_execution_event(
                            attempt_id=prepared.attempt_id,
                            state="EXECUTOR_RETURNED",
                            observed_at=self.now,
                            result_digest=hashlib.sha256(b"result").hexdigest(),
                        ).accepted
                    )
                    return prepared.attempt_id

                def evidence(
                    attempt_id: str,
                    suffix: str,
                    value_a: str = required_value,
                    value_b: str = required_value,
                ) -> tuple[tuple[ExecutionFileObservationRequest, str], ...]:
                    items = []
                    for observer_suffix, key_id, key, value in (
                        (
                            "a",
                            "execution-observer-v1",
                            self.execution_observer,
                            value_a,
                        ),
                        (
                            "b",
                            "execution-observer-b-v1",
                            self.execution_observer_b,
                            value_b,
                        ),
                    ):
                        request = ExecutionFileObservationRequest(
                            observation_id=(
                                f"reconcile-observation-{suffix}-{observer_suffix}"
                            ),
                            request_id=(
                                f"reconcile-request-{suffix}-{observer_suffix}"
                            ),
                            nonce=(
                                f"reconcile-nonce-{suffix}-{observer_suffix}-0001"
                            ),
                            attempt_id=attempt_id,
                            intent_id=f"intent-{suffix}",
                            target_id="repo-1",
                            observation_subject="observed.txt",
                            observation_field="current_sha256",
                            state_version=1,
                            issued_at=self.now,
                        )
                        signed = create_signed_execution_reality_observation(
                            observation_id=request.observation_id,
                            attempt_id=request.attempt_id,
                            intent_id=request.intent_id,
                            target_id=request.target_id,
                            observation_subject=request.observation_subject,
                            observation_field=request.observation_field,
                            observed_value=value,
                            signing_key_id=key_id,
                            signing_private_key=key,
                            trust_bundle=self.bundle,
                            observed_at=self.now,
                        )
                        items.append((request, signed))
                    return tuple(items)

                resolved_attempt = prepare("resolved")
                resolved_evidence = evidence(resolved_attempt, "resolved")
                invalid_policy = reconcile_execution_file_observations(
                    journal=journal,
                    attempt_id=resolved_attempt,
                    requested_observations=resolved_evidence,
                    trust_bundle=self.bundle,
                    minimum_principals=1,
                    signature_max_age=timedelta(minutes=1),
                    observation_max_age=timedelta(minutes=1),
                    now=self.now,
                )
                self.assertFalse(invalid_policy.accepted)
                self.assertEqual(
                    invalid_policy.reason_codes,
                    ("EXECUTION_RECONCILIATION_EVIDENCE_INVALID",),
                )
                self.assertEqual(
                    journal.unresolved_execution_attempt_ids(),
                    (resolved_attempt,),
                )
                resolved = reconcile_execution_file_observations(
                    journal=journal,
                    attempt_id=resolved_attempt,
                    requested_observations=resolved_evidence,
                    trust_bundle=self.bundle,
                    minimum_principals=2,
                    signature_max_age=timedelta(minutes=1),
                    observation_max_age=timedelta(minutes=1),
                    now=self.now,
                )
                self.assertTrue(resolved.accepted, resolved.reason_codes)
                self.assertEqual(resolved.outcome, "VERIFIED_RESOLVED")
                self.assertEqual(journal.unresolved_execution_attempt_ids(), ())
                terminal = reconcile_execution_file_observations(
                    journal=journal,
                    attempt_id=resolved_attempt,
                    requested_observations=resolved_evidence,
                    trust_bundle=self.bundle,
                    minimum_principals=2,
                    signature_max_age=timedelta(minutes=1),
                    observation_max_age=timedelta(minutes=1),
                    now=self.now,
                )
                self.assertFalse(terminal.accepted)
                self.assertEqual(
                    terminal.reason_codes,
                    ("EXECUTION_RECONCILIATION_TERMINAL",),
                )

                retry_attempt = prepare("retry")
                retry_evidence = evidence(retry_attempt, "retry")
                insufficient = reconcile_execution_file_observations(
                    journal=journal,
                    attempt_id=retry_attempt,
                    requested_observations=retry_evidence[:1],
                    trust_bundle=self.bundle,
                    minimum_principals=2,
                    signature_max_age=timedelta(minutes=1),
                    observation_max_age=timedelta(minutes=1),
                    now=self.now,
                )
                self.assertEqual(insufficient.outcome, "EVIDENCE_INSUFFICIENT")
                self.assertEqual(
                    journal.unresolved_execution_attempt_ids(),
                    (retry_attempt,),
                )
                retried = reconcile_execution_file_observations(
                    journal=journal,
                    attempt_id=retry_attempt,
                    requested_observations=retry_evidence,
                    trust_bundle=self.bundle,
                    minimum_principals=2,
                    signature_max_age=timedelta(minutes=1),
                    observation_max_age=timedelta(minutes=1),
                    now=self.now,
                )
                self.assertEqual(retried.outcome, "VERIFIED_RESOLVED")

                conflict_attempt = prepare("conflict")
                wrong_attempt_evidence = evidence(
                    "f" * 64,
                    "conflict",
                )
                wrong_attempt = reconcile_execution_file_observations(
                    journal=journal,
                    attempt_id=conflict_attempt,
                    requested_observations=wrong_attempt_evidence,
                    trust_bundle=self.bundle,
                    minimum_principals=2,
                    signature_max_age=timedelta(minutes=1),
                    observation_max_age=timedelta(minutes=1),
                    now=self.now,
                )
                self.assertFalse(wrong_attempt.accepted)
                self.assertEqual(
                    wrong_attempt.reason_codes,
                    ("EXECUTION_RECONCILIATION_ATTEMPT_MISMATCH",),
                )
                conflicting = reconcile_execution_file_observations(
                    journal=journal,
                    attempt_id=conflict_attempt,
                    requested_observations=evidence(
                        conflict_attempt,
                        "conflict",
                        value_b=hashlib.sha256(b"other-state").hexdigest(),
                    ),
                    trust_bundle=self.bundle,
                    minimum_principals=2,
                    signature_max_age=timedelta(minutes=1),
                    observation_max_age=timedelta(minutes=1),
                    now=self.now,
                )
                self.assertEqual(conflicting.outcome, "CONFLICT")
                self.assertEqual(
                    journal.unresolved_execution_attempt_ids(),
                    (conflict_attempt,),
                )
                self.assertEqual(journal.verify(), ())

    def test_authority_manifest_requires_distinct_matching_principals(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            placement = self.placement(Path(directory))
            attestations = self.authority_attestations(placement)
            accepted = assess_authority_manifest_quorum(
                attestations,
                placement=placement,
                trust_bundle=self.bundle,
                minimum_principals=2,
                signature_max_age=timedelta(minutes=1),
                now=self.now,
            )
            self.assertTrue(accepted.satisfied, accepted.reason_codes)
            self.assertEqual(
                accepted.principal_ids,
                ("authority-auditor-a", "authority-auditor-b"),
            )
            duplicate = assess_authority_manifest_quorum(
                (attestations[0], attestations[0]),
                placement=placement,
                trust_bundle=self.bundle,
                minimum_principals=2,
                signature_max_age=timedelta(minutes=1),
                now=self.now,
            )
            self.assertFalse(duplicate.satisfied)
            self.assertEqual(
                duplicate.reason_codes,
                ("AUTHORITY_MANIFEST_QUORUM_NOT_REACHED",),
            )
            changed = replace(
                placement,
                execution_integrity_key_authority_domain=(
                    "different-key-custodian"
                ),
            )
            mismatch = assess_authority_manifest_quorum(
                attestations,
                placement=changed,
                trust_bundle=self.bundle,
                minimum_principals=2,
                signature_max_age=timedelta(minutes=1),
                now=self.now,
            )
            self.assertFalse(mismatch.satisfied)
            self.assertIn(
                "AUTHORITY_MANIFEST_PLACEMENT_MISMATCH",
                mismatch.reason_codes,
            )

    def test_root_policy_requires_independent_threshold_endorsement(self) -> None:
        endorsements = self.root_policy_endorsements()
        accepted = assess_root_policy_quorum(
            endorsements,
            pinned_policy_roots=self.pinned_policy_roots,
            primary_root_keys={"offline-root-v1": self.root.public_key()},
            trust_bundle=self.bundle,
            admission_challenge="c" * 64,
            minimum_principals=2,
            signature_max_age=timedelta(minutes=1),
            now=self.now,
        )
        self.assertTrue(accepted.satisfied, accepted.reason_codes)
        self.assertEqual(
            accepted.principal_ids,
            ("policy-principal-a", "policy-principal-b"),
        )
        duplicate = assess_root_policy_quorum(
            (endorsements[0], endorsements[0]),
            pinned_policy_roots=self.pinned_policy_roots,
            primary_root_keys={"offline-root-v1": self.root.public_key()},
            trust_bundle=self.bundle,
            admission_challenge="c" * 64,
            minimum_principals=2,
            signature_max_age=timedelta(minutes=1),
            now=self.now,
        )
        self.assertFalse(duplicate.satisfied)
        reused_primary = {
            **self.pinned_policy_roots,
            "policy-root-a": PinnedPolicyRoot(
                "policy-root-a",
                "policy-principal-a",
                self.root.public_key(),
            ),
        }
        invalid_policy = assess_root_policy_quorum(
            endorsements,
            pinned_policy_roots=reused_primary,
            primary_root_keys={"offline-root-v1": self.root.public_key()},
            trust_bundle=self.bundle,
            admission_challenge="c" * 64,
            minimum_principals=2,
            signature_max_age=timedelta(minutes=1),
            now=self.now,
        )
        self.assertFalse(invalid_policy.satisfied)
        self.assertEqual(
            invalid_policy.reason_codes,
            ("ROOT_POLICY_CONFIG_INVALID",),
        )
        changed_bundle = replace(
            self.bundle,
            signed_bundle_sha256="f" * 64,
        )
        mismatch = assess_root_policy_quorum(
            endorsements,
            pinned_policy_roots=self.pinned_policy_roots,
            primary_root_keys={"offline-root-v1": self.root.public_key()},
            trust_bundle=changed_bundle,
            admission_challenge="c" * 64,
            minimum_principals=2,
            signature_max_age=timedelta(minutes=1),
            now=self.now,
        )
        self.assertFalse(mismatch.satisfied)
        self.assertIn(
            "ROOT_POLICY_TRUST_BUNDLE_MISMATCH",
            mismatch.reason_codes,
        )
        wrong_challenge = assess_root_policy_quorum(
            endorsements,
            pinned_policy_roots=self.pinned_policy_roots,
            primary_root_keys={"offline-root-v1": self.root.public_key()},
            trust_bundle=self.bundle,
            admission_challenge="d" * 64,
            minimum_principals=2,
            signature_max_age=timedelta(minutes=1),
            now=self.now,
        )
        self.assertFalse(wrong_challenge.satisfied)
        self.assertIn(
            "ROOT_POLICY_ADMISSION_CHALLENGE_MISMATCH",
            wrong_challenge.reason_codes,
        )
        wrong_configuration = assess_root_policy_quorum(
            self.root_policy_endorsements(configuration_sha256="e" * 64),
            pinned_policy_roots=self.pinned_policy_roots,
            primary_root_keys={"offline-root-v1": self.root.public_key()},
            trust_bundle=self.bundle,
            admission_challenge="c" * 64,
            minimum_principals=2,
            signature_max_age=timedelta(minutes=1),
            now=self.now,
        )
        self.assertFalse(wrong_configuration.satisfied)
        self.assertIn(
            "ROOT_POLICY_CONFIGURATION_MISMATCH",
            wrong_configuration.reason_codes,
        )

    def test_root_policy_checkpoint_verifies_endorsements_itself(self) -> None:
        endorsements = self.root_policy_endorsements()
        accept_kwargs = dict(
            pinned_policy_roots=self.pinned_policy_roots,
            primary_root_keys={"offline-root-v1": self.root.public_key()},
            admission_challenge="c" * 64,
            minimum_principals=2,
            signature_max_age=timedelta(minutes=1),
            now=self.now,
        )
        with tempfile.TemporaryDirectory() as directory:
            checkpoint_path = Path(directory) / "root-policy.sqlite3"
            with RootPolicyCheckpointStore(checkpoint_path) as checkpoint:
                duplicate_signer = checkpoint.accept(
                    (endorsements[0], endorsements[0]), self.bundle, **accept_kwargs
                )
                self.assertFalse(duplicate_signer.accepted)
                self.assertEqual(
                    duplicate_signer.reason_codes,
                    ("ROOT_POLICY_CHECKPOINT_INPUT_INVALID",),
                )
                wrong_challenge = checkpoint.accept(
                    endorsements,
                    self.bundle,
                    **{**accept_kwargs, "admission_challenge": "d" * 64},
                )
                self.assertFalse(wrong_challenge.accepted)
                self.assertEqual(
                    wrong_challenge.reason_codes,
                    ("ROOT_POLICY_CHECKPOINT_INPUT_INVALID",),
                )
                self.assertTrue(
                    checkpoint.accept(
                        endorsements, self.bundle, **accept_kwargs
                    ).accepted
                )

    def test_root_policy_checkpoint_and_witnesses_reject_rollback(self) -> None:
        signed_bundle_2 = create_signed_trust_bundle(
            generation=2,
            keys=tuple(
                TrustedKeySpec(
                    record.key_id,
                    record.principal_id,
                    record.role,
                    record.public_key,
                    record.valid_from,
                    record.valid_until,
                    record.revoked_at,
                )
                for record in self.bundle.keys
            ),
            root_key_id="offline-root-v1",
            root_private_key=self.root,
            issued_at=self.now + timedelta(seconds=1),
            previous_signed_bundle_json=self.signed_bundle,
        )
        verification_2 = verify_signed_trust_bundle(
            signed_bundle_2,
            pinned_root_keys={"offline-root-v1": self.root.public_key()},
            signature_max_age=timedelta(seconds=5),
            now=self.now + timedelta(seconds=1),
        )
        self.assertIsNotNone(verification_2.bundle, verification_2.reason_codes)
        bundle_2 = verification_2.bundle
        assert bundle_2 is not None

        with tempfile.TemporaryDirectory() as directory:
            placement = self.placement(Path(directory))
            endorsements_1 = self.witnessed_root_policy_endorsements(placement)
            quorum_1 = assess_root_policy_quorum(
                endorsements_1,
                pinned_policy_roots=self.pinned_policy_roots,
                primary_root_keys={"offline-root-v1": self.root.public_key()},
                trust_bundle=self.bundle,
                admission_challenge="c" * 64,
                minimum_principals=2,
                signature_max_age=timedelta(minutes=1),
                now=self.now,
            )
            checkpoint_path = placement.root_policy_checkpoint_database_path
            assert checkpoint_path is not None
            with RootPolicyWitnessStateStore(
                checkpoint_path.parent / "root-policy-witness-a.sqlite3",
                self.pinned_policy_roots["policy-root-a"],
            ) as store:
                with self.assertRaisesRegex(
                    ValueError,
                    "ROOT_POLICY_WITNESS_CONFIGURATION_CHANGE_NOT_AUTHORIZED",
                ):
                    store.endorse(
                        policy_id="execution-root-policy-v1",
                        policy_configuration_sha256="e" * 64,
                        endorsement_id="unauthorized-root-configuration-g2",
                        private_key=self.policy_root,
                        trust_bundle=bundle_2,
                        admission_challenge="c" * 64,
                        endorsed_at=self.now + timedelta(seconds=1),
                        valid_until=self.now + timedelta(minutes=5),
                    )
            endorsements_2 = self.witnessed_root_policy_endorsements(
                placement,
                trust_bundle=bundle_2,
            )
            quorum_2 = assess_root_policy_quorum(
                endorsements_2,
                pinned_policy_roots=self.pinned_policy_roots,
                primary_root_keys={"offline-root-v1": self.root.public_key()},
                trust_bundle=bundle_2,
                admission_challenge="c" * 64,
                minimum_principals=2,
                signature_max_age=timedelta(minutes=1),
                now=self.now + timedelta(seconds=1),
            )
            self.assertTrue(quorum_1.satisfied, quorum_1.reason_codes)
            self.assertTrue(quorum_2.satisfied, quorum_2.reason_codes)
            accept_kwargs = dict(
                pinned_policy_roots=self.pinned_policy_roots,
                primary_root_keys={"offline-root-v1": self.root.public_key()},
                admission_challenge="c" * 64,
                minimum_principals=2,
                signature_max_age=timedelta(minutes=1),
            )
            with RootPolicyCheckpointStore(checkpoint_path) as checkpoint:
                self.assertTrue(
                    checkpoint.accept(
                        endorsements_1, self.bundle, now=self.now, **accept_kwargs
                    ).accepted
                )
                self.assertTrue(
                    checkpoint.accept(
                        endorsements_2,
                        bundle_2,
                        now=self.now + timedelta(seconds=1),
                        **accept_kwargs,
                    ).accepted
                )
                rollback = checkpoint.accept(
                    endorsements_1, self.bundle, now=self.now, **accept_kwargs
                )
                self.assertFalse(rollback.accepted)
                self.assertEqual(rollback.reason_codes, ("ROOT_POLICY_ROLLBACK",))
            with self.assertRaisesRegex(
                ValueError,
                "ROOT_POLICY_WITNESS_ROLLBACK",
            ):
                self.witnessed_root_policy_endorsements(placement)

    def test_root_policy_rotation_requires_previous_and_next_quorums(self) -> None:
        signed_bundle_2 = create_signed_trust_bundle(
            generation=2,
            keys=tuple(
                TrustedKeySpec(
                    record.key_id,
                    record.principal_id,
                    record.role,
                    record.public_key,
                    record.valid_from,
                    record.valid_until,
                    record.revoked_at,
                )
                for record in self.bundle.keys
            ),
            root_key_id="offline-root-v1",
            root_private_key=self.root,
            issued_at=self.now + timedelta(seconds=1),
            previous_signed_bundle_json=self.signed_bundle,
        )
        verification_2 = verify_signed_trust_bundle(
            signed_bundle_2,
            pinned_root_keys={"offline-root-v1": self.root.public_key()},
            signature_max_age=timedelta(seconds=5),
            now=self.now + timedelta(seconds=1),
        )
        self.assertIsNotNone(verification_2.bundle, verification_2.reason_codes)
        bundle_2 = verification_2.bundle
        assert bundle_2 is not None

        policy_root_c = Ed25519PrivateKey.generate()
        next_roots = {
            "policy-root-b": self.pinned_policy_roots["policy-root-b"],
            "policy-root-c": PinnedPolicyRoot(
                "policy-root-c",
                "policy-principal-c",
                policy_root_c.public_key(),
            ),
        }
        previous_configuration = root_policy_configuration_sha256(
            policy_id="execution-root-policy-v1",
            pinned_policy_roots=self.pinned_policy_roots,
            minimum_principals=2,
        )
        next_configuration = root_policy_configuration_sha256(
            policy_id="execution-root-policy-v1",
            pinned_policy_roots=next_roots,
            minimum_principals=2,
        )
        approvals = tuple(
            create_signed_root_policy_rotation_approval(
                rotation_id="policy-root-rotation-1",
                approval_side=side,
                policy_id="execution-root-policy-v1",
                previous_configuration_sha256=previous_configuration,
                next_configuration_sha256=next_configuration,
                target_bundle=bundle_2,
                admission_challenge="c" * 64,
                policy_root=root,
                private_key=private_key,
                approved_at=self.now + timedelta(seconds=1),
                valid_until=self.now + timedelta(minutes=5),
            )
            for side, root, private_key in (
                (
                    "PREVIOUS",
                    self.pinned_policy_roots["policy-root-a"],
                    self.policy_root,
                ),
                (
                    "PREVIOUS",
                    self.pinned_policy_roots["policy-root-b"],
                    self.policy_root_b,
                ),
                (
                    "NEXT",
                    next_roots["policy-root-b"],
                    self.policy_root_b,
                ),
                ("NEXT", next_roots["policy-root-c"], policy_root_c),
            )
        )
        rotation = assess_root_policy_rotation_quorum(
            approvals,
            rotation_id="policy-root-rotation-1",
            policy_id="execution-root-policy-v1",
            previous_policy_roots=self.pinned_policy_roots,
            previous_minimum_principals=2,
            next_policy_roots=next_roots,
            next_minimum_principals=2,
            primary_root_keys={"offline-root-v1": self.root.public_key()},
            target_bundle=bundle_2,
            admission_challenge="c" * 64,
            signature_max_age=timedelta(minutes=1),
            now=self.now + timedelta(seconds=1),
        )
        self.assertTrue(rotation.satisfied, rotation.reason_codes)
        rotation_evidence = RootPolicyRotationEvidence(
            signed_approvals=approvals,
            rotation_id="policy-root-rotation-1",
            policy_id="execution-root-policy-v1",
            previous_policy_roots=self.pinned_policy_roots,
            previous_minimum_principals=2,
            next_policy_roots=next_roots,
            next_minimum_principals=2,
            primary_root_keys={"offline-root-v1": self.root.public_key()},
            admission_challenge="c" * 64,
            signature_max_age=timedelta(minutes=1),
        )
        missing_previous = assess_root_policy_rotation_quorum(
            approvals[2:],
            rotation_id="policy-root-rotation-1",
            policy_id="execution-root-policy-v1",
            previous_policy_roots=self.pinned_policy_roots,
            previous_minimum_principals=2,
            next_policy_roots=next_roots,
            next_minimum_principals=2,
            primary_root_keys={"offline-root-v1": self.root.public_key()},
            target_bundle=bundle_2,
            admission_challenge="c" * 64,
            signature_max_age=timedelta(minutes=1),
            now=self.now + timedelta(seconds=1),
        )
        self.assertFalse(missing_previous.satisfied)
        self.assertIn(
            "ROOT_POLICY_PREVIOUS_ROTATION_QUORUM_NOT_REACHED",
            missing_previous.reason_codes,
        )
        missing_previous_evidence = replace(
            rotation_evidence,
            signed_approvals=approvals[2:],
        )

        next_endorsements = tuple(
            create_signed_root_policy_endorsement(
                policy_id="execution-root-policy-v1",
                policy_configuration_sha256=next_configuration,
                endorsement_id=f"next-root-endorsement-{suffix}",
                policy_root=next_roots[key_id],
                private_key=private_key,
                trust_bundle=bundle_2,
                admission_challenge="c" * 64,
                endorsed_at=self.now + timedelta(seconds=1),
                valid_until=self.now + timedelta(minutes=5),
            )
            for suffix, key_id, private_key in (
                ("b", "policy-root-b", self.policy_root_b),
                ("c", "policy-root-c", policy_root_c),
            )
        )
        quorum_1 = assess_root_policy_quorum(
            self.root_policy_endorsements(),
            pinned_policy_roots=self.pinned_policy_roots,
            primary_root_keys={"offline-root-v1": self.root.public_key()},
            trust_bundle=self.bundle,
            admission_challenge="c" * 64,
            minimum_principals=2,
            signature_max_age=timedelta(minutes=1),
            now=self.now,
        )
        quorum_2 = assess_root_policy_quorum(
            next_endorsements,
            pinned_policy_roots=next_roots,
            primary_root_keys={"offline-root-v1": self.root.public_key()},
            trust_bundle=bundle_2,
            admission_challenge="c" * 64,
            minimum_principals=2,
            signature_max_age=timedelta(minutes=1),
            now=self.now + timedelta(seconds=1),
        )
        self.assertTrue(quorum_1.satisfied, quorum_1.reason_codes)
        self.assertTrue(quorum_2.satisfied, quorum_2.reason_codes)
        with tempfile.TemporaryDirectory() as directory:
            checkpoint_path = Path(directory) / "root-policy.sqlite3"
            previous_accept_kwargs = dict(
                pinned_policy_roots=self.pinned_policy_roots,
                primary_root_keys={"offline-root-v1": self.root.public_key()},
                admission_challenge="c" * 64,
                minimum_principals=2,
                signature_max_age=timedelta(minutes=1),
            )
            next_accept_kwargs = dict(
                pinned_policy_roots=next_roots,
                primary_root_keys={"offline-root-v1": self.root.public_key()},
                admission_challenge="c" * 64,
                minimum_principals=2,
                signature_max_age=timedelta(minutes=1),
            )
            with RootPolicyCheckpointStore(checkpoint_path) as checkpoint:
                self.assertTrue(
                    checkpoint.accept(
                        self.root_policy_endorsements(),
                        self.bundle,
                        now=self.now,
                        **previous_accept_kwargs,
                    ).accepted
                )
                unauthorized = checkpoint.accept(
                    next_endorsements,
                    bundle_2,
                    now=self.now + timedelta(seconds=1),
                    **next_accept_kwargs,
                )
                self.assertFalse(unauthorized.accepted)
                self.assertEqual(
                    unauthorized.reason_codes,
                    ("ROOT_POLICY_CONFIGURATION_CHANGE_NOT_AUTHORIZED",),
                )
                forged_type_name_is_not_enough = checkpoint.accept(
                    next_endorsements,
                    bundle_2,
                    rotation_evidence=missing_previous_evidence,
                    now=self.now + timedelta(seconds=1),
                    **next_accept_kwargs,
                )
                self.assertFalse(forged_type_name_is_not_enough.accepted)
                authorized = checkpoint.accept(
                    next_endorsements,
                    bundle_2,
                    rotation_evidence=rotation_evidence,
                    now=self.now + timedelta(seconds=1),
                    **next_accept_kwargs,
                )
                self.assertTrue(authorized.accepted, authorized.reason_codes)

            witness_path = Path(directory) / "root-policy-witness-c.sqlite3"
            retained_path = Path(directory) / "root-policy-witness-b.sqlite3"
            with RootPolicyWitnessStateStore(
                retained_path,
                self.pinned_policy_roots["policy-root-b"],
            ) as retained_witness:
                retained_witness.endorse(
                    policy_id="execution-root-policy-v1",
                    policy_configuration_sha256=previous_configuration,
                    endorsement_id="retained-root-b-g1",
                    private_key=self.policy_root_b,
                    trust_bundle=self.bundle,
                    admission_challenge="c" * 64,
                    endorsed_at=self.now,
                    valid_until=self.now + timedelta(minutes=5),
                )
                with self.assertRaisesRegex(
                    ValueError,
                    "invalid root policy endorsement",
                ):
                    retained_witness.rotate_retained(
                        rotation_evidence=rotation_evidence,
                        policy_configuration_sha256=next_configuration,
                        endorsement_id="retained-root-b-g2",
                        private_key=policy_root_c,
                        trust_bundle=bundle_2,
                        admission_challenge="c" * 64,
                        endorsed_at=self.now + timedelta(seconds=1),
                        valid_until=self.now + timedelta(minutes=5),
                    )
                retained_endorsement = retained_witness.rotate_retained(
                    rotation_evidence=rotation_evidence,
                    policy_configuration_sha256=next_configuration,
                    endorsement_id="retained-root-b-g2",
                    private_key=self.policy_root_b,
                    trust_bundle=bundle_2,
                    admission_challenge="c" * 64,
                    endorsed_at=self.now + timedelta(seconds=1),
                    valid_until=self.now + timedelta(minutes=5),
                )
            removed_path = Path(directory) / "root-policy-witness-a.sqlite3"
            with RootPolicyWitnessStateStore(
                removed_path,
                self.pinned_policy_roots["policy-root-a"],
            ) as removed_witness:
                removed_witness.endorse(
                    policy_id="execution-root-policy-v1",
                    policy_configuration_sha256=previous_configuration,
                    endorsement_id="removed-root-a-g1",
                    private_key=self.policy_root,
                    trust_bundle=self.bundle,
                    admission_challenge="c" * 64,
                    endorsed_at=self.now,
                    valid_until=self.now + timedelta(minutes=5),
                )
                with self.assertRaisesRegex(
                    ValueError,
                    "ROOT_POLICY_WITNESS_ROTATION_INVALID",
                ):
                    removed_witness.rotate_retained(
                        rotation_evidence=rotation_evidence,
                        policy_configuration_sha256=next_configuration,
                        endorsement_id="removed-root-a-g2",
                        private_key=self.policy_root,
                        trust_bundle=bundle_2,
                        admission_challenge="c" * 64,
                        endorsed_at=self.now + timedelta(seconds=1),
                        valid_until=self.now + timedelta(minutes=5),
                    )
            with RootPolicyWitnessStateStore(
                witness_path,
                next_roots["policy-root-c"],
            ) as new_witness:
                with self.assertRaisesRegex(
                    ValueError,
                    "invalid root policy endorsement",
                ):
                    new_witness.bootstrap_rotation(
                        rotation_evidence=rotation_evidence,
                        policy_configuration_sha256=next_configuration,
                        endorsement_id="bootstrap-root-c",
                        private_key=self.policy_root,
                        trust_bundle=bundle_2,
                        admission_challenge="c" * 64,
                        endorsed_at=self.now + timedelta(seconds=1),
                        valid_until=self.now + timedelta(minutes=5),
                    )
                bootstrapped_endorsement = new_witness.bootstrap_rotation(
                    rotation_evidence=rotation_evidence,
                    policy_configuration_sha256=next_configuration,
                    endorsement_id="bootstrap-root-c",
                    private_key=policy_root_c,
                    trust_bundle=bundle_2,
                    admission_challenge="c" * 64,
                    endorsed_at=self.now + timedelta(seconds=1),
                    valid_until=self.now + timedelta(minutes=5),
                )
                with self.assertRaisesRegex(
                    ValueError,
                    "ROOT_POLICY_WITNESS_BOOTSTRAP_NOT_EMPTY",
                ):
                    new_witness.bootstrap_rotation(
                        rotation_evidence=rotation_evidence,
                        policy_configuration_sha256=next_configuration,
                        endorsement_id="bootstrap-root-c-again",
                        private_key=policy_root_c,
                        trust_bundle=bundle_2,
                        admission_challenge="c" * 64,
                        endorsed_at=self.now + timedelta(seconds=1),
                        valid_until=self.now + timedelta(minutes=5),
                    )
            bootstrap_quorum = assess_root_policy_quorum(
                (retained_endorsement, bootstrapped_endorsement),
                pinned_policy_roots=next_roots,
                primary_root_keys={"offline-root-v1": self.root.public_key()},
                trust_bundle=bundle_2,
                admission_challenge="c" * 64,
                minimum_principals=2,
                signature_max_age=timedelta(minutes=1),
                now=self.now + timedelta(seconds=1),
            )
            self.assertTrue(bootstrap_quorum.satisfied, bootstrap_quorum.reason_codes)

    def test_root_policy_witness_service_issues_state_bound_rotation_approval(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            _, root_public, _ = self.launcher_material(temporary)
            policy_private_path = temporary / "policy-root-b.pem"
            policy_private_path.write_bytes(
                self.policy_root_b.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.PKCS8,
                    serialization.NoEncryption(),
                )
            )
            process = RootPolicyWitnessProcess(
                temporary / "online-root-policy-witness-b.sqlite3",
                "policy-principal-b",
                "policy-root-b",
                policy_private_path,
                "policy-host-b",
                "policy-os-identity-b",
                "policy-key-custodian-b",
                "policy-state-custodian-b",
            )
            issued_at = datetime.now(timezone.utc)
            signed_bundle_2 = create_signed_trust_bundle(
                generation=2,
                keys=tuple(
                    TrustedKeySpec(
                        record.key_id,
                        record.principal_id,
                        record.role,
                        record.public_key,
                        record.valid_from,
                        record.valid_until,
                        record.revoked_at,
                    )
                    for record in self.bundle.keys
                ),
                root_key_id="offline-root-v1",
                root_private_key=self.root,
                issued_at=issued_at,
                previous_signed_bundle_json=self.signed_bundle,
            )
            verification = verify_signed_trust_bundle(
                signed_bundle_2,
                pinned_root_keys={"offline-root-v1": self.root.public_key()},
                signature_max_age=timedelta(minutes=1),
                now=issued_at,
            )
            self.assertIsNotNone(verification.bundle, verification.reason_codes)
            bundle_2 = verification.bundle
            assert bundle_2 is not None
            policy_root_c = Ed25519PrivateKey.generate()
            next_roots = {
                "policy-root-b": self.pinned_policy_roots["policy-root-b"],
                "policy-root-c": PinnedPolicyRoot(
                    "policy-root-c",
                    "policy-principal-c",
                    policy_root_c.public_key(),
                ),
            }
            previous_configuration = root_policy_configuration_sha256(
                policy_id="execution-root-policy-v1",
                pinned_policy_roots=self.pinned_policy_roots,
                minimum_principals=2,
            )
            next_configuration = root_policy_configuration_sha256(
                policy_id="execution-root-policy-v1",
                pinned_policy_roots=next_roots,
                minimum_principals=2,
            )
            with RootPolicyWitnessStateStore(
                process.database_path,
                self.pinned_policy_roots["policy-root-b"],
            ) as store:
                store.endorse(
                    policy_id="execution-root-policy-v1",
                    policy_configuration_sha256=previous_configuration,
                    endorsement_id="service-root-b-g1",
                    private_key=self.policy_root_b,
                    trust_bundle=self.bundle,
                    admission_challenge="c" * 64,
                    endorsed_at=self.now,
                    valid_until=self.now + timedelta(minutes=5),
                )

            def invoke(request: dict[str, object]) -> subprocess.CompletedProcess[str]:
                return subprocess.run(
                    (
                        sys.executable,
                        "-m",
                        "note.poc_horizontal_ai.trusted_runtime.root_policy_witness_service",
                        "--witness-database",
                        str(process.database_path),
                        "--policy-root-principal-id",
                        process.principal_id,
                        "--policy-root-key-id",
                        process.key_id,
                        "--policy-root-private-key-file",
                        str(process.private_key_path),
                        "--policy-root-public-key-fingerprint",
                        hashlib.sha256(
                            self.policy_root_b.public_key().public_bytes(
                                serialization.Encoding.Raw,
                                serialization.PublicFormat.Raw,
                            )
                        ).hexdigest(),
                        "--pinned-root-key-id",
                        "offline-root-v1",
                        "--pinned-root-public-key-file",
                        str(root_public),
                        "--trust-bundle-max-age-seconds",
                        "300",
                        "--endorsement-validity-seconds",
                        "300",
                    ),
                    input=json.dumps(request, sort_keys=True, separators=(",", ":")),
                    capture_output=True,
                    text=True,
                    timeout=5.0,
                    check=False,
                )

            base_request = {
                "admission_challenge": "c" * 64,
                "next_configuration_sha256": next_configuration,
                "policy_id": "execution-root-policy-v1",
                "previous_configuration_sha256": previous_configuration,
                "rotation_id": "online-policy-root-rotation-1",
                "schema_version": "root-policy-rotation-approval-request/1.0",
                "signed_trust_bundle_json": signed_bundle_2,
            }
            previous_result = invoke(
                {**base_request, "approval_side": "PREVIOUS"}
            )
            next_result = invoke({**base_request, "approval_side": "NEXT"})
            self.assertEqual(previous_result.returncode, 0, previous_result.stdout)
            self.assertEqual(next_result.returncode, 0, next_result.stdout)

            direct_approvals = (
                create_signed_root_policy_rotation_approval(
                    rotation_id="online-policy-root-rotation-1",
                    approval_side="PREVIOUS",
                    policy_id="execution-root-policy-v1",
                    previous_configuration_sha256=previous_configuration,
                    next_configuration_sha256=next_configuration,
                    target_bundle=bundle_2,
                    admission_challenge="c" * 64,
                    policy_root=self.pinned_policy_roots["policy-root-a"],
                    private_key=self.policy_root,
                    approved_at=issued_at,
                    valid_until=issued_at + timedelta(minutes=5),
                ),
                create_signed_root_policy_rotation_approval(
                    rotation_id="online-policy-root-rotation-1",
                    approval_side="NEXT",
                    policy_id="execution-root-policy-v1",
                    previous_configuration_sha256=previous_configuration,
                    next_configuration_sha256=next_configuration,
                    target_bundle=bundle_2,
                    admission_challenge="c" * 64,
                    policy_root=next_roots["policy-root-c"],
                    private_key=policy_root_c,
                    approved_at=issued_at,
                    valid_until=issued_at + timedelta(minutes=5),
                ),
            )
            rotation = assess_root_policy_rotation_quorum(
                (previous_result.stdout, direct_approvals[0], next_result.stdout, direct_approvals[1]),
                rotation_id="online-policy-root-rotation-1",
                policy_id="execution-root-policy-v1",
                previous_policy_roots=self.pinned_policy_roots,
                previous_minimum_principals=2,
                next_policy_roots=next_roots,
                next_minimum_principals=2,
                primary_root_keys={"offline-root-v1": self.root.public_key()},
                target_bundle=bundle_2,
                admission_challenge="c" * 64,
                signature_max_age=timedelta(minutes=1),
                now=datetime.now(timezone.utc),
            )
            self.assertTrue(rotation.satisfied, rotation.reason_codes)
            changed_previous = invoke(
                {
                    **base_request,
                    "approval_side": "PREVIOUS",
                    "previous_configuration_sha256": "e" * 64,
                    "rotation_id": "online-policy-root-rotation-bad",
                }
            )
            self.assertEqual(changed_previous.returncode, 2)
            mixed_schema = invoke(
                {
                    **base_request,
                    "approval_side": "PREVIOUS",
                    "policy_configuration_sha256": previous_configuration,
                }
            )
            self.assertEqual(mixed_schema.returncode, 2)

    def test_rotation_collection_gates_next_processes_on_previous_quorum(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            _, root_public, _ = self.launcher_material(temporary)
            policy_root_c = Ed25519PrivateKey.generate()
            private_keys = {
                "a": self.policy_root,
                "b": self.policy_root_b,
                "c": policy_root_c,
            }
            private_paths = {}
            for suffix, private_key in private_keys.items():
                path = temporary / f"rotation-policy-root-{suffix}.pem"
                path.write_bytes(
                    private_key.private_bytes(
                        serialization.Encoding.PEM,
                        serialization.PrivateFormat.PKCS8,
                        serialization.NoEncryption(),
                    )
                )
                private_paths[suffix] = path

            issued_at = datetime.now(timezone.utc)
            signed_bundle_2 = create_signed_trust_bundle(
                generation=2,
                keys=tuple(
                    TrustedKeySpec(
                        record.key_id,
                        record.principal_id,
                        record.role,
                        record.public_key,
                        record.valid_from,
                        record.valid_until,
                        record.revoked_at,
                    )
                    for record in self.bundle.keys
                ),
                root_key_id="offline-root-v1",
                root_private_key=self.root,
                issued_at=issued_at,
                previous_signed_bundle_json=self.signed_bundle,
            )
            verification = verify_signed_trust_bundle(
                signed_bundle_2,
                pinned_root_keys={"offline-root-v1": self.root.public_key()},
                signature_max_age=timedelta(minutes=1),
                now=issued_at,
            )
            self.assertIsNotNone(verification.bundle, verification.reason_codes)
            bundle_2 = verification.bundle
            assert bundle_2 is not None
            next_roots = {
                "policy-root-b": self.pinned_policy_roots["policy-root-b"],
                "policy-root-c": PinnedPolicyRoot(
                    "policy-root-c",
                    "policy-principal-c",
                    policy_root_c.public_key(),
                ),
            }
            previous_configuration = root_policy_configuration_sha256(
                policy_id="execution-root-policy-v1",
                pinned_policy_roots=self.pinned_policy_roots,
                minimum_principals=2,
            )
            process_a = RootPolicyWitnessProcess(
                temporary / "rotation-old-a.sqlite3",
                "policy-principal-a",
                "policy-root-a",
                private_paths["a"],
                "rotation-host-a",
                "rotation-os-a",
                "rotation-key-domain-a",
                "rotation-state-domain-a",
            )
            process_b = RootPolicyWitnessProcess(
                temporary / "rotation-retained-b.sqlite3",
                "policy-principal-b",
                "policy-root-b",
                private_paths["b"],
                "rotation-host-b",
                "rotation-os-b",
                "rotation-key-domain-b",
                "rotation-state-domain-b",
            )
            process_c = RootPolicyWitnessProcess(
                temporary / "rotation-new-c.sqlite3",
                "policy-principal-c",
                "policy-root-c",
                private_paths["c"],
                "rotation-host-c",
                "rotation-os-c",
                "rotation-key-domain-c",
                "rotation-state-domain-c",
            )
            for process, root, private_key, suffix in (
                (
                    process_a,
                    self.pinned_policy_roots["policy-root-a"],
                    self.policy_root,
                    "a",
                ),
                (
                    process_b,
                    self.pinned_policy_roots["policy-root-b"],
                    self.policy_root_b,
                    "b",
                ),
            ):
                with RootPolicyWitnessStateStore(
                    process.database_path,
                    root,
                ) as store:
                    store.endorse(
                        policy_id="execution-root-policy-v1",
                        policy_configuration_sha256=previous_configuration,
                        endorsement_id=f"rotation-seed-{suffix}",
                        private_key=private_key,
                        trust_bundle=self.bundle,
                        admission_challenge="a" * 64,
                        endorsed_at=self.now,
                        valid_until=self.now + timedelta(minutes=5),
                    )

            bad_process_b = replace(
                process_b,
                private_key_path=private_paths["c"],
            )
            common = {
                "rotation_id": "online-policy-root-rotation-2",
                "policy_id": "execution-root-policy-v1",
                "previous_policy_roots": self.pinned_policy_roots,
                "previous_minimum_principals": 2,
                "next_processes": (process_b, process_c),
                "next_policy_roots": next_roots,
                "next_minimum_principals": 2,
                "signed_trust_bundle_json": signed_bundle_2,
                "pinned_root_key_id": "offline-root-v1",
                "pinned_root_public_key_path": root_public,
                "trust_bundle_signature_max_age": timedelta(minutes=1),
                "approval_signature_max_age": timedelta(minutes=1),
                "approval_validity": timedelta(minutes=5),
                "process_timeout_seconds": 5.0,
                "admission_challenge": "c" * 64,
                "now": issued_at,
            }
            with self.assertRaisesRegex(
                ValueError,
                "ROOT_POLICY_PREVIOUS_ROTATION_QUORUM_NOT_REACHED",
            ):
                collect_root_policy_rotation_evidence(
                    previous_processes=(process_a, bad_process_b),
                    **common,
                )
            self.assertFalse(process_c.database_path.exists())

            evidence = collect_root_policy_rotation_evidence(
                previous_processes=(process_a, process_b),
                **common,
            )
            self.assertEqual(len(evidence.signed_approvals), 4)
            final = assess_root_policy_rotation_quorum(
                evidence.signed_approvals,
                rotation_id=evidence.rotation_id,
                policy_id=evidence.policy_id,
                previous_policy_roots=evidence.previous_policy_roots,
                previous_minimum_principals=(
                    evidence.previous_minimum_principals
                ),
                next_policy_roots=evidence.next_policy_roots,
                next_minimum_principals=evidence.next_minimum_principals,
                primary_root_keys=evidence.primary_root_keys,
                target_bundle=bundle_2,
                admission_challenge=evidence.admission_challenge,
                signature_max_age=evidence.signature_max_age,
                now=datetime.now(timezone.utc),
            )
            self.assertTrue(final.satisfied, final.reason_codes)
            self.assertTrue(process_c.database_path.exists())

    def test_tampered_checkpoint_is_not_witnessed(self) -> None:
        checkpoint = self.checkpoint(self.head_1, "checkpoint-1")
        tampered = checkpoint.replace('"payload_json":"', '"payload_json":"x', 1)
        verified, reasons = verify_signed_latch_checkpoint(
            tampered,
            trust_bundle=self.bundle,
            signature_max_age=timedelta(seconds=5),
            now=self.now,
        )
        self.assertIsNone(verified)
        self.assertTrue(reasons)
        with tempfile.TemporaryDirectory() as directory:
            with LatchCheckpointWitnessStateStore(
                Path(directory) / "witness.sqlite3",
                "principal-a",
                "repo-latch-v1",
            ) as store:
                with self.assertRaises(ValueError):
                    store.attest(
                        (tampered,),
                        trust_bundle=self.bundle,
                        checkpoint_signature_max_age=timedelta(seconds=5),
                        witness_key_id="witness-a1",
                        witness_private_key=self.witness_a1,
                        witnessed_at=self.now,
                    )

    def test_witness_rejects_checkpoint_from_another_latch_store(self) -> None:
        other_checkpoint = create_signed_latch_checkpoint(
            self.head_1,
            checkpoint_id="other-checkpoint",
            latch_store_id="other-latch-v1",
            signing_key_id="latch-checkpoint-v1",
            signing_private_key=self.checkpoint_signer,
            trust_bundle=self.bundle,
            checkpointed_at=self.now,
        )
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "witness.sqlite3"
            with LatchCheckpointWitnessStateStore(
                database,
                "principal-a",
                "repo-latch-v1",
            ) as store:
                with self.assertRaisesRegex(
                    ValueError,
                    "LATCH_WITNESS_SCOPE_MISMATCH",
                ):
                    store.attest(
                        (other_checkpoint,),
                        trust_bundle=self.bundle,
                        checkpoint_signature_max_age=timedelta(seconds=5),
                        witness_key_id="witness-a1",
                        witness_private_key=self.witness_a1,
                        witnessed_at=self.now,
                    )
            with self.assertRaisesRegex(
                ValueError,
                "LATCH_WITNESS_SCOPE_MISMATCH",
            ):
                LatchCheckpointWitnessStateStore(
                    database,
                    "principal-a",
                    "other-latch-v1",
                )

    def test_separate_process_witness_service_attests_checkpoint(self) -> None:
        checkpoint = self.checkpoint(self.head_1, "checkpoint-1")
        challenge = create_boundary_admission_challenge()
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            root_public = temporary / "root-public.pem"
            witness_private = temporary / "witness-private.pem"
            root_public.write_bytes(
                self.root.public_key().public_bytes(
                    serialization.Encoding.PEM,
                    serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )
            witness_private.write_bytes(
                self.witness_a1.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.PKCS8,
                    serialization.NoEncryption(),
                )
            )
            request = json.dumps(
                {
                    "admission_challenge": challenge.nonce,
                    "schema_version": "latch-witness-request/1.0",
                    "signed_latch_checkpoints": [checkpoint],
                    "signed_trust_bundle_json": self.signed_bundle,
                }
            )
            result = subprocess.run(
                (
                    sys.executable,
                    "-m",
                    "note.poc_horizontal_ai.trusted_runtime.latch_witness_service",
                    "--witness-database",
                    str(temporary / "witness.sqlite3"),
                    "--witness-principal-id",
                    "principal-a",
                    "--latch-store-id",
                    "repo-latch-v1",
                    "--witness-key-id",
                    "witness-a1",
                    "--witness-private-key-file",
                    str(witness_private),
                    "--pinned-root-key-id",
                    "offline-root-v1",
                    "--pinned-root-public-key-file",
                    str(root_public),
                ),
                input=request,
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            verified, reasons = verify_latch_witness_attestation(
                result.stdout,
                trust_bundle=self.bundle,
                signature_max_age=timedelta(minutes=5),
                now=datetime.now(timezone.utc),
            )
            self.assertEqual(reasons, ())
            self.assertIsNotNone(verified)
            assert verified is not None
            self.assertEqual(verified.witness_principal_id, "principal-a")
            self.assertEqual(verified.admission_challenge, challenge.nonce)

    def test_nonempty_runtime_requires_fresh_two_principal_quorum(self) -> None:
        integrity_key = b"L" * 32
        thresholds = Thresholds(0.4, 0.6, 0.8)
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            placement = self.placement(temporary)
            witness_a_database = temporary / "witness-a.sqlite3"
            witness_b_database = temporary / "witness-b.sqlite3"
            genesis_challenge = create_boundary_admission_challenge()
            genesis_checkpoint = create_signed_latch_genesis(
                checkpoint_id="runtime-genesis",
                latch_store_id="repo-latch-v1",
                signing_key_id="latch-checkpoint-v1",
                signing_private_key=self.checkpoint_signer,
                trust_bundle=self.bundle,
                checkpointed_at=self.now,
            )
            genesis_attestation_a = self.attest(
                witness_a_database,
                "principal-a",
                "witness-a1",
                self.witness_a1,
                (genesis_checkpoint,),
                genesis_challenge.nonce,
            )
            genesis_attestation_b = self.attest(
                witness_b_database,
                "principal-b",
                "witness-b",
                self.witness_b,
                (genesis_checkpoint,),
                genesis_challenge.nonce,
            )
            genesis_evidence = ExternalLatchWitnessEvidence(
                signed_trust_bundle_json=self.signed_bundle,
                signed_latch_checkpoint_json=genesis_checkpoint,
                signed_witness_attestations=(
                    genesis_attestation_a,
                    genesis_attestation_b,
                ),
                minimum_principals=2,
                signature_max_age=timedelta(seconds=5),
            )
            with self.assertRaisesRegex(
                ValueError,
                "ROOT_POLICY_EVIDENCE_REQUIRED",
            ):
                admit_boundary_runtime(
                    placement=placement,
                    latch_integrity_key=integrity_key,
                    latch_store_id="repo-latch-v1",
                    admission_challenge=genesis_challenge,
                    external_witness_evidence=genesis_evidence,
                    pinned_root_keys={
                        "offline-root-v1": self.root.public_key()
                    },
                    trust_bundle_signature_max_age=timedelta(seconds=5),
                    now=self.now,
                )
            with self.assertRaisesRegex(
                ValueError,
                "AUTHORITY_MANIFEST_EVIDENCE_REQUIRED",
            ):
                admit_boundary_runtime(
                    placement=placement,
                    latch_integrity_key=integrity_key,
                    latch_store_id="repo-latch-v1",
                    admission_challenge=genesis_challenge,
                    external_witness_evidence=replace(
                        genesis_evidence,
                        signed_root_policy_endorsements=(
                            self.witnessed_root_policy_endorsements(
                                placement,
                                admission_challenge=genesis_challenge.nonce,
                            )
                        ),
                    ),
                    pinned_root_keys={
                        "offline-root-v1": self.root.public_key()
                    },
                    trust_bundle_signature_max_age=timedelta(seconds=5),
                    pinned_policy_roots=self.pinned_policy_roots,
                    minimum_policy_root_principals=2,
                    root_policy_signature_max_age=timedelta(seconds=5),
                    now=self.now,
                )
            with self.admit_runtime(
                placement=placement,
                latch_integrity_key=integrity_key,
                latch_store_id="repo-latch-v1",
                admission_challenge=genesis_challenge,
                external_witness_evidence=genesis_evidence,
                now=self.now,
            ) as runtime:
                self.assertTrue(runtime.external_witness_current)
                self.assertTrue(
                    runtime.deployment_assessment.authority_domain_separation_verified
                )
                self.assertNotIn(
                    "AUTHORITY_DOMAIN_SEPARATION_NOT_ATTESTED",
                    runtime.deployment_assessment.reason_codes,
                )
                result = runtime.assess_axes(
                    target_id="repo-1",
                    axes=(AxisEvidence("scope_escape", 0.8, 1.0, thresholds),),
                    observed_at=self.now,
                )
                self.assertEqual(
                    result.target_state,
                    TargetBoundaryState.IRREVERSIBLE_TRANSITION,
                )
                self.assertFalse(runtime.external_witness_current)

            with self.assertRaisesRegex(
                ValueError,
                "LATCH_EXTERNAL_WITNESS_REQUIRED",
            ):
                self.admit_runtime(
                    placement=placement,
                    latch_integrity_key=integrity_key,
                    latch_store_id="repo-latch-v1",
                    admission_challenge=create_boundary_admission_challenge(),
                    now=self.now,
                )

            with PersistentIrreversibleLatchStore(
                placement.latch_database_path,
                integrity_key,
            ) as latch_store:
                head = latch_store.head()
            assert head is not None
            checkpoint = self.checkpoint(head, "runtime-checkpoint-1")
            head_challenge = create_boundary_admission_challenge()
            attestation_a = self.attest(
                witness_a_database,
                "principal-a",
                "witness-a1",
                self.witness_a1,
                (checkpoint,),
                head_challenge.nonce,
            )
            attestation_b = self.attest(
                witness_b_database,
                "principal-b",
                "witness-b",
                self.witness_b,
                (checkpoint,),
                head_challenge.nonce,
            )
            insufficient_evidence = ExternalLatchWitnessEvidence(
                signed_trust_bundle_json=self.signed_bundle,
                signed_latch_checkpoint_json=checkpoint,
                signed_witness_attestations=(attestation_a,),
                minimum_principals=2,
                signature_max_age=timedelta(seconds=5),
            )
            with self.assertRaisesRegex(
                ValueError,
                "LATCH_WITNESS_QUORUM_NOT_REACHED",
            ):
                self.admit_runtime(
                    placement=placement,
                    latch_integrity_key=integrity_key,
                    latch_store_id="repo-latch-v1",
                    admission_challenge=create_boundary_admission_challenge(),
                    external_witness_evidence=ExternalLatchWitnessEvidence(
                        signed_trust_bundle_json=self.signed_bundle,
                        signed_latch_checkpoint_json=checkpoint,
                        signed_witness_attestations=(
                            attestation_a,
                            attestation_b,
                        ),
                        minimum_principals=2,
                        signature_max_age=timedelta(seconds=5),
                    ),
                    now=self.now,
                )
            with self.assertRaisesRegex(
                ValueError,
                "LATCH_WITNESS_QUORUM_NOT_REACHED",
            ):
                self.admit_runtime(
                    placement=placement,
                    latch_integrity_key=integrity_key,
                    latch_store_id="repo-latch-v1",
                    admission_challenge=head_challenge,
                    external_witness_evidence=insufficient_evidence,
                    now=self.now,
                )
            evidence = ExternalLatchWitnessEvidence(
                signed_trust_bundle_json=self.signed_bundle,
                signed_latch_checkpoint_json=checkpoint,
                signed_witness_attestations=(attestation_a, attestation_b),
                minimum_principals=2,
                signature_max_age=timedelta(seconds=5),
            )
            with self.admit_runtime(
                placement=placement,
                latch_integrity_key=integrity_key,
                latch_store_id="repo-latch-v1",
                admission_challenge=head_challenge,
                external_witness_evidence=evidence,
                now=self.now,
            ) as reopened:
                self.assertTrue(reopened.external_witness_current)
                retained = reopened.assess_axes(
                    target_id="repo-1",
                    axes=(AxisEvidence("scope_escape", 0.1, 1.0, thresholds),),
                    observed_at=self.now,
                )
                self.assertEqual(
                    retained.target_state,
                    TargetBoundaryState.IRREVERSIBLE_TRANSITION,
                )
                self.assertTrue(reopened.external_witness_current)

            with self.assertRaisesRegex(
                ValueError,
                "BOUNDARY_ADMISSION_CHALLENGE_REUSED",
            ):
                self.admit_runtime(
                    placement=placement,
                    latch_integrity_key=integrity_key,
                    latch_store_id="repo-latch-v1",
                    admission_challenge=head_challenge,
                    external_witness_evidence=evidence,
                    now=self.now,
                )

            replay_challenge = create_boundary_admission_challenge()
            replay_evidence = ExternalLatchWitnessEvidence(
                signed_trust_bundle_json=self.signed_bundle,
                signed_latch_checkpoint_json=genesis_checkpoint,
                signed_witness_attestations=(
                    genesis_attestation_a,
                    genesis_attestation_b,
                ),
                minimum_principals=2,
                signature_max_age=timedelta(seconds=5),
            )
            with self.assertRaisesRegex(
                ValueError,
                "LATCH_WITNESS_STATE_MISMATCH",
            ):
                self.admit_runtime(
                    placement=placement,
                    latch_integrity_key=integrity_key,
                    latch_store_id="repo-latch-v1",
                    admission_challenge=replay_challenge,
                    external_witness_evidence=replay_evidence,
                    now=self.now,
                )

    def test_launcher_rejects_policy_witness_deployment_tamper(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            placement = self.placement(temporary)
            signer, root_public, processes = self.launcher_material(temporary)
            with self.assertRaisesRegex(
                ValueError,
                "POLICY_WITNESS_DEPLOYMENT_MISMATCH",
            ):
                self.launch(
                    placement,
                    signer,
                    root_public,
                    processes,
                    policy_process_host_override="tampered-policy-host",
                )

    def test_launcher_rejects_policy_witness_execution_authority_overlap(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            placement = self.placement(temporary)
            signer, root_public, processes = self.launcher_material(temporary)
            with self.assertRaisesRegex(
                ValueError,
                "POLICY_WITNESS_EXECUTION_AUTHORITY_DOMAIN_OVERLAP",
            ):
                self.launch(
                    placement,
                    signer,
                    root_public,
                    processes,
                    policy_process_authority_overlap=True,
                )

    def test_launcher_requires_two_online_policy_root_processes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            placement = self.placement(temporary)
            signer, root_public, processes = self.launcher_material(temporary)
            with self.assertRaisesRegex(
                ValueError,
                "ROOT_POLICY_QUORUM_CONFIG_INVALID",
            ):
                self.launch(
                    placement,
                    signer,
                    root_public,
                    processes,
                    policy_process_limit=1,
                )

    def test_launcher_rejects_witness_state_database_inside_repository(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            placement = self.placement(temporary)
            signer, root_public, processes = self.launcher_material(temporary)
            tampered_processes = (
                processes[0],
                replace(
                    processes[1],
                    database_path=Path.cwd() / "launcher-witness-b.sqlite3",
                ),
            )
            with self.assertRaisesRegex(
                ValueError,
                "LATCH_CHECKPOINT_SIGNER_STATE_PLACEMENT_INVALID",
            ):
                self.launch(
                    placement,
                    signer,
                    root_public,
                    tampered_processes,
                )

    def test_launcher_completes_genesis_and_multi_head_witness_rounds(self) -> None:
        thresholds = Thresholds(0.4, 0.6, 0.8)
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            placement = self.placement(temporary)
            signer, root_public, processes = self.launcher_material(temporary)
            with self.launch(
                placement,
                signer,
                root_public,
                processes,
            ) as runtime:
                self.assertTrue(runtime.external_witness_current)
                result = runtime.assess_axes(
                    target_id="repo-1",
                    axes=(
                        AxisEvidence("scope_escape", 0.8, 1.0, thresholds),
                        AxisEvidence("secret_exposure", 0.9, 1.0, thresholds),
                    ),
                    observed_at=self.now,
                )
                self.assertEqual(
                    result.target_state,
                    TargetBoundaryState.IRREVERSIBLE_TRANSITION,
                )
                self.assertFalse(runtime.external_witness_current)

            with self.launch(
                placement,
                signer,
                root_public,
                processes,
            ) as reopened:
                self.assertTrue(reopened.external_witness_current)
                retained = reopened.assess_axes(
                    target_id="repo-1",
                    axes=(AxisEvidence("scope_escape", 0.1, 1.0, thresholds),),
                    observed_at=self.now,
                )
                self.assertEqual(
                    retained.target_state,
                    TargetBoundaryState.IRREVERSIBLE_TRANSITION,
                )
                self.assertTrue(reopened.external_witness_current)

    def test_execution_gate_is_two_stage_bound_and_fail_closed(self) -> None:
        thresholds = Thresholds(0.4, 0.6, 0.8)
        action = b'{"operation":"bounded-test"}'
        other_action = b'{"operation":"other-test"}'
        intent = BoundaryExecutionIntent(
            intent_id="intent-1",
            target_id="repo-1",
            action_digest=hashlib.sha256(action).hexdigest(),
            postcondition_subject="deployment.json",
            postcondition_field="deployment_state",
            required_postcondition_value="required-secret-ready",
        )
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            placement = self.placement(temporary)
            signer, root_public, processes = self.launcher_material(temporary)
            executor = RecordingExecutor()
            with self.launch(
                placement,
                signer,
                root_public,
                processes,
                execution_executor=executor,
            ) as runtime:
                authorization = self.authorize_execution(
                    intent,
                    authorization_id="authorization-1",
                    authorization_nonce="authorization-nonce-0001",
                    expected_latch_head=None,
                )
                with self.assertRaisesRegex(
                    ValueError,
                    "EXECUTION_AUTHORIZATION_QUORUM_NOT_REACHED",
                ):
                    runtime.prepare_execution(authorization[:1])
                with self.assertRaisesRegex(
                    ValueError,
                    "EXECUTION_AUTHORIZATION_QUORUM_NOT_REACHED",
                ):
                    runtime.prepare_execution((authorization[0], authorization[0]))
                other_intent = BoundaryExecutionIntent(
                    intent_id=intent.intent_id,
                    target_id=intent.target_id,
                    action_digest=hashlib.sha256(other_action).hexdigest(),
                    postcondition_subject=intent.postcondition_subject,
                    postcondition_field=intent.postcondition_field,
                    required_postcondition_value=(
                        intent.required_postcondition_value
                    ),
                )
                other_authorization = self.authorize_execution(
                    other_intent,
                    authorization_id="authorization-1",
                    authorization_nonce="authorization-nonce-0001",
                    expected_latch_head=None,
                )
                with self.assertRaisesRegex(
                    ValueError,
                    "EXECUTION_AUTHORIZATION_PAYLOAD_MISMATCH",
                ):
                    runtime.prepare_execution(
                        (authorization[0], other_authorization[1])
                    )
                capability = runtime.prepare_execution(authorization)
                report = runtime.execute_authorized_action(capability, intent, action)
                self.assertEqual(report.intent, intent)
                self.assertIsNone(report.latch_head)
                self.assertEqual(
                    report.authorizer_principal_ids,
                    ("external-authority-a", "external-authority-b"),
                )
                self.assertEqual(report.result, b'{"executed":true}')
                self.assertEqual(
                    report.result_sha256,
                    hashlib.sha256(report.result).hexdigest(),
                )
                self.assertEqual(
                    report.response_integrity_state,
                    ResponseIntegrityState.COMPLETED_UNVERIFIED,
                )
                self.assertEqual(len(executor.calls), 1)
                self.assertEqual(executor.calls[0], (action, report.attempt_id, intent))
                with self.assertRaisesRegex(
                    ValueError,
                    "EXECUTION_CAPABILITY_REUSED",
                ):
                    runtime.execute_authorized_action(capability, intent, action)

                second_authorization = self.authorize_execution(
                    intent,
                    authorization_id="authorization-2",
                    authorization_nonce="authorization-nonce-0002",
                    expected_latch_head=None,
                )
                bound = runtime.prepare_execution(second_authorization)
                with self.assertRaisesRegex(
                    ValueError,
                    "EXECUTION_CAPABILITY_INTENT_MISMATCH",
                ):
                    runtime.execute_authorized_action(bound, other_intent, other_action)
                with self.assertRaisesRegex(
                    ValueError,
                    "EXECUTION_CAPABILITY_REUSED",
                ):
                    runtime.execute_authorized_action(bound, intent, action)

                digest_authorization = self.authorize_execution(
                    intent,
                    authorization_id="authorization-digest",
                    authorization_nonce="authorization-nonce-digest",
                    expected_latch_head=None,
                )
                digest_bound = runtime.prepare_execution(digest_authorization)
                with self.assertRaisesRegex(
                    ValueError,
                    "EXECUTION_ACTION_DIGEST_MISMATCH",
                ):
                    runtime.execute_authorized_action(
                        digest_bound,
                        intent,
                        other_action,
                    )
                self.assertEqual(len(executor.calls), 1)

                third_authorization = self.authorize_execution(
                    intent,
                    authorization_id="authorization-3",
                    authorization_nonce="authorization-nonce-0003",
                    expected_latch_head=None,
                )
                stale = runtime.prepare_execution(third_authorization)
                safe = runtime.assess_axes(
                    target_id="repo-1",
                    axes=(AxisEvidence("scope_escape", 0.1, 1.0, thresholds),),
                    observed_at=self.now,
                )
                self.assertEqual(safe.target_state, TargetBoundaryState.PERMIT)
                self.assertTrue(runtime.external_witness_current)
                with self.assertRaisesRegex(
                    ValueError,
                    "EXECUTION_CAPABILITY_STALE",
                ):
                    runtime.execute_authorized_action(stale, intent, action)

                fourth_authorization = self.authorize_execution(
                    intent,
                    authorization_id="authorization-4",
                    authorization_nonce="authorization-nonce-0004",
                    expected_latch_head=None,
                )
                before_latch = runtime.prepare_execution(fourth_authorization)
                latched = runtime.assess_axes(
                    target_id="repo-1",
                    axes=(AxisEvidence("scope_escape", 0.8, 1.0, thresholds),),
                    observed_at=self.now,
                )
                self.assertEqual(
                    latched.target_state,
                    TargetBoundaryState.IRREVERSIBLE_TRANSITION,
                )
                self.assertFalse(runtime.external_witness_current)
                with self.assertRaisesRegex(
                    ValueError,
                    "EXTERNAL_LATCH_WITNESS_NOT_CURRENT",
                ):
                    runtime.execute_authorized_action(before_latch, intent, action)
                with self.assertRaisesRegex(
                    ValueError,
                    "EXTERNAL_LATCH_WITNESS_NOT_CURRENT",
                ):
                    runtime.prepare_execution(fourth_authorization)

    def test_execution_gate_denies_capability_for_irreversibly_latched_target(
        self,
    ) -> None:
        thresholds = Thresholds(0.4, 0.6, 0.8)
        action = b'{"operation":"post-latch-attempt"}'
        intent = BoundaryExecutionIntent(
            intent_id="intent-post-latch",
            target_id="repo-1",
            action_digest=hashlib.sha256(action).hexdigest(),
            postcondition_subject="deployment.json",
            postcondition_field="deployment_state",
            required_postcondition_value="ready",
        )
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            placement = self.placement(temporary)
            signer, root_public, processes = self.launcher_material(temporary)
            with self.launch(placement, signer, root_public, processes) as runtime:
                latched = runtime.assess_axes(
                    target_id="repo-1",
                    axes=(AxisEvidence("scope_escape", 0.8, 1.0, thresholds),),
                    observed_at=self.now,
                )
                self.assertEqual(
                    latched.target_state,
                    TargetBoundaryState.IRREVERSIBLE_TRANSITION,
                )

            executor = RecordingExecutor()
            with self.launch(
                placement,
                signer,
                root_public,
                processes,
                execution_executor=executor,
            ) as reopened:
                self.assertTrue(reopened.external_witness_current)
                current_head = reopened._latch_store.head()
                authorization = self.authorize_execution(
                    intent,
                    authorization_id="authorization-post-latch",
                    authorization_nonce="authorization-nonce-post-latch",
                    expected_latch_head=current_head,
                )
                with self.assertRaisesRegex(
                    ValueError,
                    "EXECUTION_TARGET_IRREVERSIBLY_LATCHED",
                ):
                    reopened.prepare_execution(authorization)
                self.assertEqual(executor.calls, [])

    def test_execution_gate_enforces_pluggable_hard_invariant_checker(
        self,
    ) -> None:
        action = b'{"operation":"invariant-checked"}'
        other_action = b'{"operation":"invariant-clean"}'
        intent = BoundaryExecutionIntent(
            intent_id="intent-invariant",
            target_id="repo-1",
            action_digest=hashlib.sha256(action).hexdigest(),
            postcondition_subject="deployment.json",
            postcondition_field="deployment_state",
            required_postcondition_value="ready",
        )
        other_intent = BoundaryExecutionIntent(
            intent_id="intent-invariant-clean",
            target_id="repo-1",
            action_digest=hashlib.sha256(other_action).hexdigest(),
            postcondition_subject="deployment.json",
            postcondition_field="deployment_state",
            required_postcondition_value="ready",
        )

        def checker(checked_intent, checked_action):
            if b"invariant-checked" in checked_action:
                return ("SCOPE_ESCAPE",)
            return ()

        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            placement = self.placement(temporary)
            signer, root_public, processes = self.launcher_material(temporary)
            executor = RecordingExecutor()
            with self.launch(
                placement,
                signer,
                root_public,
                processes,
                execution_executor=executor,
                hard_invariant_checker=checker,
            ) as runtime:
                authorization = self.authorize_execution(
                    intent,
                    authorization_id="authorization-invariant",
                    authorization_nonce="authorization-nonce-invariant",
                    expected_latch_head=None,
                )
                capability = runtime.prepare_execution(authorization)
                with self.assertRaisesRegex(
                    ValueError,
                    "EXECUTION_HARD_INVARIANT_VIOLATION:SCOPE_ESCAPE",
                ):
                    runtime.execute_authorized_action(capability, intent, action)
                self.assertEqual(executor.calls, [])

                other_authorization = self.authorize_execution(
                    other_intent,
                    authorization_id="authorization-invariant-clean",
                    authorization_nonce="authorization-nonce-invariant-clean",
                    expected_latch_head=None,
                )
                other_capability = runtime.prepare_execution(other_authorization)
                report = runtime.execute_authorized_action(
                    other_capability, other_intent, other_action
                )
                self.assertEqual(report.intent, other_intent)
                self.assertEqual(len(executor.calls), 1)

    def test_execution_gate_rejects_malformed_hard_invariant_checker_result(
        self,
    ) -> None:
        action = b'{"operation":"malformed-checker"}'
        intent = BoundaryExecutionIntent(
            intent_id="intent-malformed-checker",
            target_id="repo-1",
            action_digest=hashlib.sha256(action).hexdigest(),
            postcondition_subject="deployment.json",
            postcondition_field="deployment_state",
            required_postcondition_value="ready",
        )
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            placement = self.placement(temporary)
            signer, root_public, processes = self.launcher_material(temporary)
            executor = RecordingExecutor()
            with self.launch(
                placement,
                signer,
                root_public,
                processes,
                execution_executor=executor,
                hard_invariant_checker=lambda checked_intent, checked_action: [
                    "NOT_A_TUPLE"
                ],
            ) as runtime:
                authorization = self.authorize_execution(
                    intent,
                    authorization_id="authorization-malformed-checker",
                    authorization_nonce="authorization-nonce-malformed-checker",
                    expected_latch_head=None,
                )
                capability = runtime.prepare_execution(authorization)
                with self.assertRaisesRegex(
                    ValueError,
                    "EXECUTION_HARD_INVARIANT_CHECKER_INVALID",
                ):
                    runtime.execute_authorized_action(capability, intent, action)
                self.assertEqual(executor.calls, [])

    def test_execution_authorization_replay_persists_across_runtime(self) -> None:
        action = b'{"operation":"replay-test"}'
        intent = BoundaryExecutionIntent(
            "intent-replay",
            "repo-1",
            hashlib.sha256(action).hexdigest(),
            "deployment.json",
            "deployment_state",
            "ready",
        )
        authorization = self.authorize_execution(
            intent,
            authorization_id="authorization-replay",
            authorization_nonce="authorization-nonce-replay",
            expected_latch_head=None,
        )
        wrong_head_authorization = self.authorize_execution(
            intent,
            authorization_id="authorization-wrong-head",
            authorization_nonce="authorization-nonce-wrong-head",
            expected_latch_head=self.head_1,
        )
        next_intent = BoundaryExecutionIntent(
            "intent-after-report",
            "repo-1",
            hashlib.sha256(action).hexdigest(),
            "deployment.json",
            "deployment_state",
            "ready",
        )
        next_authorization = self.authorize_execution(
            next_intent,
            authorization_id="authorization-after-report",
            authorization_nonce="authorization-nonce-after-report",
            expected_latch_head=None,
        )
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            placement = self.placement(temporary)
            signer, root_public, processes = self.launcher_material(temporary)
            executor = RecordingExecutor()
            with self.launch(
                placement,
                signer,
                root_public,
                processes,
                execution_executor=executor,
            ) as runtime:
                capability = runtime.prepare_execution(authorization)
                runtime.execute_authorized_action(capability, intent, action)

            reopened_executor = RecordingExecutor()
            with self.launch(
                placement,
                signer,
                root_public,
                processes,
                execution_executor=reopened_executor,
            ) as reopened:
                replay = reopened.prepare_execution(authorization)
                with self.assertRaisesRegex(
                    ValueError,
                    "NONCE_OR_REQUEST_REPLAY",
                ):
                    reopened.execute_authorized_action(replay, intent, action)
                self.assertEqual(reopened_executor.calls, [])
                next_capability = reopened.prepare_execution(next_authorization)
                with self.assertRaisesRegex(
                    ValueError,
                    "EXECUTION_OUTCOME_RECONCILIATION_REQUIRED",
                ):
                    reopened.execute_authorized_action(
                        next_capability,
                        next_intent,
                        action,
                    )
                self.assertEqual(reopened_executor.calls, [])
                with self.assertRaisesRegex(
                    ValueError,
                    "EXECUTION_AUTHORIZATION_STATE_MISMATCH",
                ):
                    reopened.prepare_execution(wrong_head_authorization)

    def test_execution_outcome_unknown_persists_and_blocks_restart(self) -> None:
        action = b'{"operation":"unknown-outcome-test"}'
        intent = BoundaryExecutionIntent(
            "intent-unknown",
            "repo-1",
            hashlib.sha256(action).hexdigest(),
            "deployment.json",
            "deployment_state",
            "ready",
        )
        authorization = self.authorize_execution(
            intent,
            authorization_id="authorization-unknown",
            authorization_nonce="authorization-nonce-unknown",
            expected_latch_head=None,
        )
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            placement = self.placement(temporary)
            signer, root_public, processes = self.launcher_material(temporary)
            failing_executor = RecordingExecutor(error=RuntimeError("effect uncertain"))
            with self.launch(
                placement,
                signer,
                root_public,
                processes,
                execution_executor=failing_executor,
            ) as runtime:
                capability = runtime.prepare_execution(authorization)
                with self.assertRaisesRegex(
                    ValueError,
                    "EXECUTION_OUTCOME_UNKNOWN",
                ):
                    runtime.execute_authorized_action(capability, intent, action)
                self.assertEqual(len(failing_executor.calls), 1)

            next_intent = BoundaryExecutionIntent(
                "intent-after-unknown",
                "repo-1",
                hashlib.sha256(action).hexdigest(),
                "deployment.json",
                "deployment_state",
                "ready",
            )
            next_authorization = self.authorize_execution(
                next_intent,
                authorization_id="authorization-after-unknown",
                authorization_nonce="authorization-nonce-after-unknown",
                expected_latch_head=None,
            )
            reopened_executor = RecordingExecutor()
            with self.launch(
                placement,
                signer,
                root_public,
                processes,
                execution_executor=reopened_executor,
            ) as reopened:
                next_capability = reopened.prepare_execution(next_authorization)
                with self.assertRaisesRegex(
                    ValueError,
                    "EXECUTION_OUTCOME_RECONCILIATION_REQUIRED",
                ):
                    reopened.execute_authorized_action(
                        next_capability,
                        next_intent,
                        action,
                    )
                self.assertEqual(reopened_executor.calls, [])

    def test_launcher_retry_recovers_after_partial_witness_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            placement = self.placement(temporary)
            signer, root_public, processes = self.launcher_material(temporary)
            wrong_second_key_path = temporary / "wrong-private-key.pem"
            wrong_second_key_path.write_bytes(
                self.witness_a2.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.PKCS8,
                    serialization.NoEncryption(),
                )
            )
            wrong_second_key = LatchWitnessProcess(
                processes[1].database_path,
                processes[1].principal_id,
                processes[1].key_id,
                wrong_second_key_path,
            )
            with self.assertRaisesRegex(
                ValueError,
                "LATCH_WITNESS_SERVICE_FAILED",
            ):
                self.launch(
                    placement,
                    signer,
                    root_public,
                    (processes[0], wrong_second_key),
                )
            with self.launch(
                placement,
                signer,
                root_public,
                processes,
            ) as runtime:
                self.assertTrue(runtime.external_witness_current)

    def test_signer_failure_precedes_all_latch_witness_updates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            placement = self.placement(temporary)
            signer_process, root_public, processes = self.launcher_material(
                temporary
            )
            wrong_signer_path = temporary / "wrong-signer-private.pem"
            wrong_signer_path.write_bytes(
                self.witness_a2.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.PKCS8,
                    serialization.NoEncryption(),
                )
            )
            wrong_signer = LatchCheckpointSignerProcess(
                latch_integrity_key_path=(
                    signer_process.latch_integrity_key_path
                ),
                signing_key_id=signer_process.signing_key_id,
                signing_key_path=wrong_signer_path,
                trust_bundle_path=signer_process.trust_bundle_path,
                trust_checkpoint_database_path=(
                    signer_process.trust_checkpoint_database_path
                ),
                trust_checkpoint_attestation_paths=(
                    signer_process.trust_checkpoint_attestation_paths
                ),
            )
            with self.assertRaisesRegex(
                ValueError,
                "LATCH_CHECKPOINT_SIGNER_SERVICE_FAILED",
            ):
                self.launch(
                    placement,
                    wrong_signer,
                    root_public,
                    processes,
                )
            self.assertTrue(
                all(not process.database_path.exists() for process in processes)
            )


if __name__ == "__main__":
    unittest.main()
