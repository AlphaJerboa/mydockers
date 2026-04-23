# Container Collection

A collection of Dockerized tools and services for development, security testing, and infrastructure.

## Containers

### Infrastructure & Services

| Container | Description | Base Image |
|-----------|-------------|------------|
| [nginx-sso](./nginx-sso/) | Nginx reverse proxy with Keycloak OIDC authentication | openresty/openresty (Alpine) |
| [sshfs](./sshfs/) | Hardened SFTP server with chroot and key-only auth | alpine:3.19 |
| [webhook_receiver](./webhook_receiver/) | Minimal HTTP server for receiving webhook payloads | python:3.7-alpine |
| [desktop](./desktop/) | Virtual XFCE4 desktop accessible via noVNC | ubuntu:22.04 |

### Security Tools

| Container | Description | Base Image |
|-----------|-------------|------------|
| [sqlmap](./sqlmap/) | Automatic SQL injection and database takeover tool | alpine:latest |
| [smbmap](./smbmap/) | SMB share enumeration and permissions scanner | python:latest |
| [wfuzz](./wfuzz/) | Web application fuzzer with wordlists | python:3.7-alpine |
| [impacket_smbserver](./impacket_smbserver/) | SMB server for file transfers (pentesting/CTF) | kalilinux/kali-last-release |

### Utilities & Examples

| Container | Description | Base Image |
|-----------|-------------|------------|
| [secrets](./secrets/) | Demo of Docker secrets with file-based secrets | debian:buster-slim |
| [secrets-certificate](./secrets-certificate/) | Diagnostic tool for secrets permissions troubleshooting | busybox |

## Quick Start

Each container has its own README with specific usage instructions. General pattern:

```bash
cd <container-name>
docker compose up -d --build
```

## License

See individual container directories for licensing information.
