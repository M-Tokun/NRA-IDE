# Runbook — HAN Gate (Operator Manual)

## 1) What operators do (and do not do)

### You do
- Confirm the gate is deployed and integrated at ingress.
- Monitor **SILENCE rate** and **chain-reaction signals**.
- Lower R_OP / increase TAU if you want it safer.
- Review event logs after incidents.

### You do NOT
- "Fix latency" by adding retries.
- Add ML/autotuning feedback into the gate.
- Bypass the gate during cascade onset.
- Use average latency as primary trigger.

## 2) Daily checks
- Gate health: `/healthz` returns OK
- Decision endpoint reachable from proxy
- ConfigMap applied: R_OP / TAU values match intended

## 3) Common incident patterns & expected behavior

### Pattern A: dependency timeouts start rising, retries follow
Expected:
- Gate enters WATCH then SILENCE for affected route/service.
- Upstream load stops increasing (stabilizes).

### Pattern B: queue depth spikes with retry storm
Expected:
- SILENCE quickly (fail-closed).
- Once retries naturally drop, RECOVER can reopen gradually.

## 4) How to validate (curl)
Assuming gate service at `han-gate.default.svc.cluster.local:8080`

- Health:
  curl -s http://han-gate.default.svc.cluster.local:8080/healthz

- Decision:
  curl -s -X POST http://han-gate.default.svc.cluster.local:8080/v1/decision \
    -H 'content-type: application/json' \
    -d '{"scope":{"service":"checkout","route":"/api/pay"},"telemetry":{"retry_rate":12,"queue_depth":480,"dep_timeout_rate":7}}'

## 5) If the gate is SILENCE-ing "too much"

### SILENCE rate guidelines (design review, not operational decision)
- **Normal**: 0-1% of requests
- **Caution zone**: 1-5% (monitor closely)
- **Requires design review**: >5%

### Adjustment patterns (weekly design review, not real-time)
**To make it less conservative (allow more traffic)**:
- Increase R_OP: 1.0 → 1.5 (higher threshold)
- Decrease TAU: 1.5 → 1.0 (thinner safety margin)

**Important**: These are **design decisions**, not operational reactions.
- Adjust during scheduled reviews (weekly/bi-weekly)
- Do NOT adjust reactively during incidents
- Document each change with rationale

**Before adjusting**:
- Confirm telemetry isn't missing (missing => conservative).
- Check if SILENCE prevented actual cascade (review logs).
- Verify upstream services are healthy (not masking real issues).

### How to check logs
```bash
# View recent SILENCE decisions
kubectl logs -n han deployment/han-gate | grep SILENCE | tail -20

# Check telemetry values that triggered SILENCE
kubectl logs -n han deployment/han-gate --tail=100 | jq 'select(.decision=="SILENCE")'
```

## 6) If the gate never SILENCEs (unsafe)
- Lower R_OP (more conservative).
- Increase TAU for deep dependencies.
- Confirm proxy integration (ext_authz/auth_request) is actually calling the gate.

## 7) Rollback strategy
- Disable ext_authz/auth_request callout (proxy config rollback).
- Keep the gate deployed (do not delete); rollback should be reversible.

## 8) Weekly design review checklist
- [ ] SILENCE rate within normal range (0-1%)?
- [ ] Any actual cascades prevented this week?
- [ ] Any false positives (SILENCE when safe)?
- [ ] Telemetry collection working on all proxies?
- [ ] R_OP / TAU adjustment needed?

**Reminder:** Early SILENCE is safer than late heroics.

---

**Author**: M-Tokuni | GitHub: https://github.com/M-Tokun/NRA-IDE  
**Bundle**: HAN Gate (NRA/IDE) | Version: 2026-02-05_234000_FIXED
