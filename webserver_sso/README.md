# Webapp with OAuth2 Proxy

A containerized Flask application with Nginx reverse proxy and OAuth2 authentication via Keycloak.

## Architecture

```
Internet → Nginx (443) → OAuth2 Proxy (4180) → Webapp (8080)
```

| Service | Purpose |
|---------|---------|
| nginx | TLS termination, reverse proxy |
| oauth2-proxy | Authentication via Keycloak OIDC |
| webapp | Flask application |

## Prerequisites

- Docker and Docker Compose v2
- TLS certificate and key
- Keycloak client credentials

## Setup

### 1. Create required directories

```bash
mkdir -p certs secrets
```

### 2. Add TLS certificates

Place your certificates in the `certs/` directory:

```bash
cp /path/to/your/cert.crt certs/webapp.company.com.crt
cp /path/to/your/key.key certs/webapp.company.com.key
```

### 3. Configure secrets

Generate the cookie secret:

```bash
openssl rand -base64 32 > secrets/cookie_secret
chmod 600 secrets/cookie_secret
```

Add your Keycloak client secret:

```bash
echo "your-keycloak-client-secret" > secrets/client_secret
chmod 600 secrets/client_secret
```

### 4. Configure environment

Create a `.env` file (optional):

```bash
SERVER_NAME=webapp.company.com
```

### 5. Update OAuth2 Proxy configuration

Edit `docker-compose.yml` and update these values to match your environment:

- `OAUTH2_PROXY_OIDC_ISSUER_URL` - Your Keycloak realm URL
- `OAUTH2_PROXY_REDIRECT_URL` - OAuth callback URL
- `OAUTH2_PROXY_CLIENT_ID` - Keycloak client ID
- `OAUTH2_PROXY_EMAIL_DOMAINS` - Allowed email domains
- `OAUTH2_PROXY_UPSTREAMS` - Upstream application URL

## Usage

### Start services

```bash
docker compose up -d
```

### View logs

```bash
docker compose logs -f
```

### Stop services

```bash
docker compose down
```

### Rebuild webapp

```bash
docker compose build webapp
docker compose up -d webapp
```

## Security Features

- **Non-root containers**: All containers run as non-root users
- **Read-only filesystems**: Containers use immutable root filesystems
- **Dropped capabilities**: All Linux capabilities dropped except where required
- **No privilege escalation**: `no-new-privileges` enabled on all containers
- **Resource limits**: CPU and memory limits prevent resource exhaustion
- **Internal networks**: Service-to-service communication isolated from public network
- **Docker secrets**: Sensitive data stored as Docker secrets, not environment variables
- **Health checks**: All services monitored with health checks

## Network Architecture

| Network | Type | Purpose |
|---------|------|---------|
| proxy-webapp | Internal | Nginx ↔ Webapp communication |
| proxies | Internal | Nginx ↔ OAuth2 Proxy communication |
| public | Bridge | External access |

## File Structure

```
.
├── app.py                 # Flask application
├── Dockerfile             # Webapp container definition
├── docker-compose.yml     # Service orchestration
├── proxy.conf             # Nginx configuration
├── certs/
│   ├── webapp.company.com.crt
│   └── webapp.company.com.key
└── secrets/
    ├── cookie_secret      # OAuth2 Proxy cookie encryption key
    └── client_secret      # Keycloak client secret
```

## Troubleshooting

### Check service health

```bash
docker compose ps
```

### View specific service logs

```bash
docker compose logs nginx
docker compose logs oauth2-proxy
docker compose logs webapp
```

### Test webapp directly

```bash
docker compose exec webapp wget -qO- http://localhost:8080/health
```

### Validate configuration

```bash
docker compose config
```
