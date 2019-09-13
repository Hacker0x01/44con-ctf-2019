#!/usr/local/bin/python

import sys
from Crypto.Cipher import AES

def main(*args):
	try:
		if len(args) != 2 or args[0] not in ('encrypt', 'load'):
			print 'AES256 HSM Tester'
			print 'USAGE: ./main encrypt [plaintext]'
			print 'USAGE: ./main load [hex key data]'
			return

		if args[0] == 'encrypt':
			key = file('key', 'rb').read().decode('hex')[:32]
			data = args[1]
			while len(data) % 32:
				data += '\0'
			obj = AES.new(key, AES.MODE_ECB)
			ct = obj.encrypt(data)
			print ''.join('%02x' % ord(c) for c in ct)
		else:
			try:
				nkey = args[1].decode('hex')
				assert len(nkey) % 4 == 0
			except:
				print 'Invalid key format. Example key: 0123456789abcdef0123456789abcdef'
				return
			with file('key', 'rb') as fp:
				key = fp.read().decode('hex')
			key = nkey + key[len(nkey):]
			key = ''.join('%02x' % ord(c) for c in key)
			with file('key', 'wb') as fp:
				fp.write(key)
			print 'Success'
	except:
		print 'Unknown error occurred'

if __name__=='__main__':
	main(*sys.argv[1:])
