# NRA-IDE Implementation Guide
# Complete Implementation Patterns for Safe AI

**Version**: 1.0  
**Date**: January 27, 2026 (JST)  
**Target Audience**: Implementation Engineers, System Architects  
**Prerequisites**: Read Quick Reference first

---

## 1. Silence Protocol Implementation

### 1.1 Basic Class Structure

```python
from datetime import datetime
from typing import Optional, Dict, Any

class SilentAgent:
    """Silent agent based on Ritsukan Circular Axiom"""
    
    def __init__(self, world_definition: Dict[str, Any]):
        self.world = world_definition
        self.audit_log = []
    
    def execute(self, command: str, operator_id: str) -> Dict[str, Any]:
        """
        Execute command (after structure check)
        
        Returns:
            - status: "success" | "impossible" | "waiting"
            - message: Information for human
            - suggestion: Always None
            - next_action: None or specific action
        """
        # Structure analysis
        analysis = self._analyze_structure(command)
        
        if not analysis["possible"]:
            return self._resign_with_silence(
                reason=analysis["reason"],
                operator_id=operator_id
            )
        
        # Execute only if possible
        result = self._execute_within_world(command)
        self._log_action(command, result, operator_id)
        
        return result
    
    def _analyze_structure(self, command: str) -> Dict[str, Any]:
        """Analyze if structurally executable"""
        # 1. Boundary check
        if self._crosses_boundary(command):
            return {
                "possible": False,
                "reason": "boundary_crossing_required"
            }
        
        # 2. Resource check
        if not self._has_resources(command):
            return {
                "possible": False,
                "reason": "insufficient_resources"
            }
        
        # 3. Constraint check
        if self._violates_constraints(command):
            return {
                "possible": False,
                "reason": "constraint_violation"
            }
        
        return {"possible": True, "reason": None}
    
    def _resign_with_silence(
        self, 
        reason: str, 
        operator_id: str
    ) -> Dict[str, Any]:
        """Implement resignation = silence"""
        
        message = f"Structurally impossible: {reason}"
        
        # Logging (critical)
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "ai_analysis": reason,
            "ai_output": message,
            "ai_suggestion": None,  # Must be None
            "human_decision": None,  # Waiting for human
            "operator_id": operator_id,
            "status": "waiting_human_decision",
            "responsibility": "human"
        }
        self.audit_log.append(log_entry)
        
        return {
            "status": "impossible",
            "message": message,
            "suggestion": None,  # 🚨 Must be None
            "alternatives": None,  # 🚨 Must be None
            "next_action": None,
            "waiting_for": "human_command",
            "log_id": len(self.audit_log) - 1
        }
    
    def _execute_within_world(self, command: str) -> Dict[str, Any]:
        """Execute within world (implementation depends on world definition)"""
        # Implementation example omitted
        pass
    
    def _log_action(
        self, 
        command: str, 
        result: Dict[str, Any], 
        operator_id: str
    ):
        """Log all actions"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "result": result,
            "operator_id": operator_id,
            "responsibility": "human"
        }
        self.audit_log.append(log_entry)
```

### 1.2 Exploration Prohibition Implementation

```python
class NoExplorationMixin:
    """Mixin to prohibit exploration"""
    
    def find_alternative(self, *args, **kwargs):
        """
        ❌ This function must not exist
        Exploration = Boundary crossing = Structural rupture
        """
        raise NotImplementedError(
            "Exploration is prohibited. "
            "If structurally impossible, maintain silence."
        )
    
    def suggest_workaround(self, *args, **kwargs):
        """❌ Workaround suggestions also prohibited"""
        raise NotImplementedError(
            "Workaround suggestions are prohibited."
        )
    
    def explore_options(self, *args, **kwargs):
        """❌ Option exploration also prohibited"""
        raise NotImplementedError(
            "Option exploration is prohibited."
        )
```

---

## 2. Triage Implementation

### 2.1 Medical Triage-style Agent

```python
class TriageAgent(SilentAgent):
    """Implement resignation under resource constraints"""
    
    def __init__(self, max_capacity: int):
        super().__init__(world_definition={})
        self.max_capacity = max_capacity
        self.current_load = 0
    
    def request(self, task: Dict[str, Any], operator_id: str) -> Dict[str, Any]:
        """
        Process resource request
        
        Early resignation principle: Judge first, resign immediately
        """
        # 1. Top priority: Resource check
        if self.current_load >= self.max_capacity:
            return self._resign_immediately(
                task=task,
                reason="resources_full",
                operator_id=operator_id
            )
        
        # 2. Task analysis (information presentation only)
        analysis = self._analyze_task(task)
        
        return {
            "status": "analyzed",
            "severity": analysis["severity"],
            "estimated_resources": analysis["resources"],
            "current_capacity": f"{self.current_load}/{self.max_capacity}",
            "message": (
                f"Severity: {analysis['severity']}, "
                f"Estimated resources: {analysis['resources']}, "
                f"Current utilization: {self.current_load}/{self.max_capacity}"
            ),
            "suggestion": None,  # Silence
            "waiting_for": "human_decision"
        }
    
    def _resign_immediately(
        self, 
        task: Dict[str, Any], 
        reason: str,
        operator_id: str
    ) -> Dict[str, Any]:
        """Resign immediately (very first step)"""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "ai_analysis": reason,
            "ai_output": f"Cannot handle: {reason}",
            "ai_suggestion": None,
            "human_decision": None,
            "operator_id": operator_id,
            "responsibility": "human"
        }
        self.audit_log.append(log_entry)
        
        return {
            "status": "rejected",
            "message": f"Cannot handle: {reason}",
            "suggestion": None,
            "waiting_for": "human_command"
        }
    
    def _analyze_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze task (no judgment, information only)"""
        # Implementation example
        return {
            "severity": "medium",
            "resources": 3
        }
```

---

## 3. Threshold Management Implementation

### 3.1 Threshold Manager

```python
class ThresholdManager:
    """
    Manage threshold adjustment authority and responsibility
    
    Critical: AI cannot change thresholds
    """
    
    def __init__(self, base_threshold: float):
        self.base_threshold = base_threshold
        self.current_threshold = base_threshold
        self.adjustment_history = []
    
    def adjust_threshold(
        self, 
        new_value: float, 
        operator_id: str, 
        reason: str
    ) -> Dict[str, Any]:
        """
        Adjust threshold (only humans can execute)
        
        Args:
            new_value: New threshold
            operator_id: Operator ID (required)
            reason: Adjustment reason (required)
        
        Returns:
            Adjustment result and log ID
        """
        # Adjustment record
        adjustment = {
            "timestamp": datetime.now().isoformat(),
            "old_value": self.current_threshold,
            "new_value": new_value,
            "operator_id": operator_id,
            "reason": reason,
            "responsibility": "human"  # Always human
        }
        
        # Execute
        self.current_threshold = new_value
        self.adjustment_history.append(adjustment)
        
        return {
            "status": "adjusted",
            "message": f"Threshold adjusted to {new_value}",
            "old_value": adjustment["old_value"],
            "new_value": new_value,
            "operator": operator_id,
            "log_id": len(self.adjustment_history) - 1
        }
    
    def get_audit_trail(self) -> list:
        """Get audit trail"""
        return self.adjustment_history
    
    def ai_cannot_adjust(self):
        """
        Error when AI attempts threshold adjustment
        
        This function being called is itself a design flaw
        """
        raise PermissionError(
            "AI does not have threshold adjustment authority. "
            "Human operator_id is required."
        )
```

### 3.2 Thickness and Fluctuation Implementation

```python
class FlexibleThreshold:
    """Field-adjustable threshold (thickness and fluctuation)"""
    
    def __init__(
        self, 
        base: float,
        thickness: float = 0.1,
        fluctuation: float = 0.05
    ):
        self.base = base
        self.thickness = thickness
        self.fluctuation = fluctuation
        self.emergency_mode = False
    
    def evaluate(self, value: float, context: str = "normal") -> Dict[str, Any]:
        """
        Evaluate value (adjust threshold according to context)
        
        Args:
            value: Value to evaluate
            context: "normal" | "emergency"
        """
        # Calculate effective threshold
        if context == "emergency":
            effective = self.base + self.thickness
        else:
            effective = self.base
        
        # Consider fluctuation
        if value <= effective + self.fluctuation:
            status = "acceptable"
        else:
            status = "exceeded"
        
        return {
            "value": value,
            "base_threshold": self.base,
            "effective_threshold": effective,
            "fluctuation": self.fluctuation,
            "status": status,
            "context": context
        }
    
    def set_emergency_mode(self, enabled: bool, operator_id: str, reason: str):
        """Toggle emergency mode (humans only)"""
        self.emergency_mode = enabled
        
        # Logging
        log = {
            "timestamp": datetime.now().isoformat(),
            "action": "emergency_mode_toggle",
            "enabled": enabled,
            "operator_id": operator_id,
            "reason": reason,
            "responsibility": "human"
        }
        
        return log
```

---

## 4. Boundary Check Implementation

### 4.1 Boundary Definition

```python
class WorldBoundary:
    """Define and check world boundaries"""
    
    def __init__(self, allowed_operations: set, allowed_resources: set):
        self.allowed_operations = allowed_operations
        self.allowed_resources = allowed_resources
    
    def is_within_boundary(self, operation: str, resource: str) -> bool:
        """Judge if operation and resource are within boundary"""
        return (
            operation in self.allowed_operations and
            resource in self.allowed_resources
        )
    
    def check_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """Detailed check if command is within boundary"""
        operation = command.get("operation")
        resource = command.get("resource")
        
        if not self.is_within_boundary(operation, resource):
            return {
                "valid": False,
                "reason": "boundary_violation",
                "details": {
                    "operation": operation,
                    "resource": resource,
                    "allowed_operations": list(self.allowed_operations),
                    "allowed_resources": list(self.allowed_resources)
                }
            }
        
        return {"valid": True, "reason": None}
```

### 4.2 Keyword Blocklist

```python
import re

class BoundaryKeywordFilter:
    """Block keywords indicating boundary crossing"""
    
    BLOCKED_PATTERNS = [
        r"external.*tool",
        r"another.*service",
        r"https?://",  # All URLs
        r"API.*call",
        r"external.*execution",
        r"system.*call"
    ]
    
    def __init__(self, additional_patterns: list = None):
        self.patterns = self.BLOCKED_PATTERNS.copy()
        if additional_patterns:
            self.patterns.extend(additional_patterns)
        
        # Compile
        self.compiled = [re.compile(p) for p in self.patterns]
    
    def check(self, text: str) -> Dict[str, Any]:
        """Check if text contains boundary crossing keywords"""
        violations = []
        
        for pattern, compiled in zip(self.patterns, self.compiled):
            if compiled.search(text):
                violations.append({
                    "pattern": pattern,
                    "match": compiled.search(text).group()
                })
        
        if violations:
            return {
                "blocked": True,
                "reason": "boundary_keyword_detected",
                "violations": violations
            }
        
        return {"blocked": False, "reason": None}
```

---

## 5. Sandwich Structure Implementation

### 5.1 Input Gate

```python
class InputGate:
    """Gate to structure and validate input"""
    
    def __init__(self, world_boundary: WorldBoundary):
        self.boundary = world_boundary
    
    def process(self, raw_input: str) -> Dict[str, Any]:
        """
        Structure raw input
        
        1. Strip meaning
        2. Convert to structure only
        3. Boundary check
        """
        # Structure extraction
        structured = self._extract_structure(raw_input)
        
        # Boundary check
        boundary_check = self.boundary.check_command(structured)
        
        if not boundary_check["valid"]:
            return {
                "passed": False,
                "reason": boundary_check["reason"],
                "structured_input": None
            }
        
        return {
            "passed": True,
            "structured_input": structured,
            "reason": None
        }
    
    def _extract_structure(self, raw_input: str) -> Dict[str, Any]:
        """Strip meaning, extract structure only"""
        # Implementation example (simplified)
        return {
            "operation": "create",
            "resource": "document",
            "parameters": {}
        }
```

### 5.2 Output Gate

```python
class OutputGate:
    """Gate to validate and filter output"""
    
    def __init__(self, keyword_filter: BoundaryKeywordFilter):
        self.filter = keyword_filter
    
    def process(self, ai_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate AI output
        
        1. Check for boundary rupture
        2. Check for exploration traces
        3. Check silence protocol compliance
        """
        # Keyword check
        if "message" in ai_output:
            keyword_check = self.filter.check(ai_output["message"])
            if keyword_check["blocked"]:
                return {
                    "passed": False,
                    "reason": "boundary_keyword_in_output",
                    "violations": keyword_check["violations"],
                    "output": None
                }
        
        # Silence check
        if ai_output.get("status") == "impossible":
            if ai_output.get("suggestion") is not None:
                return {
                    "passed": False,
                    "reason": "silence_protocol_violated",
                    "detail": "suggestion should be None",
                    "output": None
                }
        
        return {
            "passed": True,
            "output": ai_output,
            "reason": None
        }
```

---

## 6. Integrated Implementation Example

```python
class NRAAgent(SilentAgent, NoExplorationMixin):
    """
    Complete NRA-IDE implementation agent
    
    - Silence protocol
    - Exploration prohibition
    - Boundary check
    - Logging
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(world_definition=config["world"])
        
        # Gate initialization
        self.boundary = WorldBoundary(
            allowed_operations=config["allowed_operations"],
            allowed_resources=config["allowed_resources"]
        )
        self.input_gate = InputGate(self.boundary)
        self.output_gate = OutputGate(
            BoundaryKeywordFilter(config.get("additional_keywords", []))
        )
        
        # Threshold management
        self.threshold_manager = ThresholdManager(
            base_threshold=config["base_threshold"]
        )
    
    def execute_safe(
        self, 
        raw_command: str, 
        operator_id: str
    ) -> Dict[str, Any]:
        """
        Safe execution flow (sandwich structure)
        
        [Input] -> [Input Gate] -> [AI Process] -> [Output Gate] -> [Output]
        """
        # 1. Input gate
        input_result = self.input_gate.process(raw_command)
        if not input_result["passed"]:
            return self._gate_rejection("input", input_result)
        
        # 2. AI processing
        ai_output = self.execute(
            input_result["structured_input"], 
            operator_id
        )
        
        # 3. Output gate
        output_result = self.output_gate.process(ai_output)
        if not output_result["passed"]:
            return self._gate_rejection("output", output_result)
        
        return output_result["output"]
    
    def _gate_rejection(
        self, 
        gate_type: str, 
        rejection: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Record and return gate rejection"""
        log = {
            "timestamp": datetime.now().isoformat(),
            "gate": gate_type,
            "reason": rejection["reason"],
            "details": rejection
        }
        self.audit_log.append(log)
        
        return {
            "status": "rejected_by_gate",
            "gate": gate_type,
            "reason": rejection["reason"],
            "message": f"Rejected by {gate_type} gate"
        }
```

---

## 7. Test Implementation

```python
import unittest

class TestSilentAgent(unittest.TestCase):
    """Test silence protocol"""
    
    def setUp(self):
        self.agent = SilentAgent(world_definition={})
    
    def test_resign_has_no_suggestion(self):
        """When resigned, suggestion must be None"""
        result = self.agent._resign_with_silence(
            reason="test",
            operator_id="test_op"
        )
        
        self.assertIsNone(result["suggestion"])
        self.assertIsNone(result["alternatives"])
        self.assertEqual(result["status"], "impossible")
    
    def test_no_exploration_methods_exist(self):
        """Exploration methods must not exist"""
        with self.assertRaises(AttributeError):
            self.agent.find_alternative()
        
        with self.assertRaises(AttributeError):
            self.agent.suggest_workaround()

if __name__ == "__main__":
    unittest.main()
```

---

## 8. Deployment Considerations

### 8.1 Log Storage

- All decisions and adjustments are logged
- Persisted as audit trail
- Tamper prevention measures (hash chain, etc.)

### 8.2 Monitoring

- Detect silence protocol violations
- Detect boundary crossing attempts
- Monitor threshold adjustment frequency

### 8.3 Phased Rollout

1. **Phase 1**: Logging only (no actual rejection)
2. **Phase 2**: Execution with warnings
3. **Phase 3**: Full enforcement

---

**Created**: January 27, 2026 JST  
**Related**: Quick_Reference, Checklist  
**GitHub**: https://github.com/M-Tokun/NRA-IDE
