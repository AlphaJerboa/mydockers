# impacket_smbserver

A Dockerized SMB server using Impacket's `smbserver.py`, based on Kali Linux. Useful for receiving file transfers during penetration tests or CTF challenges.

## What it does

Starts an unauthenticated SMB share named `share` pointing to `/data` inside the container, with SMBv2 support enabled.

## Stack

- Base: `kalilinux/kali-last-release`
- Tool: `impacket-scripts` (Kali package)

## Usage

```bash
# Build
docker build -t impacket_smbserver .

# Run — mount a local directory as the share
docker run --rm -it \
  -p 445:445 \
  -v "$(pwd)/share:/data" \
  impacket_smbserver
```

The share will be accessible at `\\<host-ip>\share`.

## Connecting from a Windows client

```cmd
net use Z: \\<host-ip>\share
```

## Notes

- Runs as a non-root `smbserver` user inside the container.
- Requires port 445 to be available on the host. On Linux, this port may already be in use by the system's Samba service.
- This is an unauthenticated share — intended for lab/testing environments only.
