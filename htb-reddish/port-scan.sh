#!/usr/bin/env bash

IP="$1"; for port in $(seq 1 65535); do (echo '.' >/dev/tcp/$IP/$port && echo "OPEN: $port" &) 2>/dev/null; done
