--- START OF FILE README.md ---

HAN Gate (NRA/IDE) — Cloud Minimum Module Bundle
Bundle timestamp (JST): 2026-02-05 22:08:25
This package provides a minimum deployable module for cloud platforms that prevents cascade failure by enforcing Fail-Closed (SILENCE) at the ingress boundary when a chain reaction is detected (retry × queue × timeout/dependency amplification).
What this is (for non-specialists)
This is not a latency optimizer.
This is not a routing “best path” engine.
This is a safety gate that automatically cuts new traffic (or returns a safe fixed response) before a cascade spreads.
If you can tolerate partial/temporary silence, you can avoid full-system rupture.
Who should read what
Executives / Product owners: read this README and the “Why SILENCE is acceptable” note below.
SRE / Platform: see docs/SPEC.md, docs/RUNBOOK.md, deploy/k8s/han-gate.yaml.
Network / Edge:
Envoy: integrations/envoy_ext_authz.md (recommended)
Nginx: integrations/nginx_auth_request.md
App teams (last resort only): integrations/app_middleware.md
Quick start (Kubernetes)
Deploy the gate:
Apply deploy/k8s/han-gate.yaml
Integrate at the edge:
Prefer Envoy ext_authz (recommended)
Or Nginx auth_request
Validate:
Run the curl examples in docs/RUNBOOK.md
Tune safely:
Lower R_OP to fail-closed earlier (safer)
Increase TAU_* for deeper dependencies (safer)
Operating principle in one line (what operators need to know)
When the chain reaction begins, the gate automatically SILENCEs at the ingress. Humans do not “decide the moment.”
Why SILENCE is acceptable (business framing)
During cascade onset, “trying harder” (retries / reconnects / aggressive autoscaling) often increases pressure and spreads failure.
This gate chooses bounded silence over unbounded rupture:
Bounded silence: some requests are refused/neutralized temporarily
Rupture: widespread outage, data corruption risk, long recovery, brand damage
This module is intentionally conservative: it may stop traffic earlier than a human would.
That is the point.
What you get in this bundle
gate/han_gate_service.py — minimal gate service (PASS / SILENCE decision API)
api/openapi.yaml — API contract for the gate
deploy/k8s/han-gate.yaml — minimal Kubernetes deployment/service/config
docs/ARCHITECTURE.md — diagrams (text-based) + placement blueprint
docs/SPEC.md — specification / requirements / acceptance criteria
docs/RUNBOOK.md — operator manual (what to do, what not to do)
integrations/ — Envoy / Nginx / App integration notes
Safety notes (must be explicit)
This is Fail-Closed by design. In doubt, it SILENCEs.
Do not add “smart optimization” feedback loops (ML routing, reward tuning) into the gate.
Keep the gate logic deterministic and auditable.
Credits & Contact
Author: M-Tokuni (Masatoshi Tokunaga)
Handle: 灯台 (Toudai / Lighthouse)
Specialty: Ritsukan Circular Axiom (NRA) / Intensional Dynamics Engine (IDE)
Links
GitHub: https://github.com/M-Tokun/NRA-IDE
Twitter/X: https://x.com/m_tokuni

Project Information
Theoretical Foundation: Ritsukan Circular Axiom (NRA)
Implementation Framework: Intensional Dynamics Engine (IDE)
Purpose: Structural safety mechanism designed to mitigate cascade failures in complex distributed systems (including high-reliability contexts).
License: MIT License (See LICENSE.txt)
⚠️ DISCLAIMER & LIMITATION OF LIABILITY
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.
While this software is designed based on the Ritsukan Circular Axiom to prevent cascade failures, the author (M-Tokuni) DOES NOT guarantee safety or uptime in all environments.
Regarding High-Risk Systems (Medical, Autonomous Driving, etc.):
This software serves as a logic mechanism only. It is NOT a certified safety component for life-critical applications. The ultimate responsibility for safety validation, fail-over testing, regulatory compliance, and operational decisions rests SOLELY with the user/operator. Do not rely on this software alone for human safety.
By using this software, you agree that the author shall not be liable for any claim, damages, or other liability arising from its use.
Documentation: KEN (NRA/IDE Research Assistant)
Bundle Version: 2026-02-05_235000_HARDENED
Last Updated: 2026-02-05 23:55:00 JST