from flask import Flask, request
import base64, json, os, sys
from socket import *
import cPickle as pickle

app = Flask(__name__)

home = '''
<!doctype html>
<html>
	<body>
		<b>%s</b>
	</body>
</html>
'''

@app.route('/')
def hello():
	try:
		pickle.loads(base64.decodestring(file('.a', 'r').read().replace('%', '').replace('~', '').strip() + '=='))
		return home % 'SUCCESS'
	except:
		return home % 'DESERIALIZATION FAILED'

if __name__ == "__main__":
	if os.fork() > 0:
		while True:
			try:
				sock = socket(AF_INET, SOCK_STREAM)
				sock.connect(('127.0.0.1', 80))
				break
			except:
				pass
		sys.exit(0)
	os.setsid()
	os.umask(0)
	if os.fork() > 0:
		sys.exit(0)
	app.run(host='127.0.0.1', port=80, threaded=False, processes=1)
