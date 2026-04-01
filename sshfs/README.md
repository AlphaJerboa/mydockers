# sshfs

A hardened SFTP-over-SSH server based on Alpine Linux. Designed for secure file transfer with key-only authentication, chroot jail, and a minimal attack surface.

## What it does

Runs an OpenSSH server configured exclusively for SFTP (no shell, no TCP/X11 forwarding). The `sshfsuser` is chrooted to `/data`. Mount the exposed SFTP share locally using `sshfs`.

## Stack

- Base: `alpine:3.19`
- Protocol: SFTP via `internal-sftp` (OpenSSH)
- Port: `2222`

## Setup

### 1. Prepare the data directory

The chroot directory must be owned by root:

```bash
sudo chown root:root ./data
sudo mkdir -p ./data/upload
sudo chown 1000:1000 ./data/upload
```

### 2. Add your public key

Place your SSH public key in `authorized_keys`:

```bash
cp ~/.ssh/id_rsa.pub authorized_keys
```

### 3. Start the server

```bash
docker compose up -d --build
```

## Client usage

```bash
mkdir /mnt/sshfs

sshfs -v \
  -o ssh_command='ssh -T' \
  -o PubkeyAuthentication=yes \
  -o IdentityFile=~/.ssh/<your_private_key> \
  -p 2222 \
  sshfsuser@127.0.0.1:/ /mnt/sshfs
```

## Security features

- Key-only authentication (no passwords)
- Non-root user (`sshfsuser`, UID 1000)
- Chroot to `/data`
- `ForceCommand internal-sftp` — no shell access
- No TCP forwarding, no X11 forwarding, no tunneling, no TTY
- `no-new-privileges` and `read_only: true` in compose
- Healthcheck: `ss -tnl | grep -q :2222`
