# webhook_receiver

A minimal HTTP server that receives and logs JSON webhook payloads to stdout. No external dependencies — pure Python 3 stdlib.

## What it does

- `GET /` — health check, returns `{"status": "ok"}`
- `POST <any path>` — accepts a JSON body, logs it to stdout with source IP, timestamp, and endpoint path, then returns `{"status": "success"}`
- Non-JSON bodies return `400` and are also logged with raw content

## Stack

- Base: `python:3.7-alpine`
- No external dependencies

## Usage

### With Docker Compose

```bash
docker compose up -d --build
```

Listens on port `8000` by default.

### Custom port

```bash
WEBHOOK_PORT=9000 docker compose up -d
```

### Direct Docker run

```bash
docker build -t webhook_receiver .
docker run -p 8000:8000 webhook_receiver
```

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `WEBHOOK_PORT` | `8000` | Port to listen on |

## Example

```bash
curl -X POST http://localhost:8000/github \
  -H 'Content-Type: application/json' \
  -d '{"event": "push", "ref": "refs/heads/main"}'
```

Output in container logs:

```json
{
  "source_ip": "172.17.0.1",
  "timestamp": "2026-04-01T12:00:00.000000",
  "endpoint": "/github",
  "payload": {
    "event": "push",
    "ref": "refs/heads/main"
  }
}
```

## Notes

- HTTP access logs are suppressed by default; only payload data is printed.
- The working directory inside the container is `/tmp/current`, which is bind-mounted from the host in the compose file — useful for development but remove the volume for production use.
