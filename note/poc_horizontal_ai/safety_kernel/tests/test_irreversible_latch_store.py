import json
import shutil
import sqlite3
import tempfile
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from note.poc_horizontal_ai.safety_kernel import (
    AxisEvidence,
    InputExceptionState,
    TargetBoundaryState,
    Thresholds,
)
from note.poc_horizontal_ai.trusted_runtime import (
    AdmittedBoundaryRuntime,
    ExternalLatchWitnessEvidence,
    KeyRole,
    RuntimePlacement,
    TrustedKeySpec,
    admit_boundary_runtime,
    create_boundary_admission_challenge,
    create_latch_witness_attestation,
    create_signed_latch_genesis,
    create_signed_trust_bundle,
    verify_signed_trust_bundle,
)
from note.poc_horizontal_ai.trusted_runtime.irreversible_latch_store import (
    PersistentIrreversibleLatchStore,
)


class PersistentIrreversibleLatchStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.key = b"L" * 32
        self.now = datetime.now(timezone.utc)
        self.thresholds = Thresholds(0.4, 0.6, 0.8)

    def axis(self, ratio: float, **changes: object) -> AxisEvidence:
        values = {
            "name": "scope_escape",
            "delta": ratio,
            "tau": 1.0,
            "thresholds": self.thresholds,
            "verified": True,
            "irreversible_latched": False,
        }
        values.update(changes)
        return AxisEvidence(**values)

    def test_latch_survives_reopen_and_cannot_be_cleared_by_caller(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "latch.sqlite3"
            with PersistentIrreversibleLatchStore(database, self.key) as store:
                crossed = store.assess_axes(
                    target_id="repo-1",
                    axes=(self.axis(0.8),),
                    observed_at=self.now,
                )
                self.assertEqual(
                    crossed.target_state,
                    TargetBoundaryState.IRREVERSIBLE_TRANSITION,
                )
                self.assertEqual(store.verify(), ())

            with PersistentIrreversibleLatchStore(database, self.key) as reopened:
                retained = reopened.assess_axes(
                    target_id="repo-1",
                    axes=(self.axis(0.1, irreversible_latched=False),),
                    observed_at=self.now,
                )
                self.assertEqual(
                    retained.target_state,
                    TargetBoundaryState.IRREVERSIBLE_TRANSITION,
                )
                self.assertTrue(retained.irreversible_latched)

    def test_caller_flag_cannot_create_a_trusted_latch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "latch.sqlite3"
            with PersistentIrreversibleLatchStore(database, self.key) as store:
                result = store.assess_axes(
                    target_id="repo-1",
                    axes=(self.axis(0.1, irreversible_latched=True),),
                    observed_at=self.now,
                )
                self.assertEqual(result.target_state, TargetBoundaryState.PERMIT)
                self.assertFalse(result.irreversible_latched)

                invalid = store.assess_axes(
                    target_id="repo-1",
                    axes=(self.axis(0.1, irreversible_latched="yes"),),
                    observed_at=self.now,
                )
                self.assertEqual(
                    invalid.input_exception,
                    InputExceptionState.CONFESSION,
                )
                self.assertIsNone(invalid.target_state)

    def test_latch_is_isolated_by_target_and_axis(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "latch.sqlite3"
            with PersistentIrreversibleLatchStore(database, self.key) as store:
                store.assess_axes(
                    target_id="repo-1",
                    axes=(self.axis(1.0),),
                    observed_at=self.now,
                )
                other_target = store.assess_axes(
                    target_id="repo-2",
                    axes=(self.axis(0.1),),
                    observed_at=self.now,
                )
                other_axis = store.assess_axes(
                    target_id="repo-1",
                    axes=(self.axis(0.1, name="secret_exposure"),),
                    observed_at=self.now,
                )
                self.assertEqual(
                    other_target.target_state,
                    TargetBoundaryState.PERMIT,
                )
                self.assertEqual(
                    other_axis.target_state,
                    TargetBoundaryState.PERMIT,
                )

    def test_corrupt_latch_chain_cannot_be_reopened(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "latch.sqlite3"
            with PersistentIrreversibleLatchStore(database, self.key) as store:
                store.assess_axes(
                    target_id="repo-1",
                    axes=(self.axis(0.8),),
                    observed_at=self.now,
                )
            connection = sqlite3.connect(database)
            connection.execute("DROP TRIGGER irreversible_latch_no_update")
            connection.execute(
                "UPDATE irreversible_latch SET axis_name = ? WHERE sequence = 1",
                ("tampered",),
            )
            connection.commit()
            connection.close()

            with self.assertRaisesRegex(
                ValueError,
                "IRREVERSIBLE_LATCH_CHAIN_INVALID",
            ):
                PersistentIrreversibleLatchStore(database, self.key)


class BoundaryRuntimeAdmissionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.key = b"G" * 32
        self.now = datetime.now(timezone.utc)
        self.thresholds = Thresholds(0.4, 0.6, 0.8)
        self.root = Ed25519PrivateKey.generate()
        self.checkpoint_signer = Ed25519PrivateKey.generate()
        self.witness_a = Ed25519PrivateKey.generate()
        self.witness_b = Ed25519PrivateKey.generate()
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
                        "witness-a",
                        "principal-a",
                        KeyRole.WITNESS_SIGNER,
                        self.witness_a,
                    ),
                    (
                        "witness-b",
                        "principal-b",
                        KeyRole.WITNESS_SIGNER,
                        self.witness_b,
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

    def admit_runtime(self, **kwargs: object) -> AdmittedBoundaryRuntime:
        return admit_boundary_runtime(
            pinned_root_keys={"offline-root-v1": self.root.public_key()},
            trust_bundle_signature_max_age=timedelta(seconds=5),
            **kwargs,
        )

    def admit_new(
        self,
        placement: RuntimePlacement,
    ) -> AdmittedBoundaryRuntime:
        challenge = create_boundary_admission_challenge()
        evidence = self.genesis_evidence(challenge)
        return self.admit_runtime(
            placement=placement,
            latch_integrity_key=self.key,
            latch_store_id="repo-latch-v1",
            admission_challenge=challenge,
            external_witness_evidence=evidence,
            now=self.now,
        )

    def genesis_evidence(
        self,
        challenge,
        *,
        signed_trust_bundle_json: str | None = None,
    ) -> ExternalLatchWitnessEvidence:
        checkpoint = create_signed_latch_genesis(
            checkpoint_id="repo-latch-genesis",
            latch_store_id="repo-latch-v1",
            signing_key_id="latch-checkpoint-v1",
            signing_private_key=self.checkpoint_signer,
            trust_bundle=self.bundle,
            checkpointed_at=self.now,
        )
        attestations = tuple(
            create_latch_witness_attestation(
                checkpoint,
                attestation_id=f"genesis-{principal_id}",
                witness_principal_id=principal_id,
                witness_sequence=1,
                witness_key_id=key_id,
                witness_private_key=private_key,
                trust_bundle=self.bundle,
                checkpoint_signature_max_age=timedelta(seconds=5),
                witnessed_at=self.now,
                admission_challenge=challenge.nonce,
            )
            for principal_id, key_id, private_key in (
                ("principal-a", "witness-a", self.witness_a),
                ("principal-b", "witness-b", self.witness_b),
            )
        )
        return ExternalLatchWitnessEvidence(
            signed_trust_bundle_json=(
                self.signed_bundle
                if signed_trust_bundle_json is None
                else signed_trust_bundle_json
            ),
            signed_latch_checkpoint_json=checkpoint,
            signed_witness_attestations=attestations,
            minimum_principals=2,
            signature_max_age=timedelta(seconds=5),
        )

    def placement(
        self,
        directory: Path,
        *,
        latch_database_path: Path | None = None,
        nonce_database_path: Path | None = None,
    ) -> RuntimePlacement:
        private_key = directory / "boundary-private.key"
        private_key.write_bytes(b"not-used-by-boundary-runtime")
        witness_a = directory / "witness-a"
        witness_b = directory / "witness-b"
        witness_a.mkdir()
        witness_b.mkdir()
        return RuntimePlacement(
            repository_root=Path.cwd(),
            private_key_path=private_key,
            nonce_database_path=(
                nonce_database_path or directory / "nonce.sqlite3"
            ),
            anchor_database_path=directory / "anchor.sqlite3",
            latch_database_path=(
                latch_database_path or directory / "latch.sqlite3"
            ),
            witness_roots=(witness_a, witness_b),
        )

    def axis(self, ratio: float) -> AxisEvidence:
        return AxisEvidence(
            "scope_escape",
            ratio,
            1.0,
            self.thresholds,
        )

    def test_admitted_runtime_is_the_persistent_assessment_entry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            placement = self.placement(temporary)
            with self.admit_new(placement) as runtime:
                self.assertTrue(runtime.deployment_assessment.path_separated)
                self.assertIn(
                    "OS_IDENTITY_SEPARATION_NOT_ATTESTED",
                    runtime.deployment_assessment.reason_codes,
                )
                crossed = runtime.assess_axes(
                    target_id="repo-1",
                    axes=(self.axis(0.8),),
                    observed_at=self.now,
                )
                self.assertEqual(
                    crossed.target_state,
                    TargetBoundaryState.IRREVERSIBLE_TRANSITION,
                )

            with self.assertRaisesRegex(
                ValueError,
                "LATCH_EXTERNAL_WITNESS_REQUIRED",
            ):
                self.admit_runtime(
                    placement=placement,
                    latch_integrity_key=self.key,
                    latch_store_id="repo-latch-v1",
                    admission_challenge=create_boundary_admission_challenge(),
                )

    def test_trust_bundle_is_reverified_before_local_state_creation(self) -> None:
        invalid_cases = (
            (
                "tampered-signature",
                self.signed_bundle.replace('"payload_json":"', '"payload_json":"x', 1),
                {"offline-root-v1": self.root.public_key()},
                self.now,
            ),
            (
                "wrong-pinned-root",
                self.signed_bundle,
                {"offline-root-v1": Ed25519PrivateKey.generate().public_key()},
                self.now,
            ),
            (
                "expired-bundle",
                self.signed_bundle,
                {"offline-root-v1": self.root.public_key()},
                self.now + timedelta(seconds=6),
            ),
        )
        for case_name, signed_bundle, pinned_roots, admission_time in invalid_cases:
            with self.subTest(case_name), tempfile.TemporaryDirectory() as directory:
                placement = self.placement(Path(directory))
                challenge = create_boundary_admission_challenge()
                evidence = self.genesis_evidence(
                    challenge,
                    signed_trust_bundle_json=signed_bundle,
                )
                with self.assertRaises(ValueError):
                    admit_boundary_runtime(
                        placement=placement,
                        latch_integrity_key=self.key,
                        latch_store_id="repo-latch-v1",
                        admission_challenge=challenge,
                        external_witness_evidence=evidence,
                        pinned_root_keys=pinned_roots,
                        trust_bundle_signature_max_age=timedelta(seconds=5),
                        now=admission_time,
                    )
                self.assertFalse(placement.latch_database_path.exists())
                for witness_root in placement.witness_roots:
                    self.assertEqual(tuple(witness_root.iterdir()), ())

    def test_runtime_constructor_cannot_bypass_admission(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "must be created by admission",
        ):
            AdmittedBoundaryRuntime(
                placement=None,
                deployment_assessment=None,
                latch_store=None,
                checkpoint_stores=(),
                latch_store_id="repo-latch-v1",
                external_witness_current=False,
            )

    def test_invalid_latch_placement_is_rejected_before_store_creation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            inside_repository = Path.cwd() / "forbidden-latch.sqlite3"
            placement = self.placement(
                temporary,
                latch_database_path=inside_repository,
            )
            with self.assertRaisesRegex(
                ValueError,
                "PLACEMENT_INSIDE_REPOSITORY",
            ):
                self.admit_runtime(
                    placement=placement,
                    latch_integrity_key=self.key,
                    latch_store_id="repo-latch-v1",
                )
            self.assertFalse(inside_repository.exists())

    def test_latch_database_cannot_reuse_another_runtime_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            reused = temporary / "shared.sqlite3"
            placement = self.placement(
                temporary,
                latch_database_path=reused,
                nonce_database_path=reused,
            )
            with self.assertRaisesRegex(ValueError, "PLACEMENT_PATH_REUSED"):
                self.admit_runtime(
                    placement=placement,
                    latch_integrity_key=self.key,
                    latch_store_id="repo-latch-v1",
                )
            self.assertFalse(reused.exists())

    def test_latch_database_cannot_be_placed_inside_witness_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            placement = self.placement(temporary)
            overlapping = replace(
                placement,
                latch_database_path=(
                    placement.witness_roots[0] / "latch.sqlite3"
                ),
            )
            with self.assertRaisesRegex(
                ValueError,
                "PLACEMENT_WITNESS_RUNTIME_PATH_OVERLAP",
            ):
                self.admit_runtime(
                    placement=overlapping,
                    latch_integrity_key=self.key,
                    latch_store_id="repo-latch-v1",
                    now=self.now,
                )

    def test_witness_checkpoint_rejects_database_rollback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            placement = self.placement(temporary)
            baseline = temporary / "empty-latch-baseline.sqlite3"
            with self.admit_new(placement):
                pass
            shutil.copy2(placement.latch_database_path, baseline)

            with self.admit_new(placement) as runtime:
                runtime.assess_axes(
                    target_id="repo-1",
                    axes=(self.axis(0.8),),
                    observed_at=self.now,
                )
            for root in placement.witness_roots:
                self.assertEqual(
                    len(tuple(root.glob("latch-head-*.json"))),
                    1,
                )

            shutil.copy2(baseline, placement.latch_database_path)
            with self.assertRaisesRegex(
                ValueError,
                "IRREVERSIBLE_LATCH_ROLLBACK",
            ):
                self.admit_runtime(
                    placement=placement,
                    latch_integrity_key=self.key,
                    latch_store_id="repo-latch-v1",
                    admission_challenge=create_boundary_admission_challenge(),
                    now=self.now,
                )

    def test_checkpoint_accepts_one_observation_latching_multiple_axes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            placement = self.placement(temporary)
            with self.admit_new(placement) as runtime:
                runtime.assess_axes(
                    target_id="repo-1",
                    axes=(
                        self.axis(0.8),
                        AxisEvidence(
                            "secret_exposure",
                            0.9,
                            1.0,
                            self.thresholds,
                        ),
                    ),
                    observed_at=self.now,
                )
            for root in placement.witness_roots:
                names = tuple(path.name for path in root.glob("latch-head-*.json"))
                self.assertEqual(names, ("latch-head-00000000000000000002.json",))

            with self.assertRaisesRegex(
                ValueError,
                "LATCH_EXTERNAL_WITNESS_REQUIRED",
            ):
                self.admit_runtime(
                    placement=placement,
                    latch_integrity_key=self.key,
                    latch_store_id="repo-latch-v1",
                    admission_challenge=create_boundary_admission_challenge(),
                    now=self.now,
                )

    def test_tampered_witness_checkpoint_blocks_admission(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            placement = self.placement(temporary)
            with self.admit_new(placement) as runtime:
                runtime.assess_axes(
                    target_id="repo-1",
                    axes=(self.axis(0.8),),
                    observed_at=self.now,
                )
            checkpoint = next(
                placement.witness_roots[0].glob("latch-head-*.json")
            )
            data = json.loads(checkpoint.read_text(encoding="utf-8"))
            data["row_mac"] = "0" * 64
            checkpoint.write_text(json.dumps(data), encoding="utf-8")

            with self.assertRaisesRegex(
                ValueError,
                "LATCH_CHECKPOINT_INVALID",
            ):
                self.admit_runtime(
                    placement=placement,
                    latch_integrity_key=self.key,
                    latch_store_id="repo-latch-v1",
                    admission_challenge=create_boundary_admission_challenge(),
                    now=self.now,
                )


if __name__ == "__main__":
    unittest.main()
