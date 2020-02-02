#!/usr/bin/env bash

IP="$1"; for i in $(seq 1 254); do (ping -c1 $IP.$i >/dev/null && echo "ON: $IP.$i" &); done
