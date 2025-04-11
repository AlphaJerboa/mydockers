#!/bin/sh
set -e

# Set up permissions for bind mounted volume
mkdir -p /data
chown root:root /data
chmod 755 /data
mkdir -p /data/upload
chown -R sshfsuser:sshfsgroup /data/upload
chmod 755 /data/upload

# Generate host keys if missing
if [ ! -f "/ssh/ssh_host_rsa_key" ]; then
    ssh-keygen -A 
fi

# Start SSH server
exec /usr/sbin/sshd -D -d -e -f /etc/ssh/sshd_config

