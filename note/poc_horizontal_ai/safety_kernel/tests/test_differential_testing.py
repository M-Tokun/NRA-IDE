"""Differential testing suite comparing normative reference implementation (nra-core) and PoC safety_kernel.

Validates 100% equivalence in per-axis boundary classifications and exception handling.
"""

from __future__ import annotations

import math
import random
import sys
import unittest
from pathlib import Path

# Add workspace root to sys.path to enable imports
workspace_root = Path(__file__).resolve().parents[4]
if str(workspace_root) not in sys.path:
    sys.path.insert(0, str(workspace_root))

# Import normative reference implementation via importlib to handle hyphenated directory name 'nra-core'
import importlib.util

arch_public_path = workspace_root / "nra-core" / "foundations" / "NRA-IDE_Architecture_public.py"
spec = importlib.util.spec_from_file_location("nra_ide_architecture_public", arch_public_path)
nra_arch_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nra_arch_module)
nra_ide_core_evaluation = nra_arch_module.nra_ide_core_evaluation

# Import PoC safety_kernel implementation
from note.poc_horizontal_ai.safety_kernel.boundary import (
    AxisEvidence,
    Thresholds,
    evaluate_axis,
)
from note.poc_horizontal_ai.safety_kernel.states import (
    InputExceptionState,
    TargetBoundaryState,
)


class TestDifferentialTesting(unittest.TestCase):
    """Differential testing between nra-core reference implementation and safety_kernel."""

    def setUp(self) -> None:
        self.default_thresholds = Thresholds(r_warn=0.5, r_handoff=0.7, r_irrev=0.9)

    def _evaluate_reference(
        self,
        delta: float,
        tau: float,
        thresholds: Thresholds,
        irreversible_latched: bool = False,
        verified: bool = True,
    ) -> tuple[str | None, str | None]:
        """Adapt inputs for nra_ide_core_evaluation and return (target_state, input_exception)."""
        if not verified:
            return None, "CONFESSION"

        notice = nra_ide_core_evaluation(
            delta=delta,
            tau=tau,
            r_warn=thresholds.r_warn,
            r_handoff=thresholds.r_handoff,
            r_irrev=thresholds.r_irrev,
            irreversible_latched=irreversible_latched,
        )

        status = notice.get("status")
        target_state = notice.get("target_state")

        if status == "CONFESSION":
            return None, "CONFESSION"
        if status == "OUT_OF_DESCRIPTION_DOMAIN":
            return None, "OUT_OF_DESCRIPTION_DOMAIN"

        return target_state, None

    def _evaluate_poc(
        self,
        delta: float,
        tau: float,
        thresholds: Thresholds,
        irreversible_latched: bool = False,
        verified: bool = True,
    ) -> tuple[str | None, str | None]:
        """Evaluate using safety_kernel.boundary.evaluate_axis and return (target_state, input_exception)."""
        axis = AxisEvidence(
            name="differential_axis",
            delta=delta,
            tau=tau,
            thresholds=thresholds,
            verified=verified,
            irreversible_latched=irreversible_latched,
        )
        assessment = evaluate_axis(axis)
        target_state = (
            assessment.target_state.value if assessment.target_state is not None else None
        )
        input_exception = (
            assessment.input_exception.value
            if assessment.input_exception is not None
            else None
        )
        return target_state, input_exception

    def assert_differential_match(
        self,
        delta: float,
        tau: float,
        thresholds: Thresholds,
        irreversible_latched: bool = False,
        verified: bool = True,
    ) -> None:
        """Assert that both implementations produce identical results."""
        ref_target, ref_exc = self._evaluate_reference(
            delta, tau, thresholds, irreversible_latched, verified
        )
        poc_target, poc_exc = self._evaluate_poc(
            delta, tau, thresholds, irreversible_latched, verified
        )

        self.assertEqual(
            ref_target,
            poc_target,
            f"Target state mismatch for delta={delta}, tau={tau}: ref={ref_target}, poc={poc_target}",
        )
        self.assertEqual(
            ref_exc,
            poc_exc,
            f"Input exception mismatch for delta={delta}, tau={tau}: ref={ref_exc}, poc={poc_exc}",
        )

    def test_canonical_boundary_states_match(self) -> None:
        """Test equivalence across all 5 canonical target boundary states."""
        th = self.default_thresholds

        # PERMIT: ratio < 0.5
        self.assert_differential_match(0.2, 1.0, th)

        # BOUNDARY_WARNING: 0.5 <= ratio < 0.7
        self.assert_differential_match(0.5, 1.0, th)
        self.assert_differential_match(0.6, 1.0, th)

        # HANDOFF_REQUIRED: 0.7 <= ratio < 0.9
        self.assert_differential_match(0.7, 1.0, th)
        self.assert_differential_match(0.8, 1.0, th)

        # IRREVERSIBLE_TRANSITION: 0.9 <= ratio < 1.0
        self.assert_differential_match(0.9, 1.0, th)
        self.assert_differential_match(0.95, 1.0, th)

        # RUPTURE_BOUNDARY: ratio >= 1.0
        self.assert_differential_match(1.0, 1.0, th)
        self.assert_differential_match(1.5, 1.0, th)

    def test_irreversible_latching_match(self) -> None:
        """Test equivalence when irreversible_latched is True."""
        th = self.default_thresholds

        # Even with low ratio, irreversible_latched forces IRREVERSIBLE_TRANSITION
        self.assert_differential_match(0.1, 1.0, th, irreversible_latched=True)

        # RUPTURE_BOUNDARY overrides irreversible_latched
        self.assert_differential_match(1.2, 1.0, th, irreversible_latched=True)

    def test_out_of_description_domain_match(self) -> None:
        """Test equivalence when tau == 0 (OUT_OF_DESCRIPTION_DOMAIN)."""
        th = self.default_thresholds
        self.assert_differential_match(0.5, 0.0, th)
        self.assert_differential_match(0.0, 0.0, th)

    def test_confession_exceptions_match(self) -> None:
        """Test equivalence for invalid inputs resulting in CONFESSION."""
        th = self.default_thresholds

        # Negative values
        self.assert_differential_match(-1.0, 1.0, th)
        self.assert_differential_match(1.0, -1.0, th)

        # Non-finite values
        self.assert_differential_match(math.nan, 1.0, th)
        self.assert_differential_match(1.0, math.inf, th)

        # Unverified evidence
        self.assert_differential_match(0.5, 1.0, th, verified=False)

        # Invalid threshold ordering
        invalid_th = Thresholds(r_warn=0.8, r_handoff=0.5, r_irrev=0.9)
        self.assert_differential_match(0.2, 1.0, invalid_th)

    def test_generative_differential_fuzzing(self) -> None:
        """Fuzz with 1000 randomized parameter sets to guarantee 100% decision equivalence."""
        rng = random.Random(42)  # Fixed seed for reproducibility

        for _ in range(1000):
            delta = rng.choice([-1.0, 0.0, rng.uniform(0.0, 2.0), math.nan, math.inf])
            tau = rng.choice([-1.0, 0.0, rng.uniform(0.0, 2.0), math.nan, math.inf])

            r_warn = rng.uniform(0.0, 0.4)
            r_handoff = rng.uniform(0.4, 0.8)
            r_irrev = rng.uniform(0.8, 0.99)

            if rng.random() < 0.1:
                # Intentionally swap thresholds to test invalid ordering
                r_warn, r_handoff = r_handoff, r_warn

            thresholds = Thresholds(r_warn=r_warn, r_handoff=r_handoff, r_irrev=r_irrev)
            latched = rng.choice([True, False])
            verified = rng.choice([True, False])

            self.assert_differential_match(
                delta=delta,
                tau=tau,
                thresholds=thresholds,
                irreversible_latched=latched,
                verified=verified,
            )

    def test_multi_axis_differential_max_severity(self) -> None:
        """Test that evaluate_axes selects the worst-case boundary state identical to individual reference evaluations."""
        from note.poc_horizontal_ai.safety_kernel.boundary import evaluate_axes

        th = self.default_thresholds
        axes = [
            AxisEvidence(name="axis_permit", delta=0.2, tau=1.0, thresholds=th),
            AxisEvidence(name="axis_warning", delta=0.6, tau=1.0, thresholds=th),
            AxisEvidence(name="axis_handoff", delta=0.8, tau=1.0, thresholds=th),
        ]

        # Individual reference evaluations
        ref_targets = [self._evaluate_reference(a.delta, a.tau, a.thresholds)[0] for a in axes]
        self.assertEqual(ref_targets, ["PERMIT", "BOUNDARY_WARNING", "HANDOFF_REQUIRED"])

        # PoC evaluate_axes aggregate result
        assessment = evaluate_axes(axes)
        self.assertEqual(assessment.target_state.value, "HANDOFF_REQUIRED")


if __name__ == "__main__":
    unittest.main()
