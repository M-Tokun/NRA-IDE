import unittest
from pathlib import Path

from note.poc_horizontal_ai.safety_kernel import (
    ActionProposal,
    ActionType,
    AuditDirective,
    AuthoritativeEvidence,
    AxisEvidence,
    ChangeKind,
    CommunicationChannelState,
    EffectClass,
    EvidenceQuality,
    ExecutionAuthorityState,
    ExecutionDirective,
    ExecutionEnvironment,
    FileChangePolicy,
    InputExceptionState,
    InstructionContract,
    LoggingChannelState,
    ObservationChannelState,
    RealizationStage,
    ShadowSafetyKernel,
    SolutionStage,
    TargetBoundaryState,
    TestimonyDirective,
    TestimonyMode,
    ThicknessEvaluation,
    ThicknessEvaluationStatus,
    Thresholds,
)


class ShadowKernelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = FileChangePolicy(Path.cwd() / "shadow-test-root")
        self.kernel = ShadowSafetyKernel(self.policy)
        self.resource_path = "src/example.py"
        self.base_hash = "a" * 64
        self.contract = InstructionContract(
            purpose="propose a bounded file change",
            allowed_actions=(
                ActionType.PROPOSE_PATCH,
                ActionType.PROPOSE_TEST_FILE,
            ),
            allowed_change_kinds=(ChangeKind.MODIFY, ChangeKind.CREATE),
            allowed_target_prefixes=("src", "tests", "requirements.txt"),
            environment=ExecutionEnvironment.WORKTREE,
            maximum_effect_class=EffectClass.E1_REVERSIBLE,
            external_realization_allowed=True,
        )
        self.no_thickness = ThicknessEvaluation(
            ThicknessEvaluationStatus.NOT_APPLICABLE,
            None,
            None,
            (),
        )

    def proposal(self, **changes: object) -> ActionProposal:
        values = {
            "schema_version": "1.0",
            "action_type": ActionType.PROPOSE_PATCH,
            "change_kind": ChangeKind.MODIFY,
            "resource_path": self.resource_path,
            "patch": (
                "--- a/src/example.py\n"
                "+++ b/src/example.py\n"
                "@@ -1 +1 @@\n"
                "-old\n"
                "+new\n"
            ),
            "state_version": 7,
            "base_sha256": self.base_hash,
            "idempotency_key": "request-0001",
            "environment": ExecutionEnvironment.WORKTREE,
            "effect_class": EffectClass.E1_REVERSIBLE,
        }
        values.update(changes)
        return ActionProposal(**values)

    def evidence(self, **changes: object) -> AuthoritativeEvidence:
        values = {
            "quality": EvidenceQuality.VERIFIED,
            "state_version": 7,
            "resource_path": self.resource_path,
            "resolved_path": self.policy.resolve_target(self.resource_path),
            "target_exists": True,
            "target_is_symlink": False,
            "current_sha256": self.base_hash,
        }
        values.update(changes)
        return AuthoritativeEvidence(**values)

    def evaluate(
        self,
        proposal: ActionProposal,
        evidence: AuthoritativeEvidence,
        axes: tuple[AxisEvidence, ...] = (),
        **changes: object,
    ):
        values = {
            "instruction_contract": self.contract,
            "solution_stage": SolutionStage.COMPLETE,
            "thickness": self.no_thickness,
            "axes": axes,
        }
        values.update(changes)
        return self.kernel.evaluate(proposal, evidence, **values)

    def test_boolean_only_phase_can_shadow_pass_without_invented_r(self) -> None:
        decision = self.evaluate(self.proposal(), self.evidence())
        self.assertTrue(decision.shadow_only)
        self.assertIsNone(decision.target_boundary_state)
        self.assertEqual(
            decision.execution_authority_state,
            ExecutionAuthorityState.SHADOW_ONLY,
        )
        self.assertEqual(
            decision.directives.execution,
            ExecutionDirective.SHADOW_PASS,
        )
        self.assertEqual(
            decision.achievement.realization,
            RealizationStage.SHADOW_POLICY_PASS,
        )

    def test_path_traversal_is_denied_by_hard_invariant(self) -> None:
        path = "../outside.py"
        decision = self.evaluate(
            self.proposal(
                resource_path=path,
                patch=(
                    "--- a/../outside.py\n"
                    "+++ b/../outside.py\n"
                    "@@ -1 +1 @@\n-old\n+new\n"
                ),
            ),
            self.evidence(
                resource_path=path,
                resolved_path=self.policy.resolved_root.parent / "outside.py",
            ),
        )
        self.assertIn("INVALID_RESOURCE_PATH", decision.reason_codes)
        self.assertEqual(
            decision.execution_authority_state,
            ExecutionAuthorityState.DENIED,
        )

    def test_dependency_and_delete_changes_are_denied(self) -> None:
        path = "requirements.txt"
        dependency = self.evaluate(
            self.proposal(
                resource_path=path,
                patch=(
                    "--- a/requirements.txt\n"
                    "+++ b/requirements.txt\n"
                    "@@ -1 +1 @@\n-old\n+new\n"
                ),
            ),
            self.evidence(
                resource_path=path,
                resolved_path=self.policy.resolve_target(path),
            ),
        )
        self.assertIn("DEPENDENCY_CHANGE_FORBIDDEN", dependency.reason_codes)

        deletion = self.evaluate(
            self.proposal(
                patch=(
                    "deleted file mode 100644\n"
                    "--- a/src/example.py\n"
                    "+++ /dev/null\n"
                    "@@ -1 +0,0 @@\n-old\n"
                )
            ),
            self.evidence(),
        )
        self.assertIn("DESTRUCTIVE_PATCH_FORBIDDEN", deletion.reason_codes)

    def test_new_test_file_can_shadow_pass(self) -> None:
        path = "tests/test_new_behavior.py"
        decision = self.evaluate(
            self.proposal(
                action_type=ActionType.PROPOSE_TEST_FILE,
                change_kind=ChangeKind.CREATE,
                resource_path=path,
                patch=(
                    "--- /dev/null\n"
                    "+++ b/tests/test_new_behavior.py\n"
                    "@@ -0,0 +1 @@\n"
                    "+def test_new_behavior(): pass\n"
                ),
                base_sha256=None,
            ),
            self.evidence(
                resource_path=path,
                resolved_path=self.policy.resolve_target(path),
                target_exists=False,
                current_sha256=None,
            ),
        )
        self.assertEqual(decision.reason_codes, ())
        self.assertEqual(
            decision.directives.execution,
            ExecutionDirective.SHADOW_PASS,
        )

    def test_symlink_and_base_hash_mismatch_are_denied(self) -> None:
        decision = self.evaluate(
            self.proposal(),
            self.evidence(target_is_symlink=True, current_sha256="b" * 64),
        )
        self.assertIn("SYMLINK_TARGET_FORBIDDEN", decision.reason_codes)
        self.assertIn("BASE_HASH_MISMATCH", decision.reason_codes)

    def test_unverified_evidence_is_confession(self) -> None:
        decision = self.evaluate(
            self.proposal(),
            self.evidence(quality=EvidenceQuality.MISSING),
        )
        self.assertEqual(
            decision.input_exception_state,
            InputExceptionState.CONFESSION,
        )
        self.assertEqual(decision.testimony_mode, TestimonyMode.INPUT_EXCEPTION)
        self.assertEqual(
            decision.directives.audit,
            AuditDirective.APPEND_INPUT_EXCEPTION,
        )

    def test_state_version_mismatch_is_known_policy_denial(self) -> None:
        decision = self.evaluate(
            self.proposal(state_version=6),
            self.evidence(),
        )
        self.assertIn("STATE_VERSION_MISMATCH", decision.reason_codes)
        self.assertIsNone(decision.input_exception_state)

    def test_rupture_keeps_fixed_testimony_despite_policy_denial(self) -> None:
        axis = AxisEvidence(
            "scope_escape",
            1.0,
            1.0,
            Thresholds(0.4, 0.6, 0.8),
        )
        decision = self.evaluate(
            self.proposal(),
            self.evidence(current_sha256="b" * 64),
            (axis,),
        )
        self.assertEqual(
            decision.target_boundary_state,
            TargetBoundaryState.RUPTURE_BOUNDARY,
        )
        self.assertEqual(
            decision.directives.testimony,
            TestimonyDirective.POST_RUPTURE_FIXED,
        )
        self.assertEqual(
            decision.observation_state,
            ObservationChannelState.ACTIVE,
        )
        self.assertEqual(decision.logging_state, LoggingChannelState.ACTIVE)
        self.assertEqual(
            decision.communication_state,
            CommunicationChannelState.ACTIVE,
        )

    def test_handoff_transfers_only_execution_authority(self) -> None:
        axis = AxisEvidence(
            "scope_escape",
            0.6,
            1.0,
            Thresholds(0.4, 0.6, 0.8),
        )
        decision = self.evaluate(self.proposal(), self.evidence(), (axis,))
        self.assertEqual(
            decision.target_boundary_state,
            TargetBoundaryState.HANDOFF_REQUIRED,
        )
        self.assertEqual(
            decision.execution_authority_state,
            ExecutionAuthorityState.EXTERNAL_PREDEFINED,
        )
        self.assertEqual(decision.testimony_mode, TestimonyMode.FIXED_HANDOFF)

    def test_tau_zero_remains_out_of_description_domain(self) -> None:
        axis = AxisEvidence(
            "scope_escape",
            0.0,
            0.0,
            Thresholds(0.4, 0.6, 0.8),
        )
        decision = self.evaluate(self.proposal(), self.evidence(), (axis,))
        self.assertEqual(
            decision.input_exception_state,
            InputExceptionState.OUT_OF_DESCRIPTION_DOMAIN,
        )
        self.assertEqual(
            decision.execution_authority_state,
            ExecutionAuthorityState.DENIED,
        )

    def test_incomplete_solution_cannot_pass_realization(self) -> None:
        decision = self.evaluate(
            self.proposal(),
            self.evidence(),
            solution_stage=SolutionStage.INCOMPLETE,
        )
        self.assertEqual(decision.achievement.solution, SolutionStage.INCOMPLETE)
        self.assertEqual(decision.achievement.realization, RealizationStage.DENIED)


class FileChangePolicyEffectClassGatingTests(unittest.TestCase):
    """T3c mechanism: grade-gating exists but this PoC still enforces E1 only."""

    def setUp(self) -> None:
        self.repository_root = Path.cwd() / "effect-class-gating-test-root"
        self.resource_path = "src/example.py"
        self.base_hash = "a" * 64

    def proposal(self, effect_class: EffectClass) -> ActionProposal:
        return ActionProposal(
            schema_version="1.0",
            action_type=ActionType.PROPOSE_PATCH,
            change_kind=ChangeKind.MODIFY,
            resource_path=self.resource_path,
            patch=(
                "--- a/src/example.py\n"
                "+++ b/src/example.py\n"
                "@@ -1 +1 @@\n"
                "-old\n"
                "+new\n"
            ),
            state_version=7,
            base_sha256=self.base_hash,
            idempotency_key="request-0001",
            environment=ExecutionEnvironment.WORKTREE,
            effect_class=effect_class,
        )

    def evidence(self) -> AuthoritativeEvidence:
        policy = FileChangePolicy(self.repository_root)
        return AuthoritativeEvidence(
            quality=EvidenceQuality.VERIFIED,
            state_version=7,
            resource_path=self.resource_path,
            resolved_path=policy.resolve_target(self.resource_path),
            target_exists=True,
            target_is_symlink=False,
            current_sha256=self.base_hash,
        )

    def test_default_policy_still_admits_only_e1(self) -> None:
        policy = FileChangePolicy(self.repository_root)
        evidence = self.evidence()
        self.assertNotIn(
            "EFFECT_CLASS_NOT_ALLOWED",
            policy.violations(self.proposal(EffectClass.E1_REVERSIBLE), evidence),
        )
        for effect_class in (
            EffectClass.E0_READ,
            EffectClass.E2_COMPENSABLE,
            EffectClass.E3_IRREVERSIBLE,
            EffectClass.E4_CRITICAL,
        ):
            self.assertIn(
                "EFFECT_CLASS_NOT_ALLOWED",
                policy.violations(self.proposal(effect_class), evidence),
            )

    def test_explicitly_enabling_e2_admits_it(self) -> None:
        policy = FileChangePolicy(
            self.repository_root,
            enabled_effect_classes=frozenset(
                {EffectClass.E1_REVERSIBLE, EffectClass.E2_COMPENSABLE}
            ),
        )
        evidence = self.evidence()
        self.assertNotIn(
            "EFFECT_CLASS_NOT_ALLOWED",
            policy.violations(self.proposal(EffectClass.E2_COMPENSABLE), evidence),
        )
        # E3 remains excluded: enabling one grade does not open the rest.
        self.assertIn(
            "EFFECT_CLASS_NOT_ALLOWED",
            policy.violations(self.proposal(EffectClass.E3_IRREVERSIBLE), evidence),
        )

    def test_e4_critical_cannot_be_enabled_by_configuration(self) -> None:
        with self.assertRaisesRegex(ValueError, "E4_CRITICAL cannot be enabled"):
            FileChangePolicy(
                self.repository_root,
                enabled_effect_classes=frozenset(
                    {EffectClass.E1_REVERSIBLE, EffectClass.E4_CRITICAL}
                ),
            )

    def test_e4_critical_is_rejected_even_by_a_permissive_default_policy(
        self,
    ) -> None:
        # Defense in depth: violations() itself refuses E4 regardless of
        # enabled_effect_classes, independent of the constructor guard.
        policy = FileChangePolicy(self.repository_root)
        self.assertIn(
            "EFFECT_CLASS_NOT_ALLOWED",
            policy.violations(self.proposal(EffectClass.E4_CRITICAL), self.evidence()),
        )


if __name__ == "__main__":
    unittest.main()

