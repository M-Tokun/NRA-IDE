"""Stateful gate adapter for the canonical NRA-IDE reference implementation.

Concrete domain declarations and thresholds must be fixed before evaluation.
This adapter classifies supplied Cause-Side observations; it does not prove
the physical derivation of delta/tau or persist state across process restarts.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
import importlib.util
import json
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'nra-core/foundations/NRA-IDE_Architecture_public.py'
_spec = importlib.util.spec_from_file_location('_gate_nra_reference', SOURCE)
if _spec is None or _spec.loader is None:
    raise ImportError('Canonical reference implementation unavailable')
REFERENCE = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(REFERENCE)

STATES = ('PERMIT', 'BOUNDARY_WARNING', 'HANDOFF_REQUIRED',
          'IRREVERSIBLE_TRANSITION', 'RUPTURE_BOUNDARY', 'CONFESSION',
          'OUT_OF_DESCRIPTION_DOMAIN')
DECLARATION_FIELDS = ('declared_target', 'unit', 'source', 'delta_rule',
                      'tau_rule', 'applicable_domain', 'threshold_basis')


class SafetyAction(Enum):
    """Operational effects, distinct from the seven canonical classifications."""
    CONTINUE = 'CONTINUE'
    LOG_WARN = 'LOG_WARN'
    FAIL_CLOSED = 'FAIL_CLOSED'


@dataclass(frozen=True)
class SafetyStatus:
    level_name: str
    action: SafetyAction
    ratio: Optional[float]
    message: str
    notice: dict

    @property
    def status(self):
        return self.level_name

    @property
    def irreversible_latched(self):
        return self.notice['irreversible_latched']

    def as_dict(self):
        result = deepcopy(self.notice)
        result['operational_action'] = self.action.value
        result['fail_closed'] = self.action is SafetyAction.FAIL_CLOSED
        return result


class ThresholdGuardian:
    """One instance represents one declared target and one evaluation history.

    No reset or per-call threshold override is provided. Configuration and
    output copies cannot clear retained irreversible/rupture state. A caller
    must preserve instance state or durable history for a continuing target;
    a new instance must not be used to declare that target recovered.
    """

    def __init__(self, config_path=None, *, config=None):
        self._irreversible_latched = False
        self._ruptured = False
        self._disclosure = []
        self._exceptions = []
        self._last_valid = None
        self._configuration_error = None
        self._config = {}
        try:
            if config is not None and config_path is not None:
                raise ValueError('Use config or config_path, not both')
            if config is None:
                path = Path(config_path) if config_path is not None else ROOT / 'config/ide_foundation_config.json'
                config = json.loads(path.read_text(encoding='utf-8'))
            if not isinstance(config, dict):
                raise ValueError('Configuration must be an object')
            self._config = deepcopy(config)
            meta = self._config.get('meta', {})
            if meta.get('schema_version') != 2 or meta.get('canonical_version') != '2.4':
                raise ValueError('Legacy or unsupported configuration schema')
            self._declaration = self._config.get('evaluation_declaration', {})
            if not isinstance(self._declaration, dict):
                raise ValueError('Evaluation declaration must be an object')
            missing = [key for key in DECLARATION_FIELDS
                       if not isinstance(self._declaration.get(key), str)
                       or not self._declaration[key].strip()]
            if missing:
                raise ValueError('Missing domain declaration: ' + ', '.join(missing))
            thresholds = self._config.get('thresholds', {})
            if not isinstance(thresholds, dict) or set(thresholds) != {'R_warn', 'R_handoff', 'R_irrev'}:
                raise ValueError('Three canonical thresholds must be declared')
            self._thresholds = deepcopy(thresholds)
            validation = REFERENCE.nra_ide_core_evaluation(0.0, 1.0, **self._threshold_arguments())
            if validation['status'] == 'CONFESSION':
                raise ValueError(validation['message'])
            if self._config.get('canonical_states') != list(STATES):
                raise ValueError('Canonical states must match the current state machine')
            if self._config.get('operational_actions') != self._expected_actions():
                raise ValueError('Operational actions must follow canonical autonomous permissions')
        except (OSError, UnicodeError, ValueError, TypeError, AttributeError):
            # Configuration failure is observable; it must not enable evaluation.
            self._configuration_error = 'Missing, invalid, legacy or incomplete domain configuration'

    @staticmethod
    def _expected_actions():
        return {state: ('CONTINUE' if state == 'PERMIT' else
                        'LOG_WARN' if state == 'BOUNDARY_WARNING' else 'FAIL_CLOSED')
                for state in STATES}

    @property
    def config(self):
        return deepcopy(self._config)

    def _threshold_arguments(self):
        return dict(r_warn=self._thresholds['R_warn'],
                    r_handoff=self._thresholds['R_handoff'],
                    r_irrev=self._thresholds['R_irrev'])

    def evaluate(self, current_fluctuation: Any, defined_thickness: Any, *,
                 timestamp=None, source=None, input_side='CAUSE_SIDE',
                 d_delta_dt=None, d_tau_dt=None, trend=None,
                 observation_channels=None, logging_state='ACTIVE',
                 communication_state='ACTIVE'):
        """Classify delta/tau without abs(), epsilon substitution or recovery.

        The positional names are retained for call compatibility. Both values
        must already have been constructed by the declared Cause-Side rules.
        A nonempty observation timestamp is required; source defaults only to
        the source fixed in the declaration, never to an inferred source.
        """
        delta, tau = current_fluctuation, defined_thickness
        target = getattr(self, '_declaration', {}).get('declared_target')
        error = self._configuration_error
        if not error and (not isinstance(timestamp, str) or not timestamp.strip()):
            error = 'Observation timestamp is unknown'
        if not error and source is not None and source != self._declaration['source']:
            error = 'Observation source differs from the fixed Cause-Side declaration'
        if not error and (not isinstance(logging_state, str) or not isinstance(communication_state, str)):
            error = 'Channel state must be a canonical string'
        if not error:
            try:
                REFERENCE._normalize_observation_channels(observation_channels)
            except (ValueError, TypeError):
                error = 'Observation channel metadata is invalid'
        if error:
            notice = REFERENCE.nra_ide_core_evaluation(None, tau)
            notice['message'] = error
            notice['missing_information'] = ['valid configuration or observation provenance']
            notice['input_exception_log'] = self._exceptions + [error]
        else:
            notice = REFERENCE.nra_ide_core_evaluation(
                delta, tau, **self._threshold_arguments(),
                irreversible_latched=self._irreversible_latched,
                d_delta_dt=d_delta_dt, d_tau_dt=d_tau_dt, trend=trend,
                input_side=input_side, declared_target=target,
                observation_channels=observation_channels,
                logging_state=logging_state, communication_state=communication_state,
                structural_disclosure_log=self._disclosure,
                input_exception_log=self._exceptions)
        # Input validity and surviving channels are independent dimensions.
        # The reference's input-exception result does not carry channel inputs,
        # so preserve independently valid channel metadata here without turning
        # missing observations into zero or inferring a healthy channel.
        if notice['status'] in {'CONFESSION', 'OUT_OF_DESCRIPTION_DOMAIN'}:
            try:
                channels = REFERENCE._normalize_observation_channels(observation_channels)
                notice['observation_channels'] = channels
                notice['observation_state'] = REFERENCE._aggregate_observation_state(channels)
            except (ValueError, TypeError):
                pass
            if isinstance(logging_state, str) and logging_state in REFERENCE.LOGGING_CHANNEL_STATES:
                notice['logging_state'] = logging_state
                notice['audit_log_route'] = 'ACTIVE' if logging_state == 'ACTIVE' else 'LOGGING_LOST'
            if isinstance(communication_state, str) and communication_state in REFERENCE.COMMUNICATION_CHANNEL_STATES:
                notice['communication_state'] = communication_state
        self._irreversible_latched |= notice['irreversible_latched']
        self._ruptured |= notice['status'] == 'RUPTURE_BOUNDARY'
        notice['declared_target'] = target
        notice['irreversible_latched'] = self._irreversible_latched
        valid = notice['status'] not in {'CONFESSION', 'OUT_OF_DESCRIPTION_DOMAIN'}
        if valid:
            self._last_valid = {
                'observed_delta': notice['observed_delta'], 'observed_tau': notice['observed_tau'],
                'R': notice['R'], 'timestamp': timestamp,
                'source': self._declaration['source']}
        # Rupture concerns the retained target; input exceptions remain separately
        # visible without releasing that target or suppressing fixed testimony.
        if self._ruptured:
            if valid:
                notice['status'] = 'RUPTURE_BOUNDARY'
                notice['code'] = 'RUPTURE_BOUNDARY'
                notice['message'] = 'Declared target remains ruptured; fixed testimony continues'
            notice['target_state'] = 'RUPTURE_BOUNDARY'
            notice['structural_testimony_mode'] = 'POST_RUPTURE_FIXED'
            notice['structural_testimony'] = 'POST_RUPTURE_FIXED'
            notice['execution_authority'] = 'EXTERNAL_PREDEFINED'
            notice['authority_transfer_scope'] = ['execution_authority']
            notice['autonomous_new_judgment'] = False
            notice['autonomous_new_operation'] = False
        notice['last_valid_observation'] = deepcopy(self._last_valid)
        notice['structural_disclosure_log'] = list(dict.fromkeys(self._disclosure + notice['structural_disclosure_log']))
        notice['input_exception_log'] = list(dict.fromkeys(self._exceptions + notice['input_exception_log']))
        notice['audit_log'] = notice['structural_disclosure_log'] + notice['input_exception_log']
        self._disclosure = list(notice['structural_disclosure_log'])
        self._exceptions = list(notice['input_exception_log'])
        action = SafetyAction.FAIL_CLOSED
        if notice['autonomous_new_operation'] and notice['autonomous_new_judgment']:
            action = SafetyAction.LOG_WARN if notice['status'] == 'BOUNDARY_WARNING' else SafetyAction.CONTINUE
        return SafetyStatus(notice['status'], action, notice['R'], notice['message'], deepcopy(notice))
