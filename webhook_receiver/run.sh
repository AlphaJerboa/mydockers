#!/usr/bin/env bash

# Set default port if not provided
WEBHOOK_PORT=${WEBHOOK_PORT:-8000}

# Run the container with the specified port
docker run -itd --rm \
  -p ${WEBHOOK_PORT}:${WEBHOOK_PORT} \
  -e WEBHOOK_PORT=${WEBHOOK_PORT} \
  -v .:/tmp/current \
  --name webhook_receiver \
webhook_receiver
