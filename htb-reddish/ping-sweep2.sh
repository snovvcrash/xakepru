#!/usr/bin/env bash

IP="$1" # without last octet (ex. 10.10.10)
for i in $(seq 1 254); do (ping -c1 $IP.$i|grep 'bytes from'|cut -d' ' -f4|cut -d':' -f1 &); done
