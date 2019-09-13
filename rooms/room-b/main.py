from flask import Flask
import json, os, sys
from socket import *

app = Flask(__name__)

home = '''
<!doctype html>
<html>
	<body>
		<p><b>ERROR: UNKNOWN</b></p>
		<p>Live support unavailable.</p>
		<!-- ERROR FLAG: Fiery 7he angels F311. Deep*thunder*rolled around_their shores. -->
	</body>
</html>
'''

@app.route('/')
def hello():
	return home

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
	app.run(host='127.0.0.1', port=80)
