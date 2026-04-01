# sqlmap

A Dockerized wrapper for [sqlmap](https://github.com/sqlmapproject/sqlmap), an automatic SQL injection and database takeover tool.

## What it does

Runs `sqlmap` in a throw-away container. Pass arguments directly — the container entrypoint is `sqlmap.py`.

## Stack

- Base: `alpine:latest`
- Tool: `sqlmap` (cloned from GitHub at build time)

## Usage

```bash
# Build
docker build -t sqlmap .

# Basic scan
docker run --rm sqlmap -u "http://target.example.com/page?id=1"

# Run with a wizard (interactive)
docker run --rm -it sqlmap --wizard
```

## Common flags

| Flag | Description |
|---|---|
| `-u` | Target URL |
| `--dbs` | Enumerate databases |
| `--tables` | Enumerate tables |
| `--dump` | Dump table contents |
| `--level` | Test level (1–5) |
| `--risk` | Risk level (1–3) |
| `--batch` | Non-interactive mode (use defaults) |
| `-p` | Specify parameter to test |

Run with no arguments to see the full help:

```bash
docker run --rm sqlmap
```

## Notes

- The image clones sqlmap from GitHub at build time — rebuild the image to get the latest version.
- Use `--batch` to avoid interactive prompts in automated workflows.
