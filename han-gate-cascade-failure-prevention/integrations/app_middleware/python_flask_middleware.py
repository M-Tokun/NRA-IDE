# Filename: python_flask_middleware_2026-02-05_223015.py
# Author: M-Tokuni | GitHub: https://github.com/M-Tokun/NRA-IDE
# Project: HAN Gate (NRA/IDE) - Flask Middleware Integration
# Version: 2026-02-05_234000_FIXED
"""
HAN Gate middleware for Flask applications
WARNING: This is LAST RESORT. Prefer Envoy/Nginx at ingress.
"""
from __future__ import annotations
import os
import time
import requests
from functools import wraps
from flask import Flask, request, jsonify
from typing import Dict, Any, Callable

# Config
HAN_GATE_URL = os.getenv("HAN_GATE_URL", "http://han-gate.han.svc.cluster.local:8080/v1/decision")

# In-memory telemetry (per-worker, simple approximation)
_telemetry: Dict[str, Any] = {
    "retry_count": 0,
    "timeout_count": 0,
    "queue_depth": 0,
    "last_update": time.time()
}


def track_metrics(status_code: int, is_timeout: bool = False):
    """Track metrics for HAN decision"""
    global _telemetry
    
    # Increment retry/error counters
    if status_code >= 500:
        _telemetry["retry_count"] += 1
    
    if is_timeout or status_code in (408, 504):
        _telemetry["timeout_count"] += 1


def get_telemetry_snapshot() -> Dict[str, float]:
    """Get current telemetry snapshot with rates"""
    global _telemetry
    
    now = time.time()
    last = _telemetry.get("last_update", now)
    dt = max(now - last, 1.0)
    
    retry_rate = _telemetry["retry_count"] / dt
    timeout_rate = _telemetry["timeout_count"] / dt
    queue_depth = _telemetry["queue_depth"]
    
    # Reset counters periodically
    if dt >= 1.0:
        _telemetry["retry_count"] = 0
        _telemetry["timeout_count"] = 0
        _telemetry["last_update"] = now
    
    return {
        "retry_rate": retry_rate,
        "queue_depth": queue_depth,
        "dep_timeout_rate": timeout_rate
    }


def han_gate_middleware(service_name: str = "app"):
    """
    Flask decorator for HAN Gate protection.
    
    Usage:
        @app.route('/api/endpoint')
        @han_gate_middleware('my-service')
        def my_endpoint():
            return jsonify({"status": "ok"})
    
    WARNING: This middleware runs AFTER the request enters the app.
    Prefer Envoy/Nginx for true ingress-level protection.
    """
    def decorator(f: Callable):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Update queue estimate (active request count approximation)
            _telemetry["queue_depth"] = getattr(wrapped, "_active_requests", 0)
            wrapped._active_requests = getattr(wrapped, "_active_requests", 0) + 1
            
            try:
                # Check HAN Gate
                telemetry = get_telemetry_snapshot()
                
                try:
                    gate_resp = requests.post(
                        HAN_GATE_URL,
                        json={
                            "scope": {
                                "service": service_name,
                                "route": request.path
                            },
                            "telemetry": telemetry
                        },
                        timeout=0.1
                    )
                    decision = gate_resp.json().get("decision", "SILENCE")
                except Exception:
                    # Fail-Closed
                    decision = "SILENCE"
                
                if decision == "SILENCE":
                    # Return neutral response (204 No Content)
                    return "", 204
                
                # PASS => execute route handler
                response = f(*args, **kwargs)
                
                # Track response status
                if hasattr(response, "status_code"):
                    track_metrics(response.status_code)
                
                return response
            
            finally:
                # Decrement active requests
                wrapped._active_requests = max(0, getattr(wrapped, "_active_requests", 1) - 1)
        
        return wrapped
    return decorator


# Example usage
if __name__ == "__main__":
    app = Flask(__name__)
    
    @app.route("/api/protected")
    @han_gate_middleware("example-service")
    def protected_endpoint():
        return jsonify({"message": "This endpoint is HAN-protected"})
    
    @app.route("/healthz")
    def healthz():
        return "OK", 200
    
    app.run(host="0.0.0.0", port=8080)
