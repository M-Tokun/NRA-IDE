# Filename: telemetry_sidecar_2026-02-05_223015.py
# Author: M-Tokuni | GitHub: https://github.com/M-Tokun/NRA-IDE
# Project: HAN Gate (NRA/IDE) - Telemetry Sidecar for Envoy Integration
# Version: 2026-02-05_234000_FIXED
"""
Telemetry Sidecar for Envoy ext_authz
Collects metrics from Envoy admin endpoint and calls HAN Gate
"""
from future import annotations
import os
import time
import requests
from flask import Flask, request, make_response
from typing import Dict, Any, Optional
app = Flask(name)
Config
ENVOY_ADMIN = os.getenv("ENVOY_ADMIN_URL", "http://127.0.0.1:9901")
HAN_GATE_URL = os.getenv("HAN_GATE_URL", "http://han-gate.han.svc.cluster.local:8080/v1/decision")
SCRAPE_INTERVAL = float(os.getenv("SCRAPE_INTERVAL", "1.0")) # seconds
Simple in-memory cache
_last_metrics: Dict[str, Any] = {
"retry_rate": 0.0,
"queue_depth": 0.0,
"dep_timeout_rate": 0.0,
"timestamp": 0.0,
"_retry_count": 0,
"_timeout_count": 0
}
def scrape_envoy_stats() -> Optional[Dict[str, float]]:
"""
Scrape Envoy admin stats endpoint.
OPTIMIZED: Uses filter to reduce payload size and CPU load.
"""
try:
# Optimization: Fetch only relevant metrics
# upstream_rq_retry, upstream_rq_timeout, upstream_rq_pending_total/active
filter_regex = "upstream_rq_(retry|timeout|pending|active)"
url = f"{ENVOY_ADMIN}/stats?format=json&usedonly&filter={filter_regex}"
code
Code
resp = requests.get(url, timeout=0.5)
    if resp.status_code != 200:
        return None # Trigger Fail-Closed

    stats = resp.json().get("stats", [])

    retry_count = 0
    timeout_count = 0
    queue_depth = 0

    for stat in stats:
        name = stat.get("name", "")
        value = stat.get("value", 0)

        # Filter out noise (overflows, resets)
        if "overflow" in name or "reset" in name:
            continue

        if "upstream_rq_retry" in name:
            retry_count += value
        elif "upstream_rq_timeout" in name:
            timeout_count += value
        elif "upstream_rq_pending" in name or "upstream_rq_active" in name:
            queue_depth += value

    # Compute rates
    now = time.time()
    last_ts = _last_metrics.get("timestamp", now - SCRAPE_INTERVAL)
    dt = max(now - last_ts, 0.1)

    last_retry = _last_metrics.get("_retry_count", 0)
    last_timeout = _last_metrics.get("_timeout_count", 0)

    # Handle counter resets (envoy restart)
    if retry_count < last_retry: last_retry = 0
    if timeout_count < last_timeout: last_timeout = 0

    retry_rate = max(0.0, (retry_count - last_retry) / dt)
    timeout_rate = max(0.0, (timeout_count - last_timeout) / dt)

    # Update cache
    _last_metrics.update({
        "retry_rate": retry_rate,
        "queue_depth": queue_depth,
        "dep_timeout_rate": timeout_rate,
        "timestamp": now,
        "_retry_count": retry_count,
        "_timeout_count": timeout_count
    })

    return {
        "retry_rate": retry_rate,
        "queue_depth": queue_depth,
        "dep_timeout_rate": timeout_rate
    }

except Exception:
    return None # Trigger Fail-Closed
@app.route("/healthz")
def healthz():
return "OK", 200
@app.route("/", methods=["GET", "POST"])
def ext_authz_handler():
# Extract scope
headers = request.headers
service = headers.get("x-envoy-service", "default")
route = headers.get("x-envoy-route", "default")
code
Code
# Scrape
telemetry = scrape_envoy_stats()

if telemetry is None:
    # Fail-Closed
    resp = make_response("Telemetry Failure", 403)
    resp.headers["x-han-decision"] = "SILENCE"
    return resp

# Call Gate
try:
    gate_resp = requests.post(
        HAN_GATE_URL,
        json={
            "scope": {"service": service, "route": route},
            "telemetry": telemetry
        },
        timeout=0.1
    )
    decision = gate_resp.json().get("decision", "SILENCE")
except Exception:
    decision = "SILENCE"

if decision == "PASS":
    resp = make_response("", 200)
    resp.headers["x-han-decision"] = "PASS"
    return resp
else:
    resp = make_response("Chain reaction detected", 403)
    resp.headers["x-han-decision"] = "SILENCE"
    return resp
if name == "main":
app.run(host="0.0.0.0", port=9090)
