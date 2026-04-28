# Envoy Integration — ext_authz (Recommended)

## Goal

Use Envoy external authorization filter to call HAN Gate per request and:

- PASS => allow request

- SILENCE => deny or optionally return a neutral response

## Minimal example (HTTP filter)

This is a reference snippet. Your platform team should adapt clusters/listeners.

```yaml

http_filters:

- name: envoy.filters.http.ext_authz

  typed_config:

    "@type": type.googleapis.com/envoy.extensions.filters.http.ext_authz.v3.ExtAuthz

    transport_api_version: V3

    grpc_service:

      envoy_grpc:

        cluster_name: han_gate_grpc

    failure_mode_allow: false   # fail-closed

    include_peer_certificate: false

- name: envoy.filters.http.router

```

## Notes

- `failure_mode_allow: false` is critical (Fail-Closed).

- You can scope it per route (recommended) to avoid silencing everything.

- Response handling:

  - Deny with 403/429, or

  - Map to 204 / fixed token response (policy choice)

## Required endpoints

- gRPC ext_authz or HTTP ext_authz equivalent.

This bundle ships an HTTP JSON gate; platform team can wrap it with a thin gRPC adapter if needed.
