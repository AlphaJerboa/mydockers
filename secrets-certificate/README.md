# secrets-certificate

A diagnostic utility for troubleshooting Docker Secrets access and file permission issues, specifically for TLS certificate/key secrets.

## What it does

Runs a `busybox` container as a specified UID, prints the content of two mounted secrets (`cert_file` and `key_file`), then drops into an interactive shell for further investigation.

## Usage

```bash
docker compose up -d && docker compose attach show-certs
```

The container will print the certificate and key, then open a shell. Exit with `Ctrl+D` or `exit`.

## Configuration

Edit `docker-compose.yml` to match your environment:

| Setting | Default | Description |
|---|---|---|
| `user` | `"1001"` | UID to run as — should match your target container's UID |
| `cert_file` source | `/etc/ssl/localcerts/server.crt` | Path to the certificate on the host |
| `key_file` source | `/etc/ssl/localcerts/server.key` | Path to the private key on the host |

## Docker user remapping (userns-remap)

If Docker user namespace remapping is enabled, the container UID is offset on the host. For example, with an offset of `100000`, container UID `1001` maps to host UID `101001`.

Fix secret file ownership on the host accordingly:

```bash
# Get the remapping offset
docker info | grep -A2 "userns-remap"
cat /etc/subuid

# Fix ownership (adjust UID/GID to match your offset)
sudo chown 101001 /etc/ssl/localcerts/server.crt
sudo chown 101001 /etc/ssl/localcerts/server.key
```

## Notes

- This service is for troubleshooting only — remove it from production environments.
- The `|| sh` fallback in the command ensures a shell is opened even if the `cat` commands fail, so you can diagnose from inside the container.
