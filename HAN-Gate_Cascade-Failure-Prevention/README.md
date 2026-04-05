# App Middleware Integration (Last Resort Only)
README New v2 jp_en 26-03-06
Copyright (c) 2026 M‑Tokuni

## ⚠️ CRITICAL WARNING

**This integration method is the WEAKEST form of HAN Gate protection.**

### Why this is last resort

When you integrate HAN Gate at the application layer:

1. **Requests have already entered the system**
   - Queue pressure is already present
   - Connection pools may already be saturated
   - The cascade damage has begun

2. **Protection is delayed**
   - Ingress-level protection blocks at the gate (0-1ms)
   - App-level protection blocks after routing/parsing (10-100ms+)

3. **Incomplete coverage**
   - Only protects routes with middleware applied
   - Does not protect infrastructure layers (DNS, load balancers, connection handling)

### When to use this approach

Use app middleware ONLY if:
- You cannot modify ingress proxy configuration (Envoy/Nginx)
- You are in a legacy environment with no L7 control
- This is a temporary bridge while migrating to proper ingress integration

### Prefer Envoy or Nginx

The correct integration order:
1. **Envoy ext_authz** (RECOMMENDED)
2. **Nginx auth_request** (acceptable)
3. **App middleware** (last resort)

---

## Available implementations

### Python / Flask
See: `python_flask_middleware_2026-02-05_223015.py`

Usage:
```python
from han_middleware import han_gate_middleware

@app.route('/api/endpoint')
@han_gate_middleware('my-service')
def my_endpoint():
    return jsonify({"status": "ok"})
```

### Node.js / Express
See: `nodejs_express_middleware_2026-02-05_223015.js`

Usage:
```javascript
const hanMiddleware = require('./han_middleware');

app.use('/api', hanMiddleware('my-service'));
```

---

## Limitations (must be explicit)

1. **No pre-routing protection**
   - Request parsing, routing, and middleware chain execute before HAN check
   - This consumes resources even for requests that will be silenced

2. **Per-instance telemetry**
   - Each app instance has separate metric counters
   - Chain reactions may not be detected if distributed across many instances

3. **Language/framework coupling**
   - Requires integration code for each language
   - Maintenance burden increases

4. **Testing difficulty**
   - Harder to simulate cascade conditions in app-level tests
   - Ingress-level tests are more representative

---

## Migration path (recommended)

If you start with app middleware, plan to migrate:

**Phase 1: App middleware** (immediate safety)
- Deploy middleware to critical routes
- Gain operational experience with HAN behavior

**Phase 2: Sidecar proxy** (weeks)
- Deploy Envoy/Nginx sidecar per pod
- Move protection to sidecar
- Keep app middleware as backup

**Phase 3: Ingress consolidation** (months)
- Centralize protection at cluster ingress
- Remove app middleware
- Full Fail-Closed enforcement

---

## Final reminder

**App middleware is compromise, not solution.**

If you must use it, document:
- Why ingress integration is blocked
- Timeline for migration
- Acceptance of reduced protection

The goal is always to move protection earlier in the request path.
