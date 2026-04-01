# secrets

A minimal demo of [Docker Secrets](https://docs.docker.com/engine/swarm/secrets/) using a file-based secret.

## What it does

Mounts a secret (`app_secret`) from a local file (`app_pass.txt`) into a `debian:buster-slim` container. The secret is available inside the container at `/run/secrets/app_secret`.

## Usage

```bash
# Create the secret file
echo "mysecretpassword" > app_pass.txt

# Start the container
docker compose up -d

# Attach and inspect the secret
docker exec -it test_secrets bash
cat /run/secrets/app_secret
```

## How it works

`docker-compose.yml` declares a `file:`-based secret:

```yaml
secrets:
  app_secret:
    file: ./app_pass.txt
```

Docker mounts the file content as a read-only tmpfs at `/run/secrets/app_secret` inside the container.

## Notes

- `app_pass.txt` contains the actual secret value — do not commit real passwords to version control.
- File-based secrets work with both `docker compose` and Docker Swarm. In Swarm mode, secrets are distributed securely across nodes.
