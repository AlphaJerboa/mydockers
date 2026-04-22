#!/bin/bash
# Generate a random cookie secret for OAuth2 Proxy
# Requires 16, 24, or 32 bytes for AES encryption

openssl rand -base64 32
