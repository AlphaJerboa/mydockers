# desktop

A Dockerized XFCE4 virtual desktop accessible via VNC, based on [Bytebot](https://github.com/bytebot-ai/bytebot).

## What it does

Runs a full graphical desktop environment (Ubuntu 22.04 + XFCE4) inside a container, accessible over VNC on port 5900. Includes Firefox ESR, common utilities, and Python 3.

## Stack

- Base: `ubuntu:22.04`
- Desktop: XFCE4 + Xvfb + x11vnc
- Remote access: noVNC + websockify
- Process manager: supervisord

## Usage

```bash
docker compose up -d --build
```

Then connect with any VNC client to `127.0.0.1:5900`.

**Note:** port 5900 is bound to `127.0.0.1` only (localhost). Use an SSH tunnel or adjust the bind address in `docker-compose.yml` for remote access.

## Service boot order (supervisord)

1. `dbus` — system message bus
2. `xvfb` — virtual framebuffer (display `:0`, 1280×960)
3. `xfce4` — desktop environment
4. `x11vnc` — VNC server on port 5900

## Notes

- `privileged: true` is set in the compose file — required for the desktop environment to function properly.
- The container runs as a non-root `user` for desktop processes; supervisord itself runs as root.
