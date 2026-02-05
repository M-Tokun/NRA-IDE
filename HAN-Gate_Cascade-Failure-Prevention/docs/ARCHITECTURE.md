# Architecture Blueprint — HAN Gate Minimum Module

## 1) Placement (recommended)
Put the gate at the **L7 ingress boundary** so it can stop *new* traffic quickly.

```
Client
  |
  |  (HTTP/gRPC)
  v
[ Edge Proxy: Envoy / Nginx ]  ----->  [ Upstream Services ]
        |
        |  ext_authz / auth_request
        v
   [ HAN Gate Service ]
        |
        v
  (Decision: PASS / SILENCE)
```

### Why ingress
Cascade damage grows via:
- retries
- reconnect storms
- queue amplification
- dependency timeouts

Ingress is the earliest point to cut the chain.

## 2) Minimal telemetry inputs (chain-reaction only)
The gate should react to **co-occurrence**, not single metrics.

- retry_rate ↑
- queue_depth ↑
- dependency_timeouts ↑

Co-occurrence => chain reaction onset.

## 3) Output semantics
- PASS: allow request to continue
- SILENCE: deny or return a neutral response (configured at proxy)

## 4) State model (operator-friendly)
This module is a finite-state gate.

```
NORMAL  ->  WATCH  ->  SILENCE
   ^          |          |
   |          v          v
   +-------- RECOVER <---+
```

- NORMAL: no chain reaction
- WATCH: early signals; more conservative
- SILENCE: fail-closed; stop new traffic
- RECOVER: gradual reopen (optional)

## 5) What is intentionally NOT included
- “Best” routing
- latency optimization
- ML / adaptive reward tuning
- auto-remediation scripts

Those can reintroduce runaway feedback.

---

**Author**: M-Tokuni | GitHub: https://github.com/M-Tokun/NRA-IDE  
**Bundle**: HAN Gate (NRA/IDE) | Version: 2026-02-05_234000_FIXED
