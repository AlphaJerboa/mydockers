# wfuzz

A Dockerized wrapper for [wfuzz](https://github.com/xmendez/wfuzz), a web application fuzzer.

## What it does

Runs `wfuzz` in a throw-away container. Pass arguments directly — the container entrypoint is the `wfuzz` binary. A `wfuzz.ini` is included to configure the wordlist lookup directory.

## Stack

- Base: `python:3.7-alpine`
- Tool: `wfuzz` (pip) + wordlists (cloned from GitHub at build time)
- SSL: `pycurl` compiled against OpenSSL

## Usage

```bash
# Build
docker build -t wfuzz .

# Basic directory fuzz
docker run --rm wfuzz -w /usr/share/wfuzz/wordlist/general/common.txt \
  http://target.example.com/FUZZ

# Fuzz with status code filter
docker run --rm wfuzz -w /usr/share/wfuzz/wordlist/general/common.txt \
  --hc 404 \
  http://target.example.com/FUZZ
```

## Common flags

| Flag | Description |
|---|---|
| `-w <wordlist>` | Wordlist file to use |
| `-z <type,value>` | Payload specification |
| `--hc <codes>` | Hide responses with these HTTP status codes |
| `--sc <codes>` | Show only responses with these HTTP status codes |
| `-H <header>` | Add a custom HTTP header |
| `-b <cookie>` | Set cookie |
| `-d <data>` | POST data |

Run with no arguments to see the full help:

```bash
docker run --rm wfuzz
```

## Wordlists

Wordlists are located inside the container at `/wfuzz/wordlist/` (cloned from the wfuzz GitHub repo at build time).

## Notes

- Rebuild the image to get updated wordlists.
- `dockerfile.old` and `dockerfile.old2` in this directory are legacy drafts and are not used.
