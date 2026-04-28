# App Middleware (Last Resort Only)

Use this only if you cannot control ingress proxy configuration.

## Pattern

- A lightweight middleware calls the gate with local telemetry snapshot.

- If SILENCE => return a neutral response early (e.g., 204 / fixed token).

- Avoid retries.

## Warning

Putting the gate in the app layer weakens protection:

- requests already entered the system

- queues may already be stressed

Prefer Envoy/Nginx whenever possible.
