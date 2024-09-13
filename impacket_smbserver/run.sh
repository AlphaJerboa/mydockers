#!/usr/bin/env bash



# Docker build
RUNNING_DIR=$(dirname $(realpath $0))
docker build $RUNNING_DIR -t impacket-smbserver

# Firewall rule
#sudo iptables -I DOCKER-USER -p tcp --dport 445 -m state --state NEW -j ACCEPT
#trap "sudo iptables -D DOCKER-USER -p tcp --dport 445 -m state --state NEW -j ACCEPT" SIGINT SIGKILL

docker run -ti --rm -p 445:445 -v .:/data impacket-smbserver
