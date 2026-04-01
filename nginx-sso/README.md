# nginx-sso

An OpenResty (Nginx + LuaJIT) reverse proxy that enforces Keycloak OIDC authentication and role-based access control before proxying to an upstream service.

## What it does

Every incoming request is authenticated via Keycloak OIDC. The JWT access token is verified and the user's client roles are checked. If the user is not authenticated or does not hold the required role, a `403 Forbidden` is returned. Authenticated requests are forwarded to the configured upstream.

## Stack

- Base: `openresty/openresty:1.19.9.1-5-alpine-fat`
- Auth: `lua-resty-openidc` (Lua OIDC library)
- Config: `envsubst` template rendering at startup

## Setup

### 1. TLS certificate

Generate a self-signed certificate (or provide your own):

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx-selfsigned.key \
  -out nginx-selfsigned.crt
```

### 2. Environment variables

Copy and fill in `.env`:

```bash
cp .env.example .env   # or create manually
```

| Variable | Description |
|---|---|
| `KEYCLOAK_INTERNAL_ENDPOINT` | Keycloak URL reachable from inside the container (e.g. `http://keycloak:8080`) |
| `KEYCLOAK_EXTERNAL_ENDPOINT` | Keycloak URL reachable from the browser (e.g. `https://auth.example.com`) |
| `KEYCLOAK_LOGOUT_REDIRECT_URI` | URL to redirect to after logout |
| `KEYCLOAK_REALM` | Keycloak realm name |
| `KEYCLOAK_CLIENT` | Keycloak client ID |
| `KEYCLOAK_ROLE` | Required client role for access |
| `KEYCLOAK_SECRET` | Keycloak client secret |
| `NGINX_UPSTREAM_URL` | Upstream service to proxy to (e.g. `http://myapp:3000`) |

### 3. Start

```bash
docker compose up -d --build
```

The proxy listens on `https://localhost:443`.

## Notes

- Requires Keycloak 17+ (URL format without the `/auth` prefix).
- `nginx-roles.conf.template` is a legacy reference template (Keycloak <17, plain HTTP, hardcoded upstream) — it is not used by the compose setup.
- Do not commit `.env` or certificate key files to version control.
