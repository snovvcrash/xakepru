#!/usr/bin/env bash

# Usage: ./test_waf_blacklist <IP_STR> <COOKIE_STR> <DICT_FILE>

IP=$1
COOKIE=$2
DICT=$3

G="\033[1;32m" # GREEN
R="\033[1;31m" # RED
NC="\033[0m"   # NO COLOR

for cmd in $(cat ${DICT}); do
	curl -6 -s -X POST "http://[${IP}]:80/" -H "Cookie: ${COOKIE}" -d "command=${cmd}" | grep -q "Command is not allowed."
	if [ $? -eq 1 ]; then
		echo -e "${G}${cmd}${NC} allowed"
	else
		echo -e "${R}${cmd}${NC} blocked"
	fi
done
