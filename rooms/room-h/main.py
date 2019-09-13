from flask import Flask, request
import hashlib, json, os, sys
from socket import *
import sqlite3

def query(sql, commit=False):
	c = conn.cursor()
	c.execute(sql.replace('%', '%%'))
	if commit:
		conn.commit()
	else:
		return c.fetchall()

def setup():
	global conn
	conn = sqlite3.connect(':memory:')

	def sha1(data):
		return hashlib.sha1(data).hexdigest()

	conn.create_function('sha1', 1, sha1)

	query('''
	CREATE TABLE users (username text, password text)
	''', commit=True)
	query('''
	INSERT INTO users (username, password) VALUES ('eldon', sha1('chess'))
	''', commit=True)
	query('''
	CREATE TABLE flag (value text)
	''', commit=True)
	query('''
	INSERT INTO flag (value) VALUES ('I had in mind 5ome7hing.a.little m0re~radical.')
	''', commit=True)

app = Flask(__name__)

home = '''
<!doctype html>
<html>
	<body>
		<form action="/login" method="POST">
			USERNAME: <input type="text" name="username"><br>
			PASSWORD: <input type="password" name="password"><br>
			<input type="submit" value="LOG IN">
		</form>
	</body>
</html>
'''

login = '''
<!doctype html>
<html>
	<body>
		<b>%s</b>
	</body>
</html>
'''

@app.route('/')
def hello():
	return home

@app.route('/login', methods=['POST'])
def login():
	try:
		username, password = request.form['username'], request.form['password']

		data = query('SELECT username FROM users WHERE username=\'%s\' AND password=sha1(\'%s\')' % (
			username.replace('\\', '\\\\').replace('\'', '\\\''), 
			password
		))
		if len(data) == 0:
			return '<b>INVALID CREDENTIALS</b>'
		else:
			return '<b>INSUFFICIENT ACCESS FOR USER %s</b>' % data[0][0]
	except:
		return '<b>ERROR</b>'

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
	setup()
	app.run(host='127.0.0.1', port=80, threaded=False, processes=1)
