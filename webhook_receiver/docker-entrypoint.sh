#!/bin/sh

# This script handles dynamic port exposure for the webhook receiver

# Update the EXPOSE directive at runtime (not actually needed but for documentation)
echo "Starting webhook receiver on port ${WEBHOOK_PORT}"

# Execute the command passed to docker run
exec "$@"
