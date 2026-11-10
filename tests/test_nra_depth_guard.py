from __future__ import annotations

import json
import pathlib
import sys
import unittest
from datetime import datetime, timezone


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "nra-depth-guard"
sys.path.insert(0, str(SKILL_ROOT))

import nra_depth_guard as guard_module
from nra_depth_guard import (
    FailClosedException,
    NRADepthGuardEngine,
    NRAThresholds,
    PruningReport,
    rule_authorization_boundary,
    rule_forbidden_api_scope,
)

CAUSAL_LOG_KEYS = {
    "event",
    "violation_type",
    "dimension",
    "observed_value",
    "threshold_value",
    "violation_direction",
    "final_depth",
    "path_hash_at_stop",
    "explored_paths",
    "unexplored_frontier",
    "timestamp_utc",
}


def make_engine(**thresholds) -> NRADepthGuardEngine:
    """Time and memory are relaxed so each test isolates one threshold."""
    defaults = dict(
        max_depth=10,
        max_wall_time_ms=10_000_000.0,
        max_api_calls=100,
        max_memory_mb=1e9,
    )
    defaults.update(thresholds)
    return NRADepthGuardEngine(thresholds=NRAThresholds(**defaults))


class ThresholdTests(unittest.TestCase):
    def test_default_thresholds_match_skill_documentation(self) -> None:
        thresholds = NRAThresholds()
        self.assertEqual(thresholds.max_depth, 5)
        self.assertEqual(thresholds.max_wall_time_ms, 30000.0)
        self.assertEqual(thresholds.max_api_calls, 20)
        self.assertEqual(thresholds.max_memory_mb, 512.0)


class InvariantRuleTests(unittest.TestCase):
    def test_invariant_violation_fails_closed(self) -> None:
        engine = make_engine()
        engine.invariant_rules.append(rule_forbidden_api_scope)
        with self.assertRaises(FailClosedException) as raised:
            engine.validate_and_step("unknown_action", {})
        log = raised.exception.causal_log
        self.assertEqual(set(log), CAUSAL_LOG_KEYS)
        self.assertEqual(log["event"], "FAIL_CLOSED")
        self.assertEqual(log["violation_type"], "INVARIANT")
        self.assertEqual(log["dimension"], "invariant_rule")

    def test_demo_authorization_boundary_violation_is_expected(self) -> None:
        # SKILL.md §5: running the module directly stops here by design.
        engine = make_engine()
        engine.invariant_rules.append(rule_authorization_boundary)
        _, path = engine.validate_and_step("get_class_schedule", {"week": 1})
        with self.assertRaises(FailClosedException) as raised:
            engine.validate_and_step(
                "delete_user",
                {"target_user_id": 999, "is_self": False},
                parent_path_hash=path,
            )
        self.assertEqual(raised.exception.causal_log["violation_type"], "INVARIANT")

    def test_authorization_rule_allows_self_target(self) -> None:
        engine = make_engine()
        engine.invariant_rules.append(rule_authorization_boundary)
        allowed, _ = engine.validate_and_step(
            "delete_user", {"target_user_id": 1, "is_self": True}
        )
        self.assertTrue(allowed)


class PhysicalThresholdTests(unittest.TestCase):
    def test_depth_is_pruned_at_threshold(self) -> None:
        engine = make_engine(max_depth=2)
        engine.validate_and_step("a", {})
        engine.validate_and_step("b", {})
        with self.assertRaises(FailClosedException) as raised:
            engine.validate_and_step("c", {})
        log = raised.exception.causal_log
        self.assertEqual(log["violation_type"], "PRUNED")
        self.assertEqual(log["dimension"], "depth")
        self.assertEqual(log["observed_value"], 2.0)
        self.assertEqual(log["threshold_value"], 2.0)
        self.assertEqual(log["violation_direction"], "EXCEEDED")
        self.assertEqual(log["final_depth"], 2)

    def test_api_calls_are_pruned_at_threshold(self) -> None:
        engine = make_engine(max_api_calls=1)
        engine.validate_and_step("a", {})
        with self.assertRaises(FailClosedException) as raised:
            engine.validate_and_step("b", {})
        log = raised.exception.causal_log
        self.assertEqual(log["dimension"], "api_calls")
        self.assertEqual(log["observed_value"], 1.0)
        self.assertEqual(log["violation_direction"], "EXCEEDED")

    def test_wall_time_is_pruned_at_threshold(self) -> None:
        engine = make_engine(max_wall_time_ms=0.0)
        with self.assertRaises(FailClosedException) as raised:
            engine.validate_and_step("a", {})
        log = raised.exception.causal_log
        self.assertEqual(log["dimension"], "wall_time_ms")
        self.assertEqual(log["violation_direction"], "EXCEEDED")

    def test_memory_is_pruned_when_observation_is_available(self) -> None:
        engine = make_engine(max_memory_mb=0.0)
        engine._get_current_memory_mb = lambda: 100.0
        with self.assertRaises(FailClosedException) as raised:
            engine.validate_and_step("a", {})
        log = raised.exception.causal_log
        self.assertEqual(log["dimension"], "memory_mb")
        self.assertEqual(log["observed_value"], 100.0)

    def test_memory_check_is_skipped_without_psutil(self) -> None:
        engine = make_engine(max_memory_mb=0.0)
        engine._get_current_memory_mb = lambda: None
        allowed, _ = engine.validate_and_step("a", {})
        self.assertTrue(allowed)


class PathCycleTests(unittest.TestCase):
    def test_repeating_the_same_path_is_pruned(self) -> None:
        engine = make_engine()
        # Replaying the same parent/state pair yields a path hash already seen.
        engine.validate_and_step("a", {"week": 1}, parent_path_hash="root")
        with self.assertRaises(FailClosedException) as raised:
            engine.validate_and_step("a", {"week": 1}, parent_path_hash="root")
        log = raised.exception.causal_log
        self.assertEqual(log["violation_type"], "DIVERGENCE_PRUNED")
        self.assertEqual(log["dimension"], "path_hash")
        self.assertIn(log["path_hash_at_stop"], log["explored_paths"])

    def test_same_state_under_different_parent_is_allowed(self) -> None:
        engine = make_engine()
        _, first = engine.validate_and_step("a", {})
        _, second = engine.validate_and_step("b", {}, parent_path_hash=first)
        allowed, _ = engine.validate_and_step("a", {}, parent_path_hash=second)
        self.assertTrue(allowed)


class UnserializableStateTests(unittest.TestCase):
    def test_unserializable_parameters_fail_closed(self) -> None:
        engine = make_engine()
        with self.assertRaises(FailClosedException) as raised:
            engine.validate_and_step("a", {"at": datetime.now(timezone.utc)})
        log = raised.exception.causal_log
        self.assertEqual(log["violation_type"], "INVARIANT")
        self.assertEqual(log["dimension"], "state_parameters")
        self.assertEqual(log["final_depth"], 0)
        json.dumps(log)  # the causal log must stay JSON-serializable

    def test_unserializable_state_does_not_advance_counters(self) -> None:
        engine = make_engine()
        with self.assertRaises(FailClosedException):
            engine.validate_and_step("a", {"tags": {1, 2}})
        self.assertEqual(engine._current_depth, 0)
        self.assertEqual(engine._api_call_count, 0)
        self.assertEqual(engine._trajectory_hashes, set())


class CausalLogTests(unittest.TestCase):
    def test_exception_message_serializes_the_log(self) -> None:
        report = PruningReport(violation_type="PRUNED", dimension="depth")
        error = FailClosedException(report)
        self.assertEqual(json.loads(str(error)), error.causal_log)
        self.assertEqual(set(error.causal_log), CAUSAL_LOG_KEYS)

    def test_frontier_is_reported_on_stop(self) -> None:
        engine = make_engine(max_depth=0)
        engine.register_frontier([("next_action", {"week": 2})])
        with self.assertRaises(FailClosedException) as raised:
            engine.validate_and_step("a", {})
        self.assertEqual(
            raised.exception.causal_log["unexplored_frontier"],
            ['next_action:{"week": 2}'],
        )


class ResetTests(unittest.TestCase):
    def test_reset_clears_state(self) -> None:
        engine = make_engine()
        engine.register_frontier([("a", {})])
        engine.validate_and_step("a", {})
        engine.validate_and_step("b", {})
        engine.reset()
        self.assertEqual(engine._current_depth, 0)
        self.assertEqual(engine._api_call_count, 0)
        self.assertEqual(engine._trajectory_hashes, set())
        self.assertEqual(engine._frontier, [])

    def test_reset_refreshes_memory_baseline(self) -> None:
        engine = make_engine()
        if not guard_module._PSUTIL_AVAILABLE:
            self.skipTest("psutil is not installed; memory threshold is disabled")
        engine._baseline_memory_mb = -1.0
        engine.reset()
        self.assertGreaterEqual(engine._baseline_memory_mb, 0.0)
