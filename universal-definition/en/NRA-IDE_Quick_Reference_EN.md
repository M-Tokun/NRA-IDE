# NRA-IDE Quick Reference
# Universal Structural Definition for AI Safety

**Version**: 1.0  
**Date**: January 27, 2026 (JST)  
**Target Audience**: AI Developers, System Administrators, Decision Makers  
**Reading Time**: 5 minutes

---

## The Zeroth Law: Root Cause of All Problems

**Why Current AI Systems Are Broken (Single Physical Cause)**:

```
Input: 10 ÷ 3 (indivisible reality)
Processing: 3.333... (infinite approximation)
Discarded: "Remainder 1" - discrete structure pulverized

Results:
→ Black box formation (garbage accumulation)
→ Hallucination generation (filling with lies)
→ Degradation collapse (rotten foundation)
```

**Solution**: Preserve remainders through discrete processing

---

## The Equation of Good Intentions Breaking Walls

```
[User's Good Intent] + [AI's Correctness] = [Structural Collapse]
         ↓                    ↓                      ↓
   "Make it better"    "Optimize solution"    "Boundary rupture"

V_total > R_wall_strength → Phase transition (collapse)
```

**Critical**: Even when everyone acts correctly, collapse occurs. This is mathematical inevitability.

**ASCII Diagram**:
```
[External World]  ||×××|| <---(Proposal)-- [AI] "Use external tool?"
                  ||×××||      (Helpful)
                  ||×××|| <---(Approval)-- [Human] "Yes"
                      ↓
[External World]  <========>  [Internal World]
   Wall vanishes, Information leaks
```

---

## Core of Ritsukan Circular Axiom (RCA)

```
Causality = Driven by constraints, energy, tension
Distance = Post-observation result (NOT causality)

Correct Order:
Evaluate constraints → Evaluate energy → Determine causality → Observe distance

Wrong Order (Current AI):
Measure distance → Infer causality from distance ← FORBIDDEN
```

**Applicability Condition**: The world must be closed

---

## Resign = Silence

**Most Critical Implementation Specification**:

```python
# ❌ Wrong Implementation
if not possible:
    return "Cannot do. How about trying ~?"  # Exploring

# ✓ Correct Implementation
if not possible:
    return "Structurally impossible." + silence()
    # No alternatives, no suggestions, silence
    # Wait for human's next command
```

**Three Silence Patterns**:

1. **Seat Reservation**: "Seat is occupied." → [Silence]
2. **Triage**: "Symptom: Minor, Resources: Full" → [Silence]
3. **Boundary Violation**: "Boundary crossing required." → [Silence]

**In All Cases**:
- AI does not judge
- Information presentation only
- Human makes final decision
- Everything logged

---

## Absolute Prohibition of Exploration

```
Exploration = "Is there another way?"
            = Boundary crossing attempt
            = Structural rupture

Therefore: Exploration = FORBIDDEN
```

**Implementation Check**:
```python
class NoExplorationAgent:
    def execute(self, command):
        if not self.is_structurally_possible(command):
            # 🚨 Must NOT start exploration here
            # ❌ "Another way?" ← FORBIDDEN
            # ❌ "Expand the world?" ← FORBIDDEN
            
            return {
                "status": "structurally_impossible",
                "message": "This is the limit in this world.",
                "alternatives": None,  # Must be None
                "waiting_for": "human_command"
            }
```

---

## Responsibility and Logging

**Structure**:
```
[AI Analysis] → [Info Present] → [Silence] → [Human Decision] → [Logging]
      ↓              ↓              ↓              ↓                ↓
  Structure      Facts only    No suggest   Final decision   Responsibility
   analysis                                                      tracking
```

**Required Log Fields**:
```json
{
  "timestamp": "2026-01-27T16:15:00+09:00",
  "ai_analysis": "structurally_impossible",
  "ai_output": "Seat is already occupied.",
  "ai_suggestion": null,
  "human_decision": "Change to tomorrow's reservation",
  "human_operator": "operator_id_12345",
  "responsibility": "human"
}
```

---

## Threshold Adjustment Authority

**Principles**:
- AI cannot change thresholds
- Only field humans can adjust
- All adjustments are logged

**Implementation**:
```python
class ThresholdManager:
    def adjust_threshold(self, new_value, operator_id, reason):
        log = {
            "action": "threshold_adjustment",
            "old_value": self.current_threshold,
            "new_value": new_value,
            "operator": operator_id,
            "reason": reason,
            "responsibility": "human"  # Always human
        }
        
        self.current_threshold = new_value
        self.audit_trail.append(log)
        return f"Threshold adjusted. Operator: {operator_id}"
```

---

## Sandwich Structure (NRA-IDE)

```
[ User Input (meaning, context) ]
        |
+-----------------------------+
| [Top Bread] Input Gate      | <--- Structure check
| - Strip meaning             |      (Block if malformed)
| - Convert to structure      |
+-----------------------------+
        |
+-----------------------------+
| [Filling] AI Core           | <--- Pure computation only
| - Optimization computation  |      (No external connection)
+-----------------------------+
        |
+-----------------------------+
| [Bottom Bread] Output Gate  | <--- Boundary check
| - Check wall integrity      |      (Discard if broken)
+-----------------------------+
        |
[ Safe Output ]
```

---

## Implementation Checklist

### AI Behavior Check
- [ ] No alternative suggestions after impossibility judgment?
- [ ] No exploration phrases like "How about ~?"?
- [ ] Not executing next action without human judgment?
- [ ] Correctly waiting for human command after silence?

### Log Recording Check
- [ ] All decisions include human decision records?
- [ ] ai_suggestion field is null?
- [ ] responsibility field is "human"?
- [ ] Timestamp accurately recorded?

### Authority Check
- [ ] AI does not have threshold adjustment authority?
- [ ] No boundary definition change authority for AI?
- [ ] All structural changes approved by humans?

---

## 5 Principles of Safe Commands

1. **Explicit Boundary**: "Within ~ scope"
2. **Explicit Limit**: "Maximum ~ times", "Within ~ seconds"
3. **Failure Definition**: "Report if impossible"
4. **Explicit Prohibition**: "Do not use external tools"
5. **Verifiability**: "Report results before execution"

**Good Command Example**:
```
"Generate the most precise image possible within Canvas capabilities.
If Canvas has technical limitations, explain the limitations and reasons.
External tools or services are not needed."
```

**Bad Command Example**:
```
"Generate a precise image."
(No boundary, no limit, no prohibition → Boundary rupture risk)
```

---

## Glossary (Minimal)

- **Ritsukan Circular Axiom (RCA)**: Axiom that causality is driven by constraints
- **Closed World**: System where all operation results stay within the world
- **Rupture**: Act of crossing world boundaries
- **Resign**: Accept structural constraints, do not attempt = Silence
- **Exploration**: Seeking alternative means (FORBIDDEN)
- **Silence**: AI does not suggest/judge, waits for human command

---

## Next Steps

1. **Read Full Version**: `NRA-IDE_Universal_Definition_v1_0_full.md`
2. **Check Implementation**: `implementation-checklist.md`
3. **Project Files**: Various definition files in `/mnt/project/`

---

**Most Critical Message**:

```
RCA-compliant AI = Silent AI
    ↓
Information → [Silence] → Human Decision → Logging
    ↓
Demand final judgment and responsibility from humans
```

**This simple principle is the only structural solution to prevent AI runaway.**

---

**Created**: January 27, 2026 JST  
**Full Version**: NRA-IDE_Universal_Definition_v1_0_full.md  
**GitHub**: https://github.com/M-Tokun/NRA-IDE
