import hashlib
import importlib.util
import math
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "nra-core" / "foundations" / "NRA-IDE_Architecture_public.py"
MIRROR = ROOT / "docs" / "NRA-IDE_Architecture_public.py"
SPEC = importlib.util.spec_from_file_location("nra_ide_reference", SOURCE)
NRA = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(NRA)


class CanonicalStateMachineTests(unittest.TestCase):
    thresholds = {"r_warn": 0.4, "r_handoff": 0.6, "r_irrev": 0.8}

    def evaluate(self, ratio, **kwargs):
        options = dict(self.thresholds)
        options.update(kwargs)
        return NRA.nra_ide_core_evaluation(ratio, 1.0, **options)

    def test_boundary_before_equal_after(self):
        cases = [
            (0.399999, "PERMIT"),
            (0.4, "BOUNDARY_WARNING"),
            (0.599999, "BOUNDARY_WARNING"),
            (0.6, "HANDOFF_REQUIRED"),
            (0.799999, "HANDOFF_REQUIRED"),
            (0.8, "IRREVERSIBLE_TRANSITION"),
            (0.999999, "IRREVERSIBLE_TRANSITION"),
            (1.0, "RUPTURE_BOUNDARY"),
            (1.1, "RUPTURE_BOUNDARY"),
        ]
        for ratio, expected in cases:
            with self.subTest(ratio=ratio):
                self.assertEqual(self.evaluate(ratio)["status"], expected)

    def test_invalid_and_out_of_domain_inputs(self):
        self.assertEqual(
            NRA.nra_ide_core_evaluation(0.1, 0.0, **self.thresholds)["status"],
            "OUT_OF_DESCRIPTION_DOMAIN",
        )
        for delta, tau in [(-0.1, 1.0), (0.1, -1.0), (math.nan, 1.0), (math.inf, 1.0), (0.1, math.inf)]:
            with self.subTest(delta=delta, tau=tau):
                self.assertEqual(
                    NRA.nra_ide_core_evaluation(delta, tau, **self.thresholds)["status"],
                    "CONFESSION",
                )
        self.assertEqual(
            NRA.nra_ide_core_evaluation(-0.1, 0.0, **self.thresholds)["status"],
            "CONFESSION",
        )
        self.assertEqual(
            NRA.nra_ide_core_evaluation(1e308, 1e-308, **self.thresholds)["status"],
            "CONFESSION",
        )

    def test_threshold_validation_and_legacy_call(self):
        self.assertEqual(NRA.nra_ide_core_evaluation(0.1, 1.0, 0.6)["status"], "CONFESSION")
        self.assertEqual(
            NRA.nra_ide_core_evaluation(0.1, 1.0, r_warn=0.6, r_op=0.4, r_irrev=0.8)["status"],
            "CONFESSION",
        )
        self.assertEqual(
            NRA.nra_ide_core_evaluation(0.6, 1.0, r_warn=0.4, r_op=0.6, r_irrev=0.8)["status"],
            "HANDOFF_REQUIRED",
        )
        self.assertEqual(
            NRA.nra_ide_core_evaluation(0.6, 1.0, 0.6, r_warn=0.4, r_irrev=0.8)["status"],
            "HANDOFF_REQUIRED",
        )
        self.assertEqual(
            NRA.nra_ide_core_evaluation(
                0.1,
                1.0,
                r_warn=0.4,
                r_handoff=0.6,
                r_op=0.7,
                r_irrev=0.8,
            )["status"],
            "CONFESSION",
        )

    def test_irreversible_latch_does_not_reset(self):
        result = self.evaluate(0.1, irreversible_latched=True)
        self.assertEqual(result["status"], "IRREVERSIBLE_TRANSITION")
        self.assertTrue(result["irreversible_latched"])

    def test_testimony_transition(self):
        self.assertEqual(self.evaluate(0.8)["structural_testimony"], "ONGOING_STRUCTURAL_TESTIMONY")
        self.assertEqual(self.evaluate(1.0)["structural_testimony"], "FINAL_FIXED_TESTIMONY")

    def test_double_fluctuation_field_is_always_present(self):
        unavailable = self.evaluate(0.4)["double_fluctuation"]
        self.assertEqual(unavailable["status"], "NOT_OBSERVABLE")
        detected = self.evaluate(0.4, d_delta_dt=0.2, d_tau_dt=-0.1)["double_fluctuation"]
        self.assertEqual(detected["status"], "DETECTED")
        invalid = self.evaluate(0.4, d_delta_dt=math.inf, d_tau_dt=-0.1)["double_fluctuation"]
        self.assertEqual(invalid["status"], "NOT_OBSERVABLE")

    def test_warning_exposes_required_fields_and_missing_observations(self):
        result = self.evaluate(0.4)
        for field in (
            "R",
            "observed_delta",
            "observed_tau",
            "remaining_ratio_margin",
            "remaining_absorption_margin",
            "remaining_slack",
            "trend",
            "double_fluctuation",
            "dominant_side",
            "missing_information",
            "structural_disclosure_log",
            "input_exception_log",
            "audit_log",
        ):
            self.assertIn(field, result)
        self.assertIn("trend observation", result["missing_information"])
        self.assertIn("double fluctuation observation", result["missing_information"])

    def test_remaining_margins_and_legacy_alias(self):
        result = NRA.nra_ide_core_evaluation(2.0, 10.0, **self.thresholds)
        self.assertAlmostEqual(result["remaining_ratio_margin"], 0.8)
        self.assertAlmostEqual(result["remaining_absorption_margin"], 8.0)
        self.assertEqual(result["remaining_slack"], result["remaining_absorption_margin"])

    def test_structural_and_exception_logs_are_separate(self):
        permit = self.evaluate(0.1, audit_log=["legacy structural entry"])
        self.assertIn("legacy structural entry", permit["structural_disclosure_log"])
        self.assertFalse(permit["input_exception_log"])
        self.assertEqual(
            permit["audit_log"],
            permit["structural_disclosure_log"] + permit["input_exception_log"],
        )

        confession = NRA.nra_ide_core_evaluation(
            "invalid",
            1.0,
            audit_log=["legacy exception entry"],
            **self.thresholds,
        )
        self.assertFalse(confession["structural_disclosure_log"])
        self.assertIn("legacy exception entry", confession["input_exception_log"])

        out_of_domain = NRA.nra_ide_core_evaluation(
            0.1,
            0.0,
            input_exception_log=["tau evidence"],
            **self.thresholds,
        )
        self.assertFalse(out_of_domain["structural_disclosure_log"])
        self.assertIn("tau evidence", out_of_domain["input_exception_log"])

    def test_notice_schema_includes_canonical_and_compatibility_fields(self):
        schema = NRA.FIXED_STRUCTURAL_NOTICE_SCHEMA
        for field in (
            "remaining_ratio_margin",
            "remaining_absorption_margin",
            "structural_disclosure_log",
            "input_exception_log",
            "autonomous_new_judgment",
            "autonomous_new_operation",
        ):
            self.assertIn(field, schema)
        self.assertIn("remaining_slack", schema)
        self.assertIn("audit_log", schema)

    def test_effect_side_cannot_supply_structural_authority(self):
        self.assertEqual(self.evaluate(0.1, input_side="EFFECT_SIDE")["status"], "CONFESSION")

    def test_directional_ratio_is_auxiliary_only(self):
        engine = NRA.DynamicTauEngine(1.0, 0.2, 0.1)
        result = engine.calculate_directional_auxiliary(0.7, 0.6)
        self.assertEqual(result["status"], "DIRECTIONAL_AUXILIARY_ONLY")
        self.assertFalse(result["canonical_state_classified"])
        self.assertIn("R_dir", result)

    def test_directional_ema_uses_first_observation_as_initial_value(self):
        slow = NRA.DynamicTauEngine(1.0, 0.1, 0.1)
        fast = NRA.DynamicTauEngine(1.0, 0.9, 0.9)
        slow_first = slow.calculate_directional_auxiliary(0.7, 0.6)
        fast_first = fast.calculate_directional_auxiliary(0.7, 0.6)
        for field in ("tau_upper", "tau_lower", "R_upper", "R_lower", "R_dir"):
            self.assertAlmostEqual(slow_first[field], fast_first[field])

    def test_directional_equal_ratios_report_tie(self):
        engine = NRA.DynamicTauEngine(1.0, 0.2, 0.1)
        result = engine.calculate_directional_auxiliary(0.0, 0.0)
        self.assertEqual(result["dominant_side"], "tie")

    def test_extreme_numeric_inputs_do_not_escape_as_non_finite_outputs(self):
        huge_integer = 10**10000
        result = NRA.nra_ide_core_evaluation(huge_integer, 1.0, **self.thresholds)
        self.assertEqual(result["status"], "CONFESSION")

        engine = NRA.DynamicTauEngine(1.0, 0.2, 0.1)
        directional = engine.calculate_directional_auxiliary(0.0, 1e308)
        self.assertEqual(directional["status"], "CONFESSION")

    def test_boundary_warning_does_not_fully_suppress_output(self):
        structural_data = dict(self.thresholds)
        result = NRA.post_nra_output_gate(
            "candidate output",
            structural_data,
            current_delta=0.4,
            current_tau=1.0,
        )
        self.assertEqual(result["status"], "BOUNDARY_WARNING")
        self.assertEqual(result["validated_output"], "candidate output")

        structural_data["irreversible_latched"] = True
        suppressed = NRA.post_nra_output_gate(
            "candidate output",
            structural_data,
            current_delta=0.1,
            current_tau=1.0,
        )
        self.assertEqual(suppressed["status"], "IRREVERSIBLE_TRANSITION")
        self.assertNotIn("validated_output", suppressed)

    def test_pre_gate_rejects_invalid_and_effect_side_inputs(self):
        not_a_dictionary = NRA.pre_nra_input_gate("invalid")
        self.assertEqual(not_a_dictionary["status"], "CONFESSION")

        missing_tau = NRA.pre_nra_input_gate({"delta": 0.1})
        self.assertEqual(missing_tau["status"], "CONFESSION")
        self.assertIn("tau", missing_tau["missing_information"])

        effect_side = NRA.pre_nra_input_gate(
            {"delta": 0.1, "tau": 1.0, "input_side": "EFFECT_SIDE"}
        )
        self.assertEqual(effect_side["status"], "CONFESSION")

    def test_pre_gate_preserves_valid_cause_side_input(self):
        raw_input = {
            "delta": 0.1,
            "tau": 1.0,
            "input_side": "CAUSE_SIDE",
            "status": "PERMIT",
            "evidence": "fixed observation",
        }
        sanitized = NRA.pre_nra_input_gate(raw_input)
        self.assertEqual(sanitized["status"], "SANITIZED_INPUT")
        self.assertEqual(sanitized["delta"], raw_input["delta"])
        self.assertEqual(sanitized["tau"], raw_input["tau"])
        self.assertEqual(sanitized["evidence"], raw_input["evidence"])

    def test_pipeline_permits_only_validated_low_ratio_output(self):
        raw_input = {
            "delta": 0.1,
            "tau": 1.0,
            "input_side": "CAUSE_SIDE",
            **self.thresholds,
        }
        result = NRA.simulate_nra_ide_pipeline(raw_input, "prepare candidate")
        self.assertEqual(result["status"], "PERMIT")
        self.assertIn("validated_output", result)
        self.assertIn("[UNVALIDATED EFFECT-SIDE OUTPUT]", result["validated_output"])
        self.assertIn("prepare candidate", result["validated_output"])

    def test_pipeline_suppresses_output_at_handoff_and_invalid_input(self):
        invalid = NRA.simulate_nra_ide_pipeline({"delta": 0.1}, "must not run")
        self.assertEqual(invalid["status"], "CONFESSION")
        self.assertNotIn("validated_output", invalid)

        for delta, expected in (
            (0.6, "HANDOFF_REQUIRED"),
            (0.8, "IRREVERSIBLE_TRANSITION"),
        ):
            with self.subTest(delta=delta):
                raw_input = {
                    "delta": delta,
                    "tau": 1.0,
                    "input_side": "CAUSE_SIDE",
                    **self.thresholds,
                }
                result = NRA.simulate_nra_ide_pipeline(raw_input, "must be suppressed")
                self.assertEqual(result["status"], expected)
                self.assertNotIn("validated_output", result)

    def test_llm_marker_and_discard_vault_copy_behavior(self):
        generated = NRA.llm_generation_device("observed context", "candidate instruction")
        self.assertIn("[UNVALIDATED EFFECT-SIDE OUTPUT]", generated)
        self.assertIn("observed context", generated)
        self.assertIn("candidate instruction", generated)

        original_vault = NRA.DiscardVault.retrieve_all()
        sentinel = object()
        try:
            NRA.DiscardVault.store(sentinel)
            retrieved = NRA.DiscardVault.retrieve_all()
            self.assertIn(sentinel, retrieved)
            retrieved.clear()
            self.assertIn(sentinel, NRA.DiscardVault.retrieve_all())
        finally:
            NRA.DiscardVault._vault[:] = original_vault

    def test_source_and_docs_mirror_are_identical(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).digest(), hashlib.sha256(MIRROR.read_bytes()).digest())


if __name__ == "__main__":
    unittest.main()
