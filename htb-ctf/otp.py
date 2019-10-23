#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Использование: python3 otp.py

import time
from datetime import datetime
from subprocess import check_output

import requests

URL = 'http://10.10.10.122'

while True:
	kali = datetime.utcnow()
	server = datetime.strptime(requests.head(URL).headers['Date'], '%a, %d %b %Y %X %Z')
	offset = int((server - kali).total_seconds())

	cmd = [
		'stoken',
		'--token=285449490011357156531651545652335570713167411445727140604172141456711102716717000',
		'--pin=0000',
		f'--use-time={"%+d" % offset}'
	]

	print(check_output(cmd).decode().strip(), end='\r')
	time.sleep(1)
