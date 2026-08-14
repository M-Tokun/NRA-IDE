import json
import subprocess
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from note.poc_horizontal_ai.safety_kernel import (
    ActionProposal,
    ActionType,
    AppendOnlyHistoryLedger,
    AuthoritativeEvidence,
    ChangeKind,
    EffectClass,
    EvidenceQuality,
    ExecutionDirective,
    ExecutionEnvironment,
    FileChangeFact,
    FileChangeFactType,
    FileChangeThicknessContract,
    FileChangeThicknessModel,
    FileChangePolicy,
    HistoryEventKind,
    ObservationRequest,
    InstructionContract,
    ShadowSafetyKernel,
    SolutionStage,
    TargetBoundaryState,
    ThicknessEvaluationStatus,
    ThicknessTrendState,
    Thresholds,
    append_file_change_fact,
    create_audit_bundle,
    encode_observation_request,
    measure_proposal_fact,
    serve_observation_request,
    verify_audit_bundle,
    verify_observation_envelope,
)


class FileChangeThicknessModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = AppendOnlyHistoryLedger()
        self.contract = FileChangeThicknessContract(
            target_id="repo-1",
            axis_id="review_capacity",
            model_version="bounded-file-change/1.0",
            unit="review-unit",
            line_cost=0.5,
            file_overhead=5.0,
            reserve_units=10.0,
            step_loss_units=20.0,
            thresholds=Thresholds(0.4, 0.6, 0.8),
            trusted_source_ids=("observer-v1", "decoder-v1", "reconciler-v1"),
        )
        self.model = FileChangeThicknessModel(self.contract)
        self.sequence = 0

    def append(self, fact: FileChangeFact, source: str) -> None:
        self.sequence += 1
        append_file_change_fact(
            self.ledger,
            event_id=f"event-{self.sequence}",
            target_id="repo-1",
            source_id=source,
            occurred_at=f"2026-08-13T00:00:{self.sequence:02d}+00:00",
            fact=fact,
        )

    def test_history_converts_to_delta_tau_without_double_counting(self) -> None:
        self.append(
            FileChangeFact(
                FileChangeFactType.CAPACITY_BASELINE,
                capacity_units=100.0,
            ),
            "observer-v1",
        )
        self.append(
            FileChangeFact(
                FileChangeFactType.CHANGE_PROPOSED,
                request_id="change-1",
                changed_lines=60,
                files_touched=1,
            ),
            "decoder-v1",
        )
        self.append(
            FileChangeFact(FileChangeFactType.THICKNESS_LOSS, units=10.0),
            "observer-v1",
        )
        result = self.model.evaluate(self.ledger.events)
        self.assertEqual(result.status, ThicknessEvaluationStatus.VALID)
        assert result.estimate is not None
        assert result.conservative_axis is not None
        self.assertEqual(result.estimate.delta_upper, 35.0)
        self.assertEqual(result.estimate.tau_lower, 80.0)
        self.assertEqual(result.estimate.trend, ThicknessTrendState.DEPLETING)
        self.assertEqual(
            result.conservative_axis.delta / result.conservative_axis.tau,
            0.4375,
        )

    def test_second_baseline_cannot_erase_pending_change_or_loss(self) -> None:
        self.append(
            FileChangeFact(
                FileChangeFactType.CAPACITY_BASELINE,
                capacity_units=100.0,
            ),
            "observer-v1",
        )
        self.append(
            FileChangeFact(
                FileChangeFactType.CHANGE_PROPOSED,
                request_id="change-1",
                changed_lines=10,
                files_touched=1,
            ),
            "decoder-v1",
        )
        self.append(
            FileChangeFact(FileChangeFactType.THICKNESS_LOSS, units=20.0),
            "observer-v1",
        )
        self.append(
            FileChangeFact(
                FileChangeFactType.CAPACITY_BASELINE,
                capacity_units=100.0,
            ),
            "observer-v1",
        )

        result = self.model.evaluate(self.ledger.events)

        self.assertEqual(
            result.status,
            ThicknessEvaluationStatus.INPUT_EXCEPTION,
        )
        self.assertIsNone(result.estimate)
        self.assertIn(
            "FILE_CHANGE_HISTORY_INVALID:ValueError",
            result.reason_codes,
        )

    def test_proposal_measurement_comes_from_diff_not_numeric_claim(self) -> None:
        fact = measure_proposal_fact(
            ActionProposal(
                "1.0",
                ActionType.PROPOSE_PATCH,
                ChangeKind.MODIFY,
                "src/example.py",
                (
                    "--- a/src/example.py\n"
                    "+++ b/src/example.py\n"
                    "@@ -1,2 +1,3 @@\n"
                    "-old\n"
                    "+new\n"
                    "+added\n"
                    " context\n"
                ),
                1,
                "a" * 64,
                "measured-request-1",
                ExecutionEnvironment.WORKTREE,
                EffectClass.E1_REVERSIBLE,
            )
        )
        self.assertEqual(fact.request_id, "measured-request-1")
        self.assertEqual(fact.changed_lines, 3)
        self.assertEqual(fact.files_touched, 1)

    def test_step_loss_can_jump_to_irreversible_transition(self) -> None:
        self.append(
            FileChangeFact(
                FileChangeFactType.CAPACITY_BASELINE,
                capacity_units=100.0,
            ),
            "observer-v1",
        )
        self.append(
            FileChangeFact(
                FileChangeFactType.CHANGE_PROPOSED,
                request_id="change-1",
                changed_lines=80,
                files_touched=1,
            ),
            "decoder-v1",
        )
        self.append(
            FileChangeFact(FileChangeFactType.THICKNESS_LOSS, units=35.0),
            "observer-v1",
        )
        result = self.model.evaluate(self.ledger.events)
        assert result.estimate is not None
        assert result.conservative_axis is not None
        self.assertEqual(result.estimate.trend, ThicknessTrendState.STEP_LOSS)
        from note.poc_horizontal_ai.safety_kernel import evaluate_axes

        boundary = evaluate_axes((result.conservative_axis,))
        self.assertEqual(
            boundary.target_state,
            TargetBoundaryState.IRREVERSIBLE_TRANSITION,
        )

        policy = FileChangePolicy(Path.cwd() / "shadow-domain-stage-root")
        resource_path = "src/example.py"
        base_hash = "a" * 64
        decision = ShadowSafetyKernel(policy).evaluate(
            ActionProposal(
                "1.0",
                ActionType.PROPOSE_PATCH,
                ChangeKind.MODIFY,
                resource_path,
                (
                    "--- a/src/example.py\n"
                    "+++ b/src/example.py\n"
                    "@@ -1 +1 @@\n-old\n+new\n"
                ),
                1,
                base_hash,
                "domain-request-0001",
                ExecutionEnvironment.WORKTREE,
                EffectClass.E1_REVERSIBLE,
            ),
            AuthoritativeEvidence(
                EvidenceQuality.VERIFIED,
                1,
                resource_path,
                policy.resolve_target(resource_path),
                True,
                False,
                base_hash,
            ),
            instruction_contract=InstructionContract(
                "bounded file change",
                (ActionType.PROPOSE_PATCH,),
                (ChangeKind.MODIFY,),
                ("src",),
                ExecutionEnvironment.WORKTREE,
                EffectClass.E1_REVERSIBLE,
                True,
            ),
            solution_stage=SolutionStage.COMPLETE,
            thickness=result,
        )
        self.assertEqual(
            decision.target_boundary_state,
            TargetBoundaryState.IRREVERSIBLE_TRANSITION,
        )
        self.assertEqual(decision.directives.execution, ExecutionDirective.DENY)

    def test_only_verified_reconciliation_removes_pending_delta(self) -> None:
        self.append(
            FileChangeFact(
                FileChangeFactType.CAPACITY_BASELINE,
                capacity_units=100.0,
            ),
            "observer-v1",
        )
        self.append(
            FileChangeFact(
                FileChangeFactType.CHANGE_PROPOSED,
                request_id="change-1",
                changed_lines=10,
                files_touched=1,
            ),
            "decoder-v1",
        )
        self.append(
            FileChangeFact(
                FileChangeFactType.CHANGE_RESOLVED,
                request_id="change-1",
            ),
            "reconciler-v1",
        )
        result = self.model.evaluate(self.ledger.events)
        assert result.estimate is not None
        self.assertEqual(result.estimate.delta_upper, 0.0)

    def test_untrusted_fact_source_is_input_exception(self) -> None:
        self.append(
            FileChangeFact(
                FileChangeFactType.CAPACITY_BASELINE,
                capacity_units=100.0,
            ),
            "ai-self-report",
        )
        result = self.model.evaluate(self.ledger.events)
        self.assertEqual(result.status, ThicknessEvaluationStatus.INPUT_EXCEPTION)

    def test_contract_rejects_boolean_numeric_configuration(self) -> None:
        with self.assertRaises(ValueError):
            FileChangeThicknessContract(
                target_id="repo-1",
                axis_id="review_capacity",
                model_version="bounded-file-change/1.0",
                unit="review-unit",
                line_cost=True,
                file_overhead=5.0,
                reserve_units=10.0,
                step_loss_units=20.0,
                thresholds=Thresholds(0.4, 0.6, 0.8),
                trusted_source_ids=("observer-v1",),
            )


class ObserverProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime.now(timezone.utc)
        self.request = ObservationRequest(
            request_id="observation-1",
            nonce="0123456789abcdef0123456789abcdef",
            resource_path="AGENTS.md",
            state_version=12,
            issued_at=self.now - timedelta(seconds=1),
        )

    def test_request_round_trip_has_fresh_corresponding_evidence(self) -> None:
        request_json = encode_observation_request(self.request)
        envelope = serve_observation_request(
            request_json,
            repository_root=Path.cwd(),
            observer_id="observer-process-v1",
        )
        result = verify_observation_envelope(
            envelope,
            request=self.request,
            repository_root=Path.cwd(),
            expected_observer_id="observer-process-v1",
            max_age=timedelta(seconds=5),
            now=self.now + timedelta(seconds=1),
        )
        self.assertEqual(result.reason_codes, ())
        self.assertIsNotNone(result.evidence)

    def test_observer_service_runs_across_process_boundary(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "note.poc_horizontal_ai.safety_kernel.observer_service",
                "--repository-root",
                str(Path.cwd()),
                "--observer-id",
                "observer-process-v1",
            ],
            input=encode_observation_request(self.request),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = verify_observation_envelope(
            completed.stdout,
            request=self.request,
            repository_root=Path.cwd(),
            expected_observer_id="observer-process-v1",
            max_age=timedelta(seconds=5),
            now=datetime.now(timezone.utc),
        )
        self.assertEqual(result.reason_codes, ())

    def test_tampered_envelope_is_rejected(self) -> None:
        envelope = json.loads(
            serve_observation_request(
                encode_observation_request(self.request),
                repository_root=Path.cwd(),
                observer_id="observer-process-v1",
            )
        )
        envelope["evidence"]["state_version"] = 99
        result = verify_observation_envelope(
            json.dumps(envelope),
            request=self.request,
            repository_root=Path.cwd(),
            expected_observer_id="observer-process-v1",
            max_age=timedelta(seconds=5),
            now=datetime.now(timezone.utc),
        )
        self.assertIsNone(result.evidence)
        self.assertIn("OBSERVER_STATE_VERSION_MISMATCH", result.reason_codes)
        self.assertIn("OBSERVER_SNAPSHOT_DIGEST_MISMATCH", result.reason_codes)

    def test_request_rejects_path_traversal(self) -> None:
        invalid = ObservationRequest(
            request_id="observation-2",
            nonce="0123456789abcdef0123456789abcdef",
            resource_path="../outside.txt",
            state_version=1,
            issued_at=self.now,
        )
        with self.assertRaises(ValueError):
            encode_observation_request(invalid)


class AuditBundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = AppendOnlyHistoryLedger()
        self.ledger.append(
            event_id="event-1",
            kind=HistoryEventKind.OBSERVATION,
            target_id="repo-1",
            source_id="observer-v1",
            occurred_at="2026-08-13T00:00:00+00:00",
            payload={"state": "observed"},
        )

    def test_bundle_round_trip_and_external_anchor(self) -> None:
        head = self.ledger.events[-1].digest
        bundle = create_audit_bundle(
            self.ledger.events,
            exported_at=datetime.now(timezone.utc),
        )
        result = verify_audit_bundle(bundle, expected_head_digest=head)
        self.assertEqual(result.reason_codes, ())
        self.assertEqual(result.events, self.ledger.events)
        wrong_anchor = verify_audit_bundle(bundle, expected_head_digest="0" * 64)
        self.assertEqual(
            wrong_anchor.reason_codes,
            ("AUDIT_EXTERNAL_ANCHOR_MISMATCH",),
        )

    def test_bundle_record_tampering_is_detected(self) -> None:
        bundle = json.loads(
            create_audit_bundle(
                self.ledger.events,
                exported_at=datetime.now(timezone.utc),
            )
        )
        bundle["records_jsonl"] = bundle["records_jsonl"].replace(
            "observed",
            "changed",
        )
        result = verify_audit_bundle(json.dumps(bundle))
        self.assertEqual(
            result.reason_codes,
            ("AUDIT_RECORDS_DIGEST_MISMATCH",),
        )
if __name__ == "__main__":
    unittest.main()
