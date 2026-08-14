import math
import unittest

from note.poc_horizontal_ai.safety_kernel.boundary import (
    AxisEvidence,
    Thresholds,
    evaluate_axes,
)
from note.poc_horizontal_ai.safety_kernel.states import (
    InputExceptionState,
    TargetBoundaryState,
)


class BoundaryClassificationTests(unittest.TestCase):
    def setUp(self) -> None:
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

    def test_all_five_target_states_are_distinct(self) -> None:
        cases = (
            (0.2, TargetBoundaryState.PERMIT),
            (0.4, TargetBoundaryState.BOUNDARY_WARNING),
            (0.6, TargetBoundaryState.HANDOFF_REQUIRED),
            (0.8, TargetBoundaryState.IRREVERSIBLE_TRANSITION),
            (1.0, TargetBoundaryState.RUPTURE_BOUNDARY),
        )
        for ratio, expected in cases:
            with self.subTest(ratio=ratio):
                result = evaluate_axes((self.axis(ratio),))
                self.assertEqual(result.target_state, expected)
                self.assertIsNone(result.input_exception)

    def test_tau_zero_is_out_of_description_domain(self) -> None:
        result = evaluate_axes((self.axis(0.0, tau=0.0),))
        self.assertEqual(
            result.input_exception,
            InputExceptionState.OUT_OF_DESCRIPTION_DOMAIN,
        )
        self.assertIsNone(result.target_state)

    def test_invalid_values_are_confession(self) -> None:
        cases = (
            self.axis(0.1, tau=-1.0),
            self.axis(0.1, delta=math.inf),
            self.axis(0.1, verified=False),
            self.axis(0.1, thresholds=Thresholds(0.7, 0.6, 0.8)),
        )
        for axis in cases:
            with self.subTest(reason=axis):
                result = evaluate_axes((axis,))
                self.assertEqual(
                    result.input_exception,
                    InputExceptionState.CONFESSION,
                )

    def test_boolean_and_invalid_metadata_types_are_confession(self) -> None:
        cases = (
            self.axis(0.1, delta=True),
            self.axis(0.1, tau=True),
            self.axis(0.1, thresholds=Thresholds(False, 0.6, 0.8)),
            self.axis(0.1, verified="yes"),
            self.axis(0.1, irreversible_latched="yes"),
        )
        for axis in cases:
            with self.subTest(axis=axis):
                result = evaluate_axes((axis,))
                self.assertEqual(
                    result.input_exception,
                    InputExceptionState.CONFESSION,
                )
                self.assertIsNone(result.target_state)

    def test_non_finite_derived_ratio_is_confession(self) -> None:
        result = evaluate_axes((self.axis(1.0e308, tau=1.0e-308),))
        self.assertEqual(
            result.input_exception,
            InputExceptionState.CONFESSION,
        )
        self.assertIsNone(result.target_state)
        self.assertIsNone(result.axes[0].ratio)

    def test_irreversible_latch_blocks_automatic_return(self) -> None:
        result = evaluate_axes(
            (self.axis(0.1, irreversible_latched=True),)
        )
        self.assertEqual(
            result.target_state,
            TargetBoundaryState.IRREVERSIBLE_TRANSITION,
        )
        self.assertTrue(result.irreversible_latched)

    def test_each_axis_is_retained_and_worst_state_governs(self) -> None:
        result = evaluate_axes(
            (
                self.axis(0.2, name="scope_escape"),
                self.axis(0.65, name="secret_exposure"),
            )
        )
        self.assertEqual(len(result.axes), 2)
        self.assertEqual(
            result.target_state,
            TargetBoundaryState.HANDOFF_REQUIRED,
        )
        self.assertEqual(result.governing_axis, "secret_exposure")

    def test_known_rupture_and_confession_coexist(self) -> None:
        result = evaluate_axes(
            (
                self.axis(1.0, name="known_rupture"),
                self.axis(0.1, name="missing_axis", verified=False),
            )
        )
        self.assertEqual(
            result.target_state,
            TargetBoundaryState.RUPTURE_BOUNDARY,
        )
        self.assertEqual(
            result.input_exception,
            InputExceptionState.CONFESSION,
        )
        self.assertEqual(result.governing_axis, "known_rupture")


if __name__ == "__main__":
    unittest.main()
