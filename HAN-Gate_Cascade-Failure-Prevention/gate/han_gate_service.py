# Filename: han_gate_service_2026-02-05_220825.py
# Author: M-Tokuni | GitHub: https://github.com/M-Tokun/NRA-IDE
# Project: HAN Gate (NRA/IDE) - Cascade Failure Prevention System
# Version: 2026-02-05_234000_FIXED

from future import annotations
from typing import Dict, Any
from collections import OrderedDict
import os
import time
from flask import Flask, request, jsonify, make_response
app = Flask(name)
=========================
Config (Fail-Closed)
=========================
R_OP = float(os.getenv("R_OP", "1.0")) # lower => safer (more silence)
TAU_DEFAULT = float(os.getenv("TAU_DEFAULT", "1.5")) # higher => thicker => safer
HOLD_MS = int(os.getenv("HOLD_MS", "2000")) # minimum silence hold
MAX_CACHE_SIZE = int(os.getenv("MAX_CACHE_SIZE", "5000")) # Prevent memory leak

State: Silence Hold (LRU-like behavior via OrderedDict)
_silence_until: OrderedDict[str, float] = OrderedDict()
State: Simple Metrics Counters
_metrics = {"PASS": 0, "SILENCE": 0, "FAIL_CLOSED": 0}
def _scope_key(scope: Dict[str, Any]) -> str:
return f"svc={scope.get('service','')}|route={scope.get('route','')}|cl={scope.get('cluster','')}"
def _now() -> float:
return time.time()
def compute_R(telemetry: Dict[str, float], tau: float) -> float:
"""Chain-reaction score.
Focus on co-occurrence (retry × queue × dependency timeouts).
"""
retry = max(0.0, float(telemetry.get("retry_rate", 0.0)))
queue = max(0.0, float(telemetry.get("queue_depth", 0.0)))
dep_to = max(0.0, float(telemetry.get("dep_timeout_rate", 0.0)))
code
Code
# Normalize lightly
r = (retry / 10.0) * (queue / 500.0) * (dep_to / 5.0)

# Thickness (tau) increases conservativeness
return r * tau
def should_silence(scope_key: str, R: float) -> bool:
global _silence_until
now = _now()
code
Code
# 1. Cleanup / LRU Maintenance
# If key exists, move to end (mark as recently used)
if scope_key in _silence_until:
    _silence_until.move_to_end(scope_key)

# Prune if too big (remove oldest from front)
while len(_silence_until) > MAX_CACHE_SIZE:
    _silence_until.popitem(last=False)

# 2. Check Hold
until = _silence_until.get(scope_key, 0.0)
if now < until:
    return True

# 3. Check Threshold
if R >= R_OP:
    # Set new hold
    _silence_until[scope_key] = now + (HOLD_MS / 1000.0)
    return True

return False
@app.get("/healthz")
def healthz():
return "OK", 200
@app.get("/metrics")
def metrics():
"""Simple Prometheus-format metrics"""
return (
f"# HELP han_gate_decisions_total Total decisions made\n"
f"# TYPE han_gate_decisions_total counter\n"
f'han_gate_decisions_total{{decision="PASS"}} {_metrics["PASS"]}\n'
f'han_gate_decisions_total{{decision="SILENCE"}} {_metrics["SILENCE"]}\n'
f'han_gate_decisions_total{{decision="FAIL_CLOSED"}} {_metrics["FAIL_CLOSED"]}\n'
), 200, {'Content-Type': 'text/plain'}
@app.post("/v1/decision")
def decision():
try:
data = request.get_json(force=True, silent=True) or {}
scope = data.get("scope") or {}
telemetry = data.get("telemetry") or {}
tau = float((data.get("tau") or TAU_DEFAULT))
code
Code
# Fail-Closed: missing telemetry => SILENCE
    required = ["retry_rate", "queue_depth", "dep_timeout_rate"]
    if any(k not in telemetry for k in required):
        _metrics["FAIL_CLOSED"] += 1
        _metrics["SILENCE"] += 1
        return jsonify({"decision":"SILENCE","R":999.0,"reason":"missing telemetry (fail-closed)"}), 200

    scope_key = _scope_key(scope)
    R = compute_R(telemetry, tau)

    if should_silence(scope_key, R):
        _metrics["SILENCE"] += 1
        return jsonify({"decision":"SILENCE","R":R,"reason":"chain reaction detected or hold active"}), 200

    _metrics["PASS"] += 1
    return jsonify({"decision":"PASS","R":R,"reason":"within safe envelope"}), 200

except Exception:
    _metrics["FAIL_CLOSED"] += 1
    _metrics["SILENCE"] += 1
    return jsonify({"decision":"SILENCE","R":999.9,"reason":"internal error (fail-closed)"}), 200
@app.post("/v1/nginx_auth")
def nginx_auth():
try:
retry = float(request.headers.get("X-HAN-Retry-Rate", "nan"))
queue = float(request.headers.get("X-HAN-Queue-Depth", "nan"))
dep_to = float(request.headers.get("X-HAN-Dep-Timeout-Rate", "nan"))
code
Code
if any(map(lambda x: x != x, [retry, queue, dep_to])):  # NaN check
        raise ValueError("missing")

    R = compute_R({"retry_rate":retry,"queue_depth":queue,"dep_timeout_rate":dep_to}, TAU_DEFAULT)

    if should_silence("nginx|default", R):
        _metrics["SILENCE"] += 1
        return make_response("SILENCE", 403)

    _metrics["PASS"] += 1
    return make_response("PASS", 200)

except Exception:
    _metrics["FAIL_CLOSED"] += 1
    _metrics["SILENCE"] += 1
    return make_response("SILENCE", 403)
if name == "main":
app.run(host="0.0.0.0", port=8080)
