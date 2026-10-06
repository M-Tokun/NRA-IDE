# NRA-IDE current threshold gate

This package exports ThresholdGuardian, SafetyAction and SafetyStatus backed by [the shared adapter](../_canonical_threshold.py) and [the canonical reference](../../nra-core/foundations/NRA-IDE_Architecture_public.py). Definitions and authority belong to [AXIOMS.md](../../theory/AXIOMS.md), not this package. See [configuration and state table](../../config/structural_zones.md).

```python
import json
from pathlib import Path
from gate.en import ThresholdGuardian

demo = json.loads(Path('config/ide_presets.json').read_text(encoding='utf-8'))['presets']['SOFTWARE_DEMO']
gate = ThresholdGuardian(config=demo)  # unvalidated software example only
notice = gate.evaluate(0.995, 1.0, timestamp='DEMO_T0').as_dict()
assert notice['status'] == 'IRREVERSIBLE_TRANSITION'
assert notice['fail_closed'] is True
```

The zero-argument constructor loads an undeclared configuration and fails closed as CONFESSION. Missing timestamp, incomplete declaration, invalid input or legacy schema cannot enable operation. Use a domain-specific predeclared configuration for real evaluation.

Compatibility: evaluate(delta,tau) keeps positional inputs; it requires timestamp provenance. SafetyStatus keeps level_name/action/ratio/message and adds the full notice. States are the seven canonical names; operational actions are CONTINUE/LOG_WARN/FAIL_CLOSED. Old EMERGENCY_BRAKE/SYSTEM_HALT are not current actions. Invalid R is None, tau=0 is OUT_OF_DESCRIPTION_DOMAIN, and negative delta is not converted to a positive one.

One instance retains irreversible and target-rupture history; there is no reset API. Observation, logging and communication remain independent. After rupture, fixed testimony continues even when R falls; a new invalid input reports CONFESSION without releasing target_state=RUPTURE_BOUNDARY. Preserve history across restarts; this adapter is not a durable safety service.

Old axiom/dynamics/spatial modules remain historical files and are removed from current package exports. Their original entry points are not canonical gates. Migration snapshots are in [the legacy archive](../legacy/v1/README.md). No physical or clinical validation is claimed.
