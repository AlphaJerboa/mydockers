#!/usr/bin/env bash

docker build . -t sqlmap

docker run -ti \
--mount type=tmpfs,destination=/root/.sqlmap/ \
--mount type=tmpfs,destination=/root/.local/share/sqlmap \
--name sqlmap \
sqlmap $@
