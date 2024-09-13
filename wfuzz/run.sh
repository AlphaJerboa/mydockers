#!/usr/bin/env bash

if [[ -z "$1" ]] 
then
  RUNNING_DIR=$(dirname $(realpath $0))

  docker build $RUNNING_DIR -t wfuzz
  docker run --rm wfuzz -h

  docker run --rm --entrypoint "ls" wfuzz -R wordlist

  cat << EOF
Usage: $0 -c -w wordlist/general/common.txt -u https://<url>/WFUZZ

# OR
docker run --rm -v ~/pentest/wordlists/:/tmp wfuzz -c -w /tmp/api_entry_points.txt https://<url>/WFUZZ
EOF

else
  docker run --rm wfuzz $@
fi
