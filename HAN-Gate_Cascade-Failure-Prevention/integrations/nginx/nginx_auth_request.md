# Nginx Integration — auth_request

## Goal
Call HAN Gate before proxying upstream.

## Minimal example
```nginx
location /api/ {
  auth_request /_han_auth;
  proxy_pass http://upstream_backend;
}

location = /_han_auth {
  internal;
  proxy_pass http://han-gate.default.svc.cluster.local:8080/v1/nginx_auth;
  proxy_pass_request_body off;
  proxy_set_header Content-Length "";
  proxy_set_header X-Original-URI $request_uri;
}
```

## Fail-Closed
- If the auth subrequest fails, treat it as deny (default safe stance).
- Ensure timeouts are short to avoid blocking.

## Response policy
- 2xx => PASS
- 401/403 => SILENCE (deny)
- You can rewrite deny to 204 if you want “neutral silence.”
