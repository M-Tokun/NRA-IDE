# Specification — HAN Gate Cloud Minimum Module

## 0. Purpose
Prevent cascade failure by enforcing **Fail-Closed (SILENCE)** at the ingress boundary upon detection of **chain reaction**.

## 1. Core requirements
R1. Deterministic decisions:
- Given the same inputs and config, decisions must match.

R2. Fail-Closed:
- When uncertain or telemetry is missing => SILENCE (or configurable conservative mode).

R3. Chain-reaction focus:
- React to co-occurrence (retry × queue × timeout), not single metric spikes.

R4. Integration simplicity:
- Must work with Envoy ext_authz (recommended) and Nginx auth_request.
- App middleware allowed only as last resort.

## 2. Inputs
- Telemetry snapshot per scope (service / route / cluster):
  - retry_rate (per second)
  - queue_depth (count)
  - dependency_timeout_rate (per second)
  - optional: error_rate, latency_p95 (only as supporting signals)

## 3. Configuration
- R_OP: rupture threshold (lower => safer)
- TAU: thickness per dependency class (higher => more conservative)
- HOLD_MS: minimum SILENCE hold time
- RECOVER_STEP: gradual reopen rate (optional)

## 4. Decision API
See `api/openapi.yaml`.

## 5. Acceptance criteria
A1. Under induced retry storms, system must avoid full outage propagation (no global saturation).
A2. Gate must trigger SILENCE within bounded time (e.g., < 100ms from snapshot update).
A3. When telemetry is intentionally removed, gate must enter conservative mode (SILENCE or WATCH->SILENCE).
A4. Operator can adjust R_OP and TAU without redeploy (via ConfigMap).

## 6. Non-goals
- Producing “optimal” performance
- Explaining causality narratives in real-time
- Minimizing rejections (SILENCE is permitted)

---

**Author**: M-Tokuni | GitHub: https://github.com/M-Tokun/NRA-IDE  
**Bundle**: HAN Gate (NRA/IDE) | Version: 2026-02-05_234000_FIXED
