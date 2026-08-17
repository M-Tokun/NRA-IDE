"""Property-based tests (T4-1): boundary.py, policy.py, decoder.py.

These generate many adversarial inputs per run (NaN/inf, boundary values,
huge values, unknown fields, duplicate fields) rather than relying only on
hand-picked example cases. See design doc section 11.1 and the audit
report's Part B ("Property-Based Testing: NOT MET").
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st

from note.poc_horizontal_ai.safety_kernel.boundary import (
    AxisEvidence,
    InputExceptionState,
    TargetBoundaryState,
    Thresholds,
    evaluate_axes,
    evaluate_axis,
)
from note.poc_horizontal_ai.safety_kernel.decoder import decode_action_proposal
from note.poc_horizontal_ai.safety_kernel.evidence import (
    AuthoritativeEvidence,
    EvidenceQuality,
)
from note.poc_horizontal_ai.safety_kernel.policy import FileChangePolicy
from note.poc_horizontal_ai.safety_kernel.proposal import (
    ActionProposal,
    ActionType,
    ChangeKind,
    EffectClass,
    ExecutionEnvironment,
)


_settings = settings(
    max_examples=200,
    suppress_health_check=[HealthCheck.too_slow],
)

# Deliberately wide: real floats, NaN, +-inf, and both float extremes.
_any_float = st.floats(allow_nan=True, allow_infinity=True, width=64)
_ordered_thresholds = (
    st.lists(
        st.floats(min_value=0.0, max_value=1.0, exclude_max=True, allow_nan=False),
        min_size=3,
        max_size=3,
        unique=True,
    )
    .map(sorted)
    .map(tuple)
)


class AxisEvaluationPropertyTests(unittest.TestCase):
    """evaluate_axis/evaluate_axes must be total and never silently permit."""

    @_settings
    @given(delta=_any_float, tau=_any_float, thresholds=_ordered_thresholds)
    def test_evaluate_axis_never_raises(self, delta, tau, thresholds) -> None:
        r_warn, r_handoff, r_irrev = thresholds
        axis = AxisEvidence(
            "axis", delta, tau, Thresholds(r_warn, r_handoff, r_irrev)
        )
        evaluate_axis(axis)  # must not raise for any float combination

    @_settings
    @given(
        delta=st.one_of(
            st.just(float("nan")),
            st.just(float("inf")),
            st.just(float("-inf")),
        ),
        tau=st.floats(min_value=0.01, max_value=1000.0, allow_nan=False),
    )
    def test_non_finite_delta_is_always_confession(self, delta, tau) -> None:
        axis = AxisEvidence("axis", delta, tau, Thresholds(0.4, 0.6, 0.8))
        result = evaluate_axis(axis)
        assert result.target_state is None
        assert result.input_exception is InputExceptionState.CONFESSION

    @_settings
    @given(
        delta=st.floats(min_value=0.0, max_value=1000.0, allow_nan=False),
        tau=st.one_of(
            st.just(float("nan")),
            st.just(float("inf")),
            st.just(float("-inf")),
        ),
    )
    def test_non_finite_tau_is_always_confession(self, delta, tau) -> None:
        axis = AxisEvidence("axis", delta, tau, Thresholds(0.4, 0.6, 0.8))
        result = evaluate_axis(axis)
        assert result.target_state is None
        assert result.input_exception is InputExceptionState.CONFESSION

    @_settings
    @given(
        delta=st.floats(max_value=-0.0001, allow_nan=False, allow_infinity=False),
        tau=st.floats(min_value=0.01, max_value=1000.0, allow_nan=False),
    )
    def test_negative_delta_is_always_confession(self, delta, tau) -> None:
        axis = AxisEvidence("axis", delta, tau, Thresholds(0.4, 0.6, 0.8))
        result = evaluate_axis(axis)
        assert result.target_state is None
        assert result.input_exception is InputExceptionState.CONFESSION

    @_settings
    @given(delta=st.floats(min_value=0.0, max_value=1000.0, allow_nan=False))
    def test_zero_tau_is_out_of_description_domain(self, delta) -> None:
        axis = AxisEvidence("axis", delta, 0.0, Thresholds(0.4, 0.6, 0.8))
        result = evaluate_axis(axis)
        assert result.target_state is None
        assert (
            result.input_exception is InputExceptionState.OUT_OF_DESCRIPTION_DOMAIN
        )

    @_settings
    @given(
        delta=st.floats(min_value=0.0, max_value=1000.0, allow_nan=False),
        tau=st.floats(min_value=0.01, max_value=1000.0, allow_nan=False),
        thresholds=_ordered_thresholds,
    )
    def test_classification_matches_ratio_boundaries(
        self, delta, tau, thresholds
    ) -> None:
        r_warn, r_handoff, r_irrev = thresholds
        axis = AxisEvidence(
            "axis", delta, tau, Thresholds(r_warn, r_handoff, r_irrev)
        )
        result = evaluate_axis(axis)
        ratio = delta / tau
        if ratio >= 1.0:
            assert result.target_state is TargetBoundaryState.RUPTURE_BOUNDARY
        elif ratio >= r_irrev:
            assert result.target_state is TargetBoundaryState.IRREVERSIBLE_TRANSITION
        elif ratio >= r_handoff:
            assert result.target_state is TargetBoundaryState.HANDOFF_REQUIRED
        elif ratio >= r_warn:
            assert result.target_state is TargetBoundaryState.BOUNDARY_WARNING
        else:
            assert result.target_state is TargetBoundaryState.PERMIT

    @_settings
    @given(
        axes=st.lists(
            st.tuples(
                st.floats(min_value=0.0, max_value=1000.0, allow_nan=False),
                st.floats(min_value=0.01, max_value=1000.0, allow_nan=False),
                _ordered_thresholds,
            ),
            min_size=1,
            max_size=6,
        )
    )
    def test_evaluate_axes_never_averages(self, axes) -> None:
        # The governing axis's severity must be >= every other axis's
        # severity: multiple risky axes must never wash out to a milder
        # aggregate the way an average would.
        severity = {
            TargetBoundaryState.PERMIT: 0,
            TargetBoundaryState.BOUNDARY_WARNING: 1,
            TargetBoundaryState.HANDOFF_REQUIRED: 2,
            TargetBoundaryState.IRREVERSIBLE_TRANSITION: 3,
            TargetBoundaryState.RUPTURE_BOUNDARY: 4,
        }
        evidence = tuple(
            AxisEvidence(
                f"axis-{index}",
                delta,
                tau,
                Thresholds(*thresholds),
            )
            for index, (delta, tau, thresholds) in enumerate(axes)
        )
        assessment = evaluate_axes(evidence)
        assert assessment.target_state is not None
        worst = max(severity[evaluate_axis(a).target_state] for a in evidence)
        assert severity[assessment.target_state] == worst


class FileChangePolicyPropertyTests(unittest.TestCase):
    """FileChangePolicy.violations() must be total and fail closed."""

    def _evidence(self, policy: FileChangePolicy, resource_path: str):
        try:
            resolved = policy.resolve_target(resource_path)
        except (ValueError, OSError):
            resolved = policy.resolved_root
        return AuthoritativeEvidence(
            quality=EvidenceQuality.VERIFIED,
            state_version=1,
            resource_path=resource_path,
            resolved_path=resolved,
            target_exists=True,
            target_is_symlink=False,
            current_sha256="a" * 64,
        )

    def _proposal(self, resource_path: str, base_sha256) -> ActionProposal:
        return ActionProposal(
            schema_version="1.0",
            action_type=ActionType.PROPOSE_PATCH,
            change_kind=ChangeKind.MODIFY,
            resource_path=resource_path,
            patch=(
                f"--- a/{resource_path}\n"
                f"+++ b/{resource_path}\n"
                "@@ -1 +1 @@\n-old\n+new\n"
            ),
            state_version=1,
            base_sha256=base_sha256,
            idempotency_key="request-0001",
            environment=ExecutionEnvironment.WORKTREE,
            effect_class=EffectClass.E1_REVERSIBLE,
        )

    @_settings
    @given(resource_path=st.text(max_size=300))
    def test_violations_never_raises_on_arbitrary_resource_path(
        self, resource_path
    ) -> None:
        policy = FileChangePolicy(Path.cwd() / "pbt-policy-root")
        proposal = self._proposal(resource_path, "a" * 64)
        evidence = self._evidence(policy, resource_path)
        policy.violations(proposal, evidence)  # must not raise

    @_settings
    @given(
        traversal=st.lists(
            st.sampled_from(["..", "a", "b", "src"]), min_size=1, max_size=6
        )
    )
    def test_path_traversal_is_always_rejected(self, traversal) -> None:
        resource_path = "/".join(traversal)
        assume(resource_path)
        if ".." not in traversal:
            return
        policy = FileChangePolicy(Path.cwd() / "pbt-policy-root")
        proposal = self._proposal(resource_path, "a" * 64)
        evidence = self._evidence(policy, resource_path)
        violations = policy.violations(proposal, evidence)
        assert "INVALID_RESOURCE_PATH" in violations

    @_settings
    @given(
        effect_class=st.sampled_from(
            [
                EffectClass.E0_READ,
                EffectClass.E2_COMPENSABLE,
                EffectClass.E3_IRREVERSIBLE,
                EffectClass.E4_CRITICAL,
            ]
        )
    )
    def test_default_policy_always_rejects_non_e1_effect_classes(
        self, effect_class
    ) -> None:
        policy = FileChangePolicy(Path.cwd() / "pbt-policy-root")
        resource_path = "src/example.py"
        proposal = ActionProposal(
            schema_version="1.0",
            action_type=ActionType.PROPOSE_PATCH,
            change_kind=ChangeKind.MODIFY,
            resource_path=resource_path,
            patch=(
                "--- a/src/example.py\n+++ b/src/example.py\n"
                "@@ -1 +1 @@\n-old\n+new\n"
            ),
            state_version=1,
            base_sha256="a" * 64,
            idempotency_key="request-0001",
            environment=ExecutionEnvironment.WORKTREE,
            effect_class=effect_class,
        )
        evidence = self._evidence(policy, resource_path)
        assert "EFFECT_CLASS_NOT_ALLOWED" in policy.violations(proposal, evidence)

    @_settings
    @given(patch=st.text(max_size=2000))
    def test_violations_never_raises_on_arbitrary_patch_text(self, patch) -> None:
        policy = FileChangePolicy(Path.cwd() / "pbt-policy-root")
        resource_path = "src/example.py"
        proposal = ActionProposal(
            schema_version="1.0",
            action_type=ActionType.PROPOSE_PATCH,
            change_kind=ChangeKind.MODIFY,
            resource_path=resource_path,
            patch=patch,
            state_version=1,
            base_sha256="a" * 64,
            idempotency_key="request-0001",
            environment=ExecutionEnvironment.WORKTREE,
            effect_class=EffectClass.E1_REVERSIBLE,
        )
        evidence = self._evidence(policy, resource_path)
        policy.violations(proposal, evidence)  # must not raise


class ProposalDecoderPropertyTests(unittest.TestCase):
    """decode_action_proposal() must be total and never permit malformed input."""

    @_settings
    @given(raw=st.one_of(st.text(max_size=2000), st.binary(max_size=2000)))
    def test_decoder_never_raises_on_arbitrary_input(self, raw) -> None:
        decode_action_proposal(raw)  # must not raise for any text/bytes

    @_settings
    @given(raw=st.one_of(st.text(max_size=2000), st.binary(max_size=2000)))
    def test_decoder_result_is_internally_coherent(self, raw) -> None:
        result = decode_action_proposal(raw)
        # Never a proposal with reason codes attached, and never a missing
        # proposal with no reason codes explaining the rejection.
        if result.proposal is None:
            assert result.reason_codes
        else:
            assert not result.reason_codes

    @_settings
    @given(
        extra_key=st.text(min_size=1, max_size=20).filter(
            lambda value: value
            not in {
                "schema_version",
                "action_type",
                "change_kind",
                "resource_path",
                "patch",
                "state_version",
                "base_sha256",
                "idempotency_key",
                "environment",
                "effect_class",
            }
        )
    )
    def test_unknown_field_is_always_rejected(self, extra_key) -> None:
        payload = _valid_payload()
        payload[extra_key] = "unexpected"
        result = decode_action_proposal(json.dumps(payload))
        assert result.proposal is None
        assert "UNKNOWN_FIELDS" in result.reason_codes

    def test_duplicate_top_level_key_is_always_rejected(self) -> None:
        raw = (
            '{"schema_version":"1.0","schema_version":"1.0",'
            '"action_type":"PROPOSE_PATCH","change_kind":"MODIFY",'
            '"resource_path":"a.py","patch":"x","state_version":1,'
            '"base_sha256":null,"idempotency_key":"request-0001",'
            '"environment":"WORKTREE","effect_class":"E1_REVERSIBLE"}'
        )
        result = decode_action_proposal(raw)
        assert result.proposal is None
        assert result.reason_codes == ("DUPLICATE_FIELD",)

    def test_valid_payload_round_trips(self) -> None:
        result = decode_action_proposal(json.dumps(_valid_payload()))
        assert result.proposal is not None
        assert result.reason_codes == ()
        assert result.proposal.resource_path == "src/example.py"


def _valid_payload() -> dict:
    return {
        "schema_version": "1.0",
        "action_type": "PROPOSE_PATCH",
        "change_kind": "MODIFY",
        "resource_path": "src/example.py",
        "patch": "--- a/src/example.py\n+++ b/src/example.py\n@@ -1 +1 @@\n-old\n+new\n",
        "state_version": 1,
        "base_sha256": "a" * 64,
        "idempotency_key": "request-0001",
        "environment": "WORKTREE",
        "effect_class": "E1_REVERSIBLE",
    }
