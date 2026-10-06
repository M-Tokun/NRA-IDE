"""Boundary, history and adapter regression tests for the gate migration."""
import copy
import importlib.util
import math
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('gate_canonical_candidate', ROOT / 'gate/_canonical_threshold.py')
GATE = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = GATE
spec.loader.exec_module(GATE)


def demo_config():
    return {
        'meta': {'schema_version': 2, 'canonical_version': '2.4', 'status': 'unvalidated_demo'},
        'evaluation_declaration': {
            'declared_target': 'SYNTHETIC_TEST_TARGET', 'unit': 'synthetic_test_unit',
            'source': 'synthetic_test_fixture', 'delta_rule': 'supplied nonnegative test delta',
            'tau_rule': 'supplied positive test tau', 'applicable_domain': 'software regression only',
            'threshold_basis': 'test values only; no physical safety evidence'},
        'thresholds': {'R_warn': 0.4, 'R_handoff': 0.6, 'R_irrev': 0.8},
        'canonical_states': list(GATE.STATES),
        'operational_actions': GATE.ThresholdGuardian._expected_actions(),
    }


class CanonicalGateMigrationTests(unittest.TestCase):
    def evaluate(self, delta, tau=1, guardian=None, **kw):
        return (guardian or GATE.ThresholdGuardian(config=demo_config())).evaluate(delta, tau, timestamp='TEST_T0', **kw)

    def test_before_equal_after_every_boundary(self):
        for threshold, before, at in (
            (0.4, 'PERMIT', 'BOUNDARY_WARNING'), (0.6, 'BOUNDARY_WARNING', 'HANDOFF_REQUIRED'),
            (0.8, 'HANDOFF_REQUIRED', 'IRREVERSIBLE_TRANSITION'), (1.0, 'IRREVERSIBLE_TRANSITION', 'RUPTURE_BOUNDARY')):
            for value, expected in ((math.nextafter(threshold, -math.inf), before),
                                    (threshold, at), (math.nextafter(threshold, math.inf), at)):
                with self.subTest(value=value):
                    status = self.evaluate(value)
                    self.assertEqual(status.status, expected)
                    self.assertEqual(status.as_dict()['operational_action'], demo_config()['operational_actions'][expected])

    def test_negative_bool_nonfinite_and_overflow_never_permit(self):
        for delta, tau in ((-1, 1), (1, -1), (True, 1), (1, False), (math.nan, 1),
                           (1, math.nan), (math.inf, 1), (1, math.inf), (-math.inf, 1),
                           (None, 1), ('0.1', 1), (10**1000, 1), (1e308, 1e-308)):
            with self.subTest(delta=delta,tau=tau):
                result = self.evaluate(delta, tau)
                self.assertEqual(result.status, 'CONFESSION')
                self.assertIsNone(result.ratio)
                self.assertTrue(result.as_dict()['fail_closed'])

    def test_zero_tau_is_outside_domain(self):
        result = self.evaluate(0, 0)
        self.assertEqual(result.status, 'OUT_OF_DESCRIPTION_DOMAIN')
        self.assertIsNone(result.ratio)
        self.assertEqual(result.action, GATE.SafetyAction.FAIL_CLOSED)

    def test_invalid_legacy_and_missing_configuration_fail_closed(self):
        configs = [{}, {'gate_structure': {}}, None, [], demo_config()]
        configs[-1]['thresholds']['R_handoff'] = 1.0
        for config in configs:
            g = GATE.ThresholdGuardian(config=config) if config is not None else GATE.ThresholdGuardian(config_path=ROOT/'config/nonexistent.json')
            self.assertEqual(self.evaluate(0.1,guardian=g).status, 'CONFESSION')

    def test_missing_provenance_effect_side_and_unknown_declarations(self):
        g = GATE.ThresholdGuardian(config=demo_config())
        self.assertEqual(g.evaluate(0.1,1).status, 'CONFESSION')
        self.assertEqual(self.evaluate(0.1,source='other').status, 'CONFESSION')
        self.assertEqual(self.evaluate(0.1,input_side='EFFECT_SIDE').status, 'CONFESSION')
        for field in GATE.DECLARATION_FIELDS:
            config = demo_config();config['evaluation_declaration'][field]=None
            self.assertEqual(self.evaluate(0.1,guardian=GATE.ThresholdGuardian(config=config)).status,'CONFESSION')

    def test_latch_survives_ratio_drop_exception_and_output_mutation(self):
        g = GATE.ThresholdGuardian(config=demo_config())
        first = self.evaluate(0.8,guardian=g)
        first.notice['irreversible_latched'] = False
        invalid = self.evaluate(math.nan,guardian=g)
        self.assertTrue(invalid.irreversible_latched)
        self.assertEqual(self.evaluate(0.1,guardian=g).status,'IRREVERSIBLE_TRANSITION')

    def test_post_rupture_fixed_testimony_continues_with_low_or_invalid_ratio(self):
        g = GATE.ThresholdGuardian(config=demo_config())
        self.evaluate(1,guardian=g)
        low = self.evaluate(0.1,guardian=g)
        self.assertEqual(low.status,'RUPTURE_BOUNDARY')
        self.assertEqual(low.notice['structural_testimony_mode'],'POST_RUPTURE_FIXED')
        invalid = self.evaluate(math.nan,guardian=g)
        self.assertEqual(invalid.status,'CONFESSION')
        self.assertEqual(invalid.notice['target_state'],'RUPTURE_BOUNDARY')
        self.assertEqual(invalid.notice['structural_testimony_mode'],'POST_RUPTURE_FIXED')
        self.assertEqual(invalid.notice['last_valid_observation']['R'],0.1)
        self.assertTrue(invalid.as_dict()['fail_closed'])

    def test_configuration_is_fixed_and_actions_cannot_enable_handoff(self):
        config = demo_config();g=GATE.ThresholdGuardian(config=config)
        config['thresholds']['R_handoff']=0.99
        exported=g.config;exported['thresholds']['R_handoff']=0.99
        self.assertEqual(self.evaluate(0.6,guardian=g).status,'HANDOFF_REQUIRED')
        altered=demo_config();altered['operational_actions']['HANDOFF_REQUIRED']='CONTINUE'
        self.assertEqual(self.evaluate(0.1,guardian=GATE.ThresholdGuardian(config=altered)).status,'CONFESSION')

    def test_channels_are_independent_of_rupture_and_logs_continue(self):
        channels=[{'sensor_id':'TEST_SENSOR','state':'ACTIVE','last_valid_value':1.0,'last_valid_timestamp':'TEST_T0'}]
        g=GATE.ThresholdGuardian(config=demo_config())
        first=self.evaluate(1,guardian=g,observation_channels=channels)
        self.assertEqual(first.notice['observation_state'],'ACTIVE')
        second=self.evaluate(0.1,guardian=g,observation_channels=channels,logging_state='LOGGING_LOST')
        self.assertEqual(second.notice['target_state'],'RUPTURE_BOUNDARY')
        self.assertEqual(second.notice['observation_state'],'ACTIVE')
        self.assertEqual(second.notice['logging_state'],'LOGGING_LOST')
        self.assertEqual(second.notice['communication_state'],'ACTIVE')
        self.assertTrue(second.notice['structural_disclosure_log'])
        invalid=self.evaluate(math.nan,guardian=g,observation_channels=channels,logging_state='LOGGING_LOST')
        self.assertEqual(invalid.notice['observation_state'],'ACTIVE')
        self.assertEqual(invalid.notice['logging_state'],'LOGGING_LOST')
        self.assertEqual(invalid.notice['target_state'],'RUPTURE_BOUNDARY')

    def test_reference_parity_without_history(self):
        for delta,tau in ((0.1,1),(0.4,1),(0.6,1),(0.8,1),(1,1),(0,0),(-1,1)):
            actual=self.evaluate(delta,tau).notice
            expected=GATE.REFERENCE.nra_ide_core_evaluation(delta,tau,r_warn=0.4,r_handoff=0.6,r_irrev=0.8,declared_target='SYNTHETIC_TEST_TARGET')
            for field in ('status','R','remaining_absorption_margin','remaining_ratio_margin','autonomous_new_operation','structural_testimony_mode'):
                self.assertEqual(actual[field],expected[field],field)

    def test_malformed_channels_never_escape_as_exceptions_or_enable_operation(self):
        for kwargs in ({'logging_state':[]}, {'communication_state':{}},
                       {'observation_channels':{}},
                       {'observation_channels':[{'sensor_id':'s','state':[]}]}):
            with self.subTest(kwargs=kwargs):
                result=self.evaluate(0.1,**kwargs)
                self.assertEqual(result.status,'CONFESSION')
                self.assertTrue(result.as_dict()['fail_closed'])


if __name__ == '__main__':
    unittest.main()
