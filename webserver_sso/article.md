# How I Added SSO to a Legacy App Without Touching Its Code

Last month, management decided that all internal applications need to authenticate against our corporate Keycloak instance. No exceptions. The problem? Half of our internal tools are legacy apps, vendor appliances, or custom scripts with basic HTTP interfaces—none of them speak OAuth.

Modifying these applications wasn't an option. Some have no source code. Others are maintained by vendors who charge five figures for "custom integrations." And rewriting that 15-year-old PHP inventory system? Not happening.

Here's how I solved it using OAuth2 Proxy as an authenticating reverse proxy.

## The Situation

We had several internal applications that needed protection:

- A Flask-based reporting tool built by a developer who left years ago
- A vendor monitoring dashboard with only basic auth
- Various internal tools that assume "if you're on the network, you're authorized"

The requirement: integrate with Keycloak using OIDC. The constraint: don't modify the applications.

## The Solution

Instead of modifying each application, I placed an authentication layer in front of them. The architecture is straightforward:

```
User → Nginx (TLS) → OAuth2 Proxy → Application
                          ↓
                      Keycloak
```

The user never reaches the application without authenticating first. OAuth2 Proxy handles the entire OIDC flow—redirects, token validation, session management—and forwards authenticated requests to the backend. The application doesn't know or care that OAuth exists.

## Step-by-Step Deployment

I'll walk through the setup using Docker Compose. This example protects a simple web application, but the pattern works for anything that speaks HTTP.

### Directory Structure

```
/opt/webapp-auth/
├── docker-compose.yml
├── proxy.conf
├── certs/
│   ├── webapp.company.com.crt
│   └── webapp.company.com.key
└── secrets/
    ├── cookie_secret
    └── client_secret
```

### 1. Generate Secrets

First, create the secrets directory and generate the cookie encryption key:

```bash
mkdir -p /opt/webapp-auth/secrets
chmod 700 /opt/webapp-auth/secrets

# Cookie secret for session encryption
openssl rand -base64 32 > /opt/webapp-auth/secrets/cookie_secret
chmod 600 /opt/webapp-auth/secrets/cookie_secret
```

Get the client secret from Keycloak (Clients → your-client → Credentials) and store it:

```bash
echo "your-client-secret-from-keycloak" > /opt/webapp-auth/secrets/client_secret
chmod 600 /opt/webapp-auth/secrets/client_secret
```

### 2. Docker Compose Configuration

```yaml
services:
  nginx:
    image: nginx:1.27-alpine
    container_name: nginx
    restart: unless-stopped
    ports:
      - "443:443"
    depends_on:
      oauth2-proxy:
        condition: service_healthy
    volumes:
      - ./proxy.conf:/etc/nginx/conf.d/default.conf:ro
    secrets:
      - cert_file
      - key_file
    networks:
      - frontend
      - backend
    # Security hardening
    read_only: true
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    tmpfs:
      - /var/cache/nginx:size=10M
      - /var/run:size=1M

  oauth2-proxy:
    image: quay.io/oauth2-proxy/oauth2-proxy:v7.5.1
    container_name: oauth2-proxy
    restart: unless-stopped
    networks:
      - frontend
      - backend
    secrets:
      - cookie_secret
      - client_secret
    environment:
      - OAUTH2_PROXY_HTTP_ADDRESS=http://0.0.0.0:4180
      # Keycloak configuration
      - OAUTH2_PROXY_PROVIDER=keycloak-oidc
      - OAUTH2_PROXY_OIDC_ISSUER_URL=https://keycloak.company.com/realms/company
      - OAUTH2_PROXY_REDIRECT_URL=https://webapp.company.com/oauth2/callback
      - OAUTH2_PROXY_CLIENT_ID=webapp
      - OAUTH2_PROXY_CLIENT_SECRET_FILE=/run/secrets/client_secret
      - OAUTH2_PROXY_COOKIE_SECRET_FILE=/run/secrets/cookie_secret
      # Restrict to company domain
      - OAUTH2_PROXY_EMAIL_DOMAINS=company.com
      # Forward user info to backend
      - OAUTH2_PROXY_SET_XAUTHREQUEST=true
      # Use PKCE for added security
      - OAUTH2_PROXY_CODE_CHALLENGE_METHOD=S256
    healthcheck:
      test: ["CMD", "wget", "-q", "-T", "5", "--spider", "http://localhost:4180/ping"]
      interval: 30s
      timeout: 10s
      retries: 3
    read_only: true
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL

  # Your legacy/custom application
  webapp:
    image: your-legacy-app:latest
    container_name: webapp
    restart: unless-stopped
    networks:
      - backend  # Not on frontend network - only accessible via proxy
    # No ports exposed - only reachable through nginx

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No internet access, no direct external access

secrets:
  cert_file:
    file: ./certs/webapp.company.com.crt
  key_file:
    file: ./certs/webapp.company.com.key
  cookie_secret:
    file: ./secrets/cookie_secret
  client_secret:
    file: ./secrets/client_secret
```

### 3. Nginx Configuration

Create `proxy.conf`:

```nginx
server {
    listen 443 ssl;
    server_name webapp.company.com;

    ssl_certificate /run/secrets/cert_file;
    ssl_certificate_key /run/secrets/key_file;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # OAuth2 Proxy endpoints
    location /oauth2/ {
        proxy_pass http://oauth2-proxy:4180;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Internal auth check endpoint
    location = /oauth2/auth {
        proxy_pass http://oauth2-proxy:4180;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_pass_request_body off;
        proxy_set_header Content-Length "";
    }

    # Protected application
    location / {
        # Authenticate every request
        auth_request /oauth2/auth;
        error_page 401 = /oauth2/sign_in;

        # Capture user identity from OAuth2 Proxy response
        auth_request_set $user $upstream_http_x_auth_request_user;
        auth_request_set $email $upstream_http_x_auth_request_email;

        # Forward user identity to backend application
        proxy_set_header X-Forwarded-User $user;
        proxy_set_header X-Forwarded-Email $email;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $host;

        # Forward to backend application
        proxy_pass http://webapp:8080;
    }

    # Health check endpoint (unauthenticated)
    location /health {
        return 200 'OK';
        add_header Content-Type text/plain;
    }
}
```

### 4. Keycloak Client Configuration

In Keycloak, create a new client:

1. **Client ID**: `webapp`
2. **Client Protocol**: `openid-connect`
3. **Access Type**: `confidential`
4. **Valid Redirect URIs**: `https://webapp.company.com/oauth2/callback`
5. **Web Origins**: `https://webapp.company.com`

Copy the client secret from the Credentials tab.

### 5. Deploy

```bash
cd /opt/webapp-auth
docker compose up -d
```

Verify everything is healthy:

```bash
docker compose ps
docker compose logs -f
```

## What Happens When a User Visits

1. User navigates to `https://webapp.company.com`
2. Nginx receives the request and calls `/oauth2/auth`
3. OAuth2 Proxy checks for a valid session cookie—none exists
4. Nginx gets a 401 and redirects to `/oauth2/sign_in`
5. OAuth2 Proxy redirects the user to Keycloak's login page
6. User authenticates with Keycloak (password, MFA, whatever's configured)
7. Keycloak redirects back to `/oauth2/callback` with an authorization code
8. OAuth2 Proxy exchanges the code for tokens, validates them, creates a session
9. User is redirected to the original URL with a session cookie
10. Nginx calls `/oauth2/auth` again—this time it succeeds
11. OAuth2 Proxy returns user info in response headers
12. Nginx forwards the request to the backend with `X-Forwarded-User` and `X-Forwarded-Email` headers
13. The application receives the request, completely unaware that OAuth happened

## Operational Notes

### Logging and Debugging

Enable verbose logging temporarily if authentication isn't working:

```yaml
environment:
  - OAUTH2_PROXY_LOGGING_LEVEL=debug
```

Check what headers are being forwarded:

```bash
docker compose exec webapp env | grep -i forward
```

### Session Management

Sessions are stored in cookies by default. For multiple replicas or longer sessions, configure Redis:

```yaml
environment:
  - OAUTH2_PROXY_SESSION_STORE_TYPE=redis
  - OAUTH2_PROXY_REDIS_CONNECTION_URL=redis://redis:6379
```

### Multiple Applications

To protect multiple applications, you have two options:

**Option A**: Separate OAuth2 Proxy per application (simpler, more isolated)

**Option B**: Shared OAuth2 Proxy with path-based routing (more complex, shared sessions)

I prefer Option A—each application gets its own stack, its own secrets, its own failure domain.

### Restricting Access

Limit access to specific groups or roles in Keycloak:

```yaml
environment:
  - OAUTH2_PROXY_ALLOWED_GROUPS=webapp-users
```

Or restrict to specific email addresses:

```yaml
environment:
  - OAUTH2_PROXY_AUTHENTICATED_EMAILS_FILE=/config/allowed_emails.txt
```

### Health Checks and Monitoring

The `/ping` endpoint on OAuth2 Proxy returns 200 when healthy. Monitor it:

```bash
curl -s http://localhost:4180/ping
```

### Backup and Recovery

Critical files to backup:

- `docker-compose.yml`
- `proxy.conf`
- `secrets/` directory

The session cookies are encrypted with `cookie_secret`. If you lose it, all users will need to re-authenticate—annoying but not catastrophic.

## Security Considerations

**Network isolation is critical.** The backend application must not be reachable except through Nginx. The `internal: true` network setting prevents direct access.

**Header spoofing.** The application trusts `X-Forwarded-User`. An attacker who can reach the application directly could spoof this header. Network isolation prevents this.

**Secret rotation.** Rotate `client_secret` and `cookie_secret` periodically. After rotating `cookie_secret`, all sessions are invalidated.

**Keep images updated.** OAuth2 Proxy and Nginx receive security updates. Pin to specific versions but update regularly:

```bash
docker compose pull
docker compose up -d
```

## Conclusion

This pattern has saved me countless hours. Instead of begging vendors for OAuth support or rewriting legacy applications, I deploy an authenticating proxy in front of them. The application doesn't change. The users get SSO. Security is happy.

The same approach works for:

- Legacy PHP/Java/whatever applications
- Vendor appliances with web interfaces
- Internal tools that were never meant to be exposed
- Anything that speaks HTTP

One proxy configuration, and suddenly that ancient application is part of your modern SSO infrastructure.
