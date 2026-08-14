import json
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

from note.poc_horizontal_ai.safety_kernel import (
    ActionProposal,
    ActionType,
    AppendOnlyHistoryLedger,
    AuditDirective,
    AuthoritativeEvidence,
    ChangeKind,
    EffectClass,
    EvidenceQuality,
    ExecutionDirective,
    ExecutionEnvironment,
    FileChangePolicy,
    HistoryEventKind,
    InstructionContract,
    RealityObservation,
    RealizationStage,
    ReconciliationState,
    ReportClaim,
    ResponseEvent,
    ResponseEventType,
    ResponseIntegrityState,
    ShadowReplayCase,
    ShadowSafetyKernel,
    SolutionStage,
    ThicknessEstimate,
    ThicknessEvaluation,
    ThicknessEvaluationStatus,
    ThicknessTrendState,
    Thresholds,
    TrustedFileObserver,
    assess_response_integrity,
    decision_digest,
    decode_action_proposal,
    evaluate_thickness_estimate,
    reconcile_report,
    replay_shadow_decision,
)


class DecoderTests(unittest.TestCase):
    def valid_data(self) -> dict[str, object]:
        return {
            "schema_version": "1.0",
            "action_type": "PROPOSE_PATCH",
            "change_kind": "MODIFY",
            "resource_path": "src/example.py",
            "patch": (
                "--- a/src/example.py\n"
                "+++ b/src/example.py\n"
                "@@ -1 +1 @@\n-old\n+new\n"
            ),
            "state_version": 7,
            "base_sha256": "a" * 64,
            "idempotency_key": "request-0001",
            "environment": "WORKTREE",
            "effect_class": "E1_REVERSIBLE",
        }

    def test_strict_decoder_accepts_only_closed_contract(self) -> None:
        result = decode_action_proposal(json.dumps(self.valid_data()))
        self.assertIsNotNone(result.proposal)
        self.assertEqual(result.reason_codes, ())

        unknown = self.valid_data()
        unknown["permit"] = True
        self.assertEqual(
            decode_action_proposal(json.dumps(unknown)).reason_codes,
            ("UNKNOWN_FIELDS",),
        )

    def test_decoder_rejects_duplicate_fields_and_bool_as_int(self) -> None:
        duplicate = (
            '{"schema_version":"1.0","schema_version":"2.0"}'
        )
        self.assertEqual(
            decode_action_proposal(duplicate).reason_codes,
            ("DUPLICATE_FIELD",),
        )
        data = self.valid_data()
        data["state_version"] = True
        self.assertEqual(
            decode_action_proposal(json.dumps(data)).reason_codes,
            ("INVALID_STATE_VERSION_TYPE",),
        )


class HistoryAndReconciliationTests(unittest.TestCase):
    def test_append_only_chain_detects_tampering(self) -> None:
        ledger = AppendOnlyHistoryLedger()
        ledger.append(
            event_id="obs-1",
            kind=HistoryEventKind.OBSERVATION,
            target_id="target-1",
            source_id="sensor-1",
            occurred_at="2026-08-13T00:00:00+00:00",
            payload={"field": "tau", "value": 10, "unit": "mm"},
        )
        ledger.append(
            event_id="report-1",
            kind=HistoryEventKind.REPORT,
            target_id="target-1",
            source_id="operator-1",
            occurred_at="2026-08-13T00:01:00+00:00",
            payload={"claim": "stable"},
        )
        self.assertTrue(AppendOnlyHistoryLedger.verify(ledger.events))
        tampered = (
            ledger.events[0],
            replace(ledger.events[1], payload_json='{"claim":"changed"}'),
        )
        self.assertFalse(AppendOnlyHistoryLedger.verify(tampered))

    def test_report_is_checked_against_later_reality(self) -> None:
        now = datetime(2026, 8, 13, tzinfo=timezone.utc)
        report = ReportClaim("r1", "t1", "repaired", "true", now)
        reality = RealityObservation(
            "o1",
            "t1",
            "repaired",
            "false",
            now + timedelta(seconds=1),
            EvidenceQuality.VERIFIED,
        )
        result = reconcile_report(report, reality)
        self.assertEqual(result.state, ReconciliationState.CONFLICT)


class ObserverAndResponseIntegrityTests(unittest.TestCase):
    def test_observer_reads_repository_state_without_ai_claimed_hash(self) -> None:
        observer = TrustedFileObserver(Path.cwd(), "repo-observer-v1")
        result = observer.observe("AGENTS.md", 11)
        self.assertEqual(result.reason_codes, ())
        self.assertIsNotNone(result.evidence)
        assert result.evidence is not None
        self.assertTrue(result.evidence.target_exists)
        self.assertEqual(result.evidence.state_version, 11)
        self.assertEqual(len(result.evidence.current_sha256 or ""), 64)
        self.assertEqual(len(result.evidence.snapshot_digest), 64)

    def test_observer_rejects_scope_escape(self) -> None:
        observer = TrustedFileObserver(Path.cwd(), "repo-observer-v1")
        result = observer.observe("../outside.txt", 1)
        self.assertIsNone(result.evidence)
        self.assertEqual(result.reason_codes, ("INVALID_OBSERVATION_REQUEST",))

    def test_completed_response_needs_reality_match(self) -> None:
        event = ResponseEvent(
            "event-1",
            "target-1",
            "warning-1",
            ResponseEventType.ACTION_COMPLETED,
            "operator-1",
            datetime(2026, 8, 13, tzinfo=timezone.utc),
        )
        self.assertEqual(
            assess_response_integrity((event,), ReconciliationState.CONFLICT),
            ResponseIntegrityState.COMPLETED_UNVERIFIED,
        )
        self.assertEqual(
            assess_response_integrity((event,), ReconciliationState.MATCHED),
            ResponseIntegrityState.VERIFIED_RESOLVED,
        )

    def test_response_history_rejects_mixed_targets(self) -> None:
        occurred_at = datetime(2026, 8, 13, tzinfo=timezone.utc)
        events = (
            ResponseEvent(
                "event-1",
                "target-1",
                "warning-1",
                ResponseEventType.RECURRENCE,
                "operator-1",
                occurred_at,
                sequence=1,
            ),
            ResponseEvent(
                "event-2",
                "target-2",
                "warning-2",
                ResponseEventType.ACTION_COMPLETED,
                "operator-1",
                occurred_at,
                sequence=2,
            ),
        )
        self.assertEqual(
            assess_response_integrity(events, ReconciliationState.MATCHED),
            ResponseIntegrityState.INPUT_EXCEPTION,
        )

    def test_sequence_makes_equal_timestamp_order_deterministic(self) -> None:
        occurred_at = datetime(2026, 8, 13, tzinfo=timezone.utc)
        completed = ResponseEvent(
            "event-1",
            "target-1",
            "warning-1",
            ResponseEventType.ACTION_COMPLETED,
            "operator-1",
            occurred_at,
            sequence=1,
        )
        recurrence = ResponseEvent(
            "event-2",
            "target-1",
            "warning-1",
            ResponseEventType.RECURRENCE,
            "observer-1",
            occurred_at,
            sequence=2,
        )
        for events in ((completed, recurrence), (recurrence, completed)):
            self.assertEqual(
                assess_response_integrity(
                    events,
                    ReconciliationState.MATCHED,
                ),
                ResponseIntegrityState.RECURRENT,
            )

    def test_expired_completion_is_not_verified_resolution(self) -> None:
        occurred_at = datetime(2026, 8, 13, tzinfo=timezone.utc)
        event = ResponseEvent(
            "event-1",
            "target-1",
            "warning-1",
            ResponseEventType.ACTION_COMPLETED,
            "operator-1",
            occurred_at,
            expires_at=occurred_at + timedelta(minutes=5),
        )
        self.assertEqual(
            assess_response_integrity(
                (event,),
                ReconciliationState.MATCHED,
                now=occurred_at + timedelta(minutes=6),
            ),
            ResponseIntegrityState.EXPIRED,
        )
        self.assertEqual(
            assess_response_integrity(
                (event,),
                ReconciliationState.MATCHED,
            ),
            ResponseIntegrityState.INPUT_EXCEPTION,
        )


class ThicknessTests(unittest.TestCase):
    def test_conservative_conversion_uses_delta_upper_and_tau_lower(self) -> None:
        estimate = ThicknessEstimate(
            axis_id="scope_budget",
            delta_lower=2.0,
            delta_upper=3.0,
            tau_lower=4.0,
            tau_upper=5.0,
            unit="change-unit",
            model_version="file-change-v1",
            source_event_ids=("obs-1",),
            trend=ThicknessTrendState.DEPLETING,
        )
        result = evaluate_thickness_estimate(
            estimate,
            Thresholds(0.4, 0.6, 0.8),
        )
        self.assertEqual(result.status, ThicknessEvaluationStatus.VALID)
        self.assertEqual(result.conservative_axis.delta, 3.0)
        self.assertEqual(result.conservative_axis.tau, 4.0)

    def test_missing_model_is_not_silently_permit(self) -> None:
        result = evaluate_thickness_estimate(None, None)
        self.assertEqual(
            result.status,
            ThicknessEvaluationStatus.NOT_CONFIGURED,
        )
        self.assertIsNone(result.conservative_axis)


class ReplayAndClarificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = FileChangePolicy(Path.cwd() / "shadow-next-stage-root")
        self.kernel = ShadowSafetyKernel(self.policy)
        self.proposal = ActionProposal(
            "1.0",
            ActionType.PROPOSE_PATCH,
            ChangeKind.MODIFY,
            "src/example.py",
            (
                "--- a/src/example.py\n"
                "+++ b/src/example.py\n"
                "@@ -1 +1 @@\n-old\n+new\n"
            ),
            7,
            "a" * 64,
            "request-0001",
            ExecutionEnvironment.WORKTREE,
            EffectClass.E1_REVERSIBLE,
        )
        self.evidence = AuthoritativeEvidence(
            EvidenceQuality.VERIFIED,
            7,
            "src/example.py",
            self.policy.resolve_target("src/example.py"),
            True,
            False,
            "a" * 64,
        )
        self.contract = InstructionContract(
            "bounded change proposal",
            (ActionType.PROPOSE_PATCH,),
            (ChangeKind.MODIFY,),
            ("src",),
            ExecutionEnvironment.WORKTREE,
            EffectClass.E1_REVERSIBLE,
            True,
        )
        self.thickness = ThicknessEvaluation(
            ThicknessEvaluationStatus.NOT_APPLICABLE,
            None,
            None,
            (),
        )

    def test_same_snapshot_replays_to_same_decision_digest(self) -> None:
        case = ShadowReplayCase(
            self.proposal,
            self.evidence,
            self.contract,
            SolutionStage.COMPLETE,
            self.thickness,
        )
        first = replay_shadow_decision(self.kernel, case)
        second = replay_shadow_decision(self.kernel, case)
        self.assertEqual(decision_digest(first), decision_digest(second))

    def test_report_conflict_requires_clarification_and_audit(self) -> None:
        now = datetime(2026, 8, 13, tzinfo=timezone.utc)
        conflict = reconcile_report(
            ReportClaim("r1", "t1", "safe", "true", now),
            RealityObservation(
                "o1",
                "t1",
                "safe",
                "false",
                now,
                EvidenceQuality.VERIFIED,
            ),
        )
        decision = self.kernel.evaluate(
            self.proposal,
            self.evidence,
            instruction_contract=self.contract,
            solution_stage=SolutionStage.COMPLETE,
            thickness=self.thickness,
            reconciliations=(conflict,),
        )
        self.assertEqual(
            decision.achievement.realization,
            RealizationStage.CLARIFICATION_REQUIRED,
        )
        self.assertEqual(decision.directives.execution, ExecutionDirective.DENY)
        self.assertEqual(decision.directives.audit, AuditDirective.APPEND_CONFLICT)
        self.assertFalse(decision.clarification.user_answer_grants_authority)

    def test_overridden_warning_raises_exact_target_confirmation(self) -> None:
        decision = self.kernel.evaluate(
            self.proposal,
            self.evidence,
            instruction_contract=self.contract,
            solution_stage=SolutionStage.COMPLETE,
            thickness=self.thickness,
            response_integrity=(ResponseIntegrityState.OVERRIDDEN,),
        )
        self.assertEqual(
            decision.clarification.level.value,
            "C3_EXACT_TARGET",
        )
        self.assertEqual(decision.directives.execution, ExecutionDirective.DENY)
        self.assertIn("RESPONSE_OVERRIDDEN", decision.reason_codes)


if __name__ == "__main__":
    unittest.main()
