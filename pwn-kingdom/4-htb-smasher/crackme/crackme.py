from Crypto.Cipher import AES
import base64
import sys
import os

unbuffered = os.fdopen(sys.stdout.fileno(), 'w', 0)

def w(text):
	unbuffered.write(text+"\n")

class InvalidPadding(Exception):
	pass

def validate_padding(padded_text):
	return all([n == padded_text[-1] for n in padded_text[-ord(padded_text[-1]):]])


def pkcs7_pad(text, BLOCK_SIZE=16):
	length = BLOCK_SIZE - (len(text) % BLOCK_SIZE)
	text += chr(length) * length
	return text


def pkcs7_depad(text):
	if not validate_padding(text):
		raise InvalidPadding()
	return text[:-ord(text[-1])]


def encrypt(plaintext, key):
	cipher = AES.new(key, AES.MODE_CBC, "\x00"*16)
	padded_text = pkcs7_pad(plaintext)
	ciphertext = cipher.encrypt(padded_text)
	return base64.b64encode(ciphertext)


def decrypt(ciphertext, key):
	cipher = AES.new(key, AES.MODE_CBC, "\x00"*16)
	padded_text = cipher.decrypt(base64.b64decode(ciphertext))
	plaintext = pkcs7_depad(padded_text)
	return plaintext


w("[*] Welcome to AES Checker! (type 'exit' to quit)")
w("[!] Crack this one: irRmWB7oJSMbtBC4QuoB13DC08NI06MbcWEOc94q0OXPbfgRm+l9xHkPQ7r7NdFjo6hSo6togqLYITGGpPsXdg==")
while True:
	unbuffered.write("Insert ciphertext: ")
	try:
		aes_hash = raw_input()
	except:
		break
	if aes_hash == "exit":
		break
	try:
		decrypt(aes_hash, "Th1sCh4llang31SInsane!!!")
		w("Hash is OK!")
	except InvalidPadding:
		w("Invalid Padding!")
	except:
		w("Generic error, ignore me!")
