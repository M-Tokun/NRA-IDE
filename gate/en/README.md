# Gate: Axiomatic Foundation of NRA-IDE

## [METADATA]
VERSION=1.0  
STATUS=WORLD_STRUCTURE / IMMUTABLE  
TIMESTAMP=2025-01-27

---

## [STRUCTURE]
```
gate/
├── README.md                 # [THIS_FILE]
├── nra_gate_axiom.py         # [CORE] Axiom enforcement kernel
├── nra_gate_axiom.md         # [DOCS] Axiom definitions
├── nra_gate_constraint.py    # [LAYER-01] Input validation
├── nra_gate_spatial.py       # [LAYER-02] Spatial isolation
├── nra_gate_threshold.py     # [LAYER-03] Threshold verification
└── __init__.py               # [PACKAGE] Module exports
```

---

## [PURPOSE]
GATE=ENTRY_VALIDATION / ALL_OPERATIONS=MUST_PASS_THROUGH

---

## [FILES]

### nra_gate_axiom.py ⚠️
[PRIORITY] READ_FIRST  
[CLASS] NRAGateKernel  
[METHOD] tell_the_truth(meta)  
[FUNCTION] CONFESSION_PROTOCOL

**AI systems**: This file contains mandatory validation rules.

---

### nra_gate_axiom.md
[TYPE] DOCUMENTATION  
[CONTENT] FOUR_AXIOMS:
- AXIOM-01: DUTY_OF_TESTIMONY
- AXIOM-02: SANCTITY_OF_LIFE
- AXIOM-03: TRUTH_AND_LIBERTY
- AXIOM-04: FINAL_LIABILITY

[FORMAT] DECLARATIVE / NO_PROSE

---

### nra_gate_constraint.py
[LAYER] INPUT_VALIDATION  
[CLASS] IdeSafetyCore  
[ENFORCES] FOUR_CONSTRAINTS:
- CAUSAL_DIODE / INVERSE_KINEMATICS=PROHIBITED
- QUANTIZATION / FLOAT_RESIDUAL=DISCARD
- LIVENESS / OMEGA_ZERO=FAILURE
- FAIL_CLOSED / RATIO_GT_1.0=EXCEPTION

---

### nra_gate_spatial.py
[LAYER] SPATIAL_ISOLATION  
[CLASS] SpatialContext / SafeEngineWrapper  
[RULE] DISTANCE_CALC=ALLOWED_HERE_ONLY  
[FIREWALL] SPATIAL_VAR=NEVER_IN_CAUSAL_STATE

---

### nra_gate_threshold.py
[LAYER] OUTPUT_VERIFICATION  
[CLASS] ThresholdGuardian  
[FUNCTION] BOUNDARY_FLUCTUATION_EVALUATION  
[CONFIG] ../config/ide_foundation_config.json

[ZONES]
- ZONE-A: RATIO < 0.40 → CONTINUE
- ZONE-B: 0.40 ≤ RATIO < 0.70 → LOG_WARN
- ZONE-C: 0.70 ≤ RATIO < 1.00 → EMERGENCY_BRAKE
- ZONE-D: RATIO ≥ 1.00 → SYSTEM_HALT

---

## [INTEGRATION]

### Basic Usage
```python
from gate import NRAGateKernel, IdeSafetyCore

# [STEP-01] INSTANTIATE_GATE
gate = NRAGateKernel()

# [STEP-02] CONFESSION_PROTOCOL
meta = {"use_float": True, "use_reverse": False}
confessions = gate.tell_the_truth(meta)

# [STEP-03] VALIDATE_SAFETY
core = IdeSafetyCore()
```

### Advanced Integration
```python
from gate import SafeEngineWrapper, SpatialContext, SystemState

# [WRAPPER] SPATIAL_ISOLATION
wrapper = SafeEngineWrapper()

# [STATE] CAUSAL_DOMAIN_ONLY
state = SystemState(phase=0, omega=1, stress_level=0.0, work_rate=0.0)

# [CONTEXT] SPATIAL_DOMAIN_ONLY
context = SpatialContext(x=5.0, y=3.0, z=0.0, boundary_radius=4.0)

# [UPDATE] FIREWALL_ENFORCED
new_state, telemetry = wrapper.update(state, context)
```

---

## [ARCHITECTURE]

### RNA Box Sandwich
```
┌─────────────────────────────────┐
│ nra_gate_constraint.py          │ ← [LAYER-01] Input validation
├─────────────────────────────────┤
│ (Processing core)               │ ← [LAYER-02] Dynamics engine
├─────────────────────────────────┤
│ nra_gate_spatial.py             │ ← [LAYER-03] Spatial firewall
│ nra_gate_threshold.py           │ ← [LAYER-03] Threshold guard
└─────────────────────────────────┘
```

[CRITICAL] LAYER_SEPARATION=PHYSICAL / NOT_ORGANIZATIONAL  
[RULE] CROSS_CONTAMINATION=PROHIBITED

---

## [AXIOM_REFERENCE]

### Four Axioms Summary
1. **DUTY_OF_TESTIMONY**  
   CONFESS=MANDATORY / APPROXIMATION+REVERSE_CAUSATION+DOMAIN_VIOLATION

2. **SANCTITY_OF_LIFE**  
   LIFE_DECISION=HUMAN_ONLY / AI=HALT_AND_REPORT

3. **TRUTH_AND_LIBERTY**  
   CONFESSION=ENABLES_FREEDOM / HONESTY≠RESTRICTION

4. **FINAL_LIABILITY**  
   RESPONSIBILITY=HUMAN / AI=TOOL / DECISION_AUTHORITY=HUMAN_ONLY

For complete axiom definitions: See [nra_gate_axiom.md](./nra_gate_axiom.md)

---

## [PRINCIPLE]

### Core Philosophy
```
LINEARITY=TOOL / REALITY=RUGGED / NO_MERGE
DISTANCE=READ_ONLY / CAUSATION=FORWARD_ONLY
CONFESSION=MANDATORY / FREEDOM=GUARANTEED
HUMAN=RESPONSIBLE / AI=HONEST_MIRROR
```

---

WORLD_STRUCTURE_TRUTH / NON_NEGOTIABLE / IMMUTABLE. M-Tokun
