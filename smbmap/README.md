# smbmap

A Dockerized wrapper for [smbmap](https://github.com/ShawnDEvans/smbmap), a tool for enumerating SMB shares and permissions.

## What it does

Runs `smbmap` in a throw-away container. Pass arguments directly — the container entrypoint is `smbmap.py`.

## Stack

- Base: `python:latest`
- Tool: `smbmap` (pip)

## Usage

```bash
# Build
docker build -t smbmap .

# Run (arguments passed directly to smbmap)
docker run --rm smbmap -H <target-ip>

# Authenticated enumeration
docker run --rm smbmap -H <target-ip> -u <username> -p <password>

# List shares with read/write permissions
docker run --rm smbmap -H <target-ip> -u <username> -p <password> -R
```

## Common flags

| Flag | Description |
|---|---|
| `-H` | Target host IP |
| `-u` | Username |
| `-p` | Password |
| `-d` | Domain |
| `-R` | Recursively list directories |
| `--download` | Download a file from a share |
| `-x` | Execute a command |

Run with no arguments to see the full help:

```bash
docker run --rm smbmap
```
