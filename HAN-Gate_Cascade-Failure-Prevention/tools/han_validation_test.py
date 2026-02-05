# Filename: han_validation_test_2026-0206-0346.py
# Purpose: Validate HAN Gate decision logic and ingress integration.

import requests
import time
import json

GATE_URL = "http://localhost:8080/v1/decision" # 実際の環境に合わせて変更

def test_decision(label, telemetry, expected=None):
    payload = {
        "scope": {"service": "validation-test", "route": "/test"},
        "telemetry": telemetry,
        "tau": 1.5
    }

    print(f"--- {label} ---")
    try:
        start = time.time()
        resp = requests.post(GATE_URL, json=payload, timeout=0.5)
        duration = (time.time() - start) * 1000
        result = resp.json()

        decision = result.get("decision")
        R = result.get("R")
        print(f"Result: {decision} (R={R:.4f}) | Latency: {duration:.2f}ms")

        if expected and decision != expected:
            print(f"⚠️  WARNING: Expected {expected} but got {decision}")
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# 1. 正常系 (Safe Envelope)
# R = (0.1/10) * (5/500) * (0.1/5) * 1.5 = 0.000003
test_decision("NORMAL TRAFFIC", {
    "retry_rate": 0.1,
    "queue_depth": 5,
    "dep_timeout_rate": 0.1
}, expected="PASS")

# 2. 欠損系 (Fail-Closed Check) [cite: 1, 3]
test_decision("MISSING TELEMETRY (Fail-Closed)", {
    "retry_rate": 0.1
}, expected="SILENCE")

# 3. 連鎖反応のシミュレーション (R >= R_OP)
# R = (15/10) * (600/500) * (8/5) * 1.5 = 1.5 * 1.2 * 1.6 * 1.5 = 4.32 (R_OP=1.0を突破)
test_decision("CHAIN REACTION DETECTED", {
    "retry_rate": 15.0,
    "queue_depth": 600,
    "dep_timeout_rate": 8.0
}, expected="SILENCE")

# 4. ホールド時間の検証
print("\n--- HOLD_MS VERIFICATION ---")
print("Immediately sending safe metrics during hold...")
test_decision("STILL SILENCE (Due to Hold)", {
    "retry_rate": 0.1,
    "queue_depth": 5,
    "dep_timeout_rate": 0.1
}, expected="SILENCE")
