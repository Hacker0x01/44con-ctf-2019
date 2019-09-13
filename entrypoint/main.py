#!/usr/local/bin/python -u
# -*- coding: UTF-8 -*-

import os
os.chdir('/app')

from getpass import getpass, getuser
import docker, mistune, pexpect, subprocess, sys, time
from multicolor import *
from model import *
from socket import *
from select import select as _select
import rooms
from mapdraw import drawMap

DEBUG = True

squad = None

client = docker.from_env()

def isRunning(image):
	assert squad is not None
	containerName = '%i-%s' % (squad.id, image)
	try:
		id = client.containers.get(containerName).short_id
		return True
	except:
		return False

def spawnOrGet(image):
	assert squad is not None
	containerName = '%i-%s' % (squad.id, image)
	try:
		id = client.containers.get(containerName).short_id
	except:
		id = client.containers.run(
			image, detach=True, remove=True, 
			name=containerName, 
			security_opt=['seccomp=' + file('seccomp_profile.json').read()], 
			ports={'23/tcp' : None}, 
			network='instances'
		).short_id
	while True:
		container = client.containers.get(id)
		try:
			ip = container.attrs['NetworkSettings']['Networks']['instances']['IPAddress']
			if ip != u'':
				break
		except:
			pass
	ip = '127.0.0.1'
	port = int(container.attrs['NetworkSettings']['Ports']['23/tcp'][0]['HostPort'])
	return port

def terminate(image):
	assert squad is not None
	containerName = '%i-%s' % (squad.id, image)
	try:
		client.containers.get(containerName).kill()
	except:
		pass

def getInput(prompt, password=False):
	value = ''
	while len(value) == 0:
		try:
			value = (getpass if password else raw_input)(prompt).strip()
		except KeyboardInterrupt:
			print
	return value.decode('utf-8')

def login():
	global squad
	print Underline(Bold('Squad Login'))
	try:
		while True:
			username = getInput('Username> ')
			password = getInput('Password> ', password=True)
			squad = Squad.login(username, password)
			if squad is None:
				print Bold('Login failed')
			else:
				print unicode(Bold('Welcome back,', squad.displayName)).encode('utf-8')
				return
	except EOFError:
		return

def register():
	global squad
	print Underline(Bold('Squad Registration'))
	try:
		while True:
			name = getInput('Public Name> ')
			if Squad.one(displayName=name) is None:
				break
			print Bold('Public name in use')
		while True:
			username = getInput('Username> ')
			if Squad.one(username=username) is None:
				break
			print Bold('Username in use')
		while True:
			password = getInput('Password> ', password=True)
			repeat = getInput('Repeat Password> ', password=True)
			if password == repeat:
				break
			print Bold('Passwords do not match')
		print 'If anyone on your squad is not registered for HackerOne already, you can do so at https://hackerone.com/users/sign_up'
		h1usernames = getInput('HackerOne usernames (comma/space separated)> ')
		squad = Squad.add(username, password, h1usernames, name)
		if squad is None:
			print Bold('Registration failed')
		if getuser() == 'guest':
			print Bold('Registration complete -- connect via SSH to play')
			squad = None
	except EOFError:
		return

def tracker():
	try:
		while True:
			style = {}
			completed = {k : 0 for k in rooms.indices}
			accessible = {k : 0 for k in rooms.indices}
			for tsquad in Squad.all():
				finished = [rooms.indices[flag.index] for flag in tsquad.foundFlags]
				for name in finished:
					completed[name] += 1
				for name in rooms.indices:
					if len(rooms.roomdeps[name]) == 0 or True in [dname in finished for dname in rooms.roomdeps[name]]:
						accessible[name] += 1

			for name in rooms.indices:
				border = Regular
				text = None
				tc = Regular
				if completed[name] != 0:
					border = Green + Bold
					tc = Bold
					text = '%i' % completed[name]
				elif accessible[name] != 0:
					border = Red + Bold
					tc = Bold
				style[name] = (border, tc, text)
			print '\033[2J\033[H'
			drawMap(style)
			print
			for name in rooms.indices:
				type, points, _, _ = rooms.rooms[name]
				print type, '-', unicode(Bold(u'¥%i' % points)).encode('utf-8'), '- %i/%i' % (completed[name], accessible[name])

			print
			leaderboard(limit=10)

			time.sleep(2)
	except KeyboardInterrupt:
		print '\033[2J\033[H'

class Renderer(mistune.Renderer):
	def __init__(self):
		mistune.Renderer.__init__(self)
		self.links = []

	def get_block(self, text):
		type = text[0]
		p = text.find(':')
		if p <= 0:
			return ('', '', '')
		l = int(text[1:p])
		t = text[p+1:p+1+l]
		return (text[p+1+l:], type, t)

	def newline(self):
		return '\n'

	def text(self, text):
		return text

	def linebreak(self):
		return '\n'

	def hrule(self):
		return '---\n'

	def header(self, text, level, raw=None):
		if level == 1:
			return '# ' + Bold(Underline(text)) + '\n\n'
		elif level == 2:
			return '## ' + Underline(text) + '\n\n'
		assert False

	def paragraph(self, text):
		return text + '\n\n'

	def list(self, text, ordered=True):
		r = ''
		i = 1
		while text:
			text, type, t = self.get_block(text)
			if type == 'l':
				r += (ordered and (('%i. ' % i) + t) or ('- ' + t)) + '\n'
				i += 1
		r += '\n'
		return r

	def list_item(self, text):
		return 'l' + str(len(str(text))) + ':' + str(text)

	def block_code(self, code, lang=None):
		return '```\n' + code + '\n```\n'

	def block_quote(self, text):
		r = ''
		for line in text.splitlines():
			r += (line and '> ' or '') + line + '\n'
		return r

	def emphasis(self, text):
		return Underline(text)

	def double_emphasis(self, text):
		return Bold(text)

	def strikethrough(self, text):
		assert False

	def codespan(self, text):
		return '`' + text + '`'

	def autolink(self, link, is_email=False):
		return link

	def link(self, link, title, text, image=False):
		self.links.append((link, text))
		return Underline('[%i] %s' % (len(self.links), text))

	def image(self, src, title, text):
		assert False

	def table(self, header, body):
		assert False

	def table_row(self, content):
		assert False

	def table_cell(self, content, **flags):
		assert False

	def footnote_ref(self, key, index):
		return '[^' + str(index) + ']'

	def footnote_item(self, key, text):
		r = '[^' + str(index) + ']:\n'
		for l in text.split('\n'):
			r += '  ' + l.lstrip().rstrip() + '\n'
		return r

	def footnotes(self, text):
		return text

def knowledgebase():
	pageStack = ['index.md']
	while True:
		renderer = Renderer()
		markdown = mistune.Markdown(renderer=renderer)
		print markdown(file('knowledgebase/' + pageStack[-1], 'r').read())

		print Bold(Underline('Navigation'))
		print Underline('0'), ':=', 'Exit' if len(pageStack) == 1 else 'Back'
		for i, (fn, text) in enumerate(renderer.links):
			print Underline(str(i + 1)),  ':=', text
		
		while True:
			try:
				target = getInput('ENTRY> ')
				try:
					target = int(target)
					if target > len(renderer.links) or target < 0:
						print 'INVALID SELECTION'
						continue
				except:
					continue
			except EOFError:
				target = 0
			break
		if target == 0:
			pageStack.pop()
			if len(pageStack) == 0:
				return
		else:
			pageStack.append(renderer.links[target - 1][0])

def dataEntry():
	print
	print Underline(Bold('Data Entry'))
	while True:
		try:
			print
			line = getInput('FLAG> ').strip()
			if not line:
				continue
			if line not in rooms.flagmap:
				print 'INVALID FLAG'
			else:
				FoundFlag.add(squad, rooms.indices.index(rooms.flagmap[line]))
				print 'FLAG ACCEPTED'
				break
		except KeyboardInterrupt:
			print
		except EOFError:
			print
			break

def systemAccess():
	style = {}
	finished = [rooms.indices[flag.index] for flag in squad.foundFlags]
	available = []
	for name in rooms.indices:
		if name in finished:
			style[name] = (Green + Bold, Bold, None)
			available.append(name)
		elif len(rooms.roomdeps[name]) == 0 or True in [dname in finished for dname in rooms.roomdeps[name]]:
			style[name] = (Red + Bold, Bold, None)
			available.append(name)
	drawMap(style)

	while True:
		try:
			print
			print Underline(Bold('System Selection'))
			for i, name in enumerate(available):
				type, points, _, _ = rooms.rooms[name]
				desc = u'%s - ¥%i%s' % (type, points, u' - COMPLETED' if name in finished else u'')
				print Underline(i), ':=', (unicode(Green(desc)) if name in finished else desc).encode('utf-8')
			print
			line = getInput('SYSTEM> ')
			try:
				select = int(line)
			except:
				select = -1
			if select < 0 or select >= len(available):
				print 'INVALID SELECTION'
			else:
				print
				_systemAccess(available[select])
				print
				break
		except KeyboardInterrupt:
			print
		except EOFError:
			print
			break

def _systemAccess(room):
	port = spawnOrGet(room)
	while True:
		sock = socket(AF_INET, SOCK_STREAM)
		try:
			sock.connect(('172.17.0.1', port))
			sock.close()
			break
		except:
			time.sleep(0.1)
	print Bold('Room entry accepted')
	time.sleep(0.5)
	#subprocess.call('telnet -E 172.17.0.1 %i' % port, shell=True)
	"""child = pexpect.spawn('telnet -E 172.17.0.1 %i' % port)
	child.expect('Trying 172.17.0.1.')
	child.expect('Connected to 172.17.0.1.')
	child.expect('Escape character is \'off\'.')
	child.interact()"""
	containerName = '%i-%s' % (squad.id, room)
	child = pexpect.spawn('docker exec -it %s /telnetlogin.sh' % containerName)
	child.interact()
	#print '\033[2J\033[H'

def systemTermination():
	print Underline(Bold('System Termination'))
	print 'If a system you are accessing is causing problems, you can terminate it here to try again.'
	finished = [rooms.indices[flag.index] for flag in squad.foundFlags]
	available = []
	for name in rooms.indices:
		if name in finished:
			available.append(name)
		elif len(rooms.roomdeps[name]) == 0 or True in [dname in finished for dname in rooms.roomdeps[name]]:
			available.append(name)
	running = [name for name in available if isRunning(name)]
	if len(running) == 0:
		print
		print Bold('NO SYSTEMS RUNNING')
		return

	while True:
		try:
			print
			for i, name in enumerate(running):
				type, points, _, _ = rooms.rooms[name]
				desc = u'%s - ¥%i' % (type, points)
				print Underline(i), ':=', desc.encode('utf-8')
			print
			line = getInput('SYSTEM> ')
			try:
				select = int(line)
			except:
				select = -1
			if select < 0 or select >= len(running):
				print 'INVALID SELECTION'
			else:
				print
				print 'Terminating...'
				terminate(running[select])
				print Bold('COMPLETE')
				break
		except KeyboardInterrupt:
			print
		except EOFError:
			print
			break

def leaderboard(limit=None):
	print Bold(Underline('Leaderboard'))
	print

	squads = [squad for squad in Squad.all() if len(squad.foundFlags)]
	psquads = []
	for squad in squads:
		points = sum(rooms.rooms[rooms.indices[flag.index]][1] for flag in squad.foundFlags)
		finalTime = max([flag.at for flag in squad.foundFlags])
		psquads.append((points, finalTime, squad))
	psquads.sort(key=lambda x: (-x[0], x[1]))
	if limit is not None:
		psquads = psquads[:limit]
	if len(psquads) == 0:
		print 'YOUR SQUAD HERE'
	for i, (points, _, squad) in enumerate(psquads):
		print '#%i -' % (i + 1), unicode(Bold(u'¥%i' % points)).encode('utf-8'), (u'- %s' % squad.displayName).encode('utf-8')

def help():
	print Bold(Underline('How To Play'))
	print 'The rules are simple: hack your way through the Tyrell Corporation and find the secrets.'
	print
	print 'Register your squad and get started!'
	print 'You can access different systems via the System Access function, and if you run into a problem with a system and want to restart it, the System Termination menu will help you with that.'
	print 'Found a secret? Enter it with the Data Entry function.'
	print 'Good luck and remember: nothing lasts forever.'
	print
	print 'SSH to 34.89.17.97 for access'
	print Bold('The game is only playable via SSH, only registration is available over telnet')
	print 'Hint: The Tyrell CEO is rather fond of a game...'

def main():
	"""r, _, __ = _select((sys.stdin, ), (), (), 0.0)
	if len(r) and sys.stdin.read(1) == '\x00':
		print 'Not very sporting to fire on an unarmed opponent. I thought you were supposed to be good. Aren\'t you the "good" man? C\'mon, Deckard. Show me what you\'re made of.'
		sys.exit(1)"""
	nonguest = [
		('Log In', login)
	]

	guest = [
		('Help', help), 
		('Register Squad', register), 
		('Squad Tracker', tracker), 
		('Leaderboard', leaderboard), 
		#('Knowledgebase', knowledgebase)
	]

	if getuser() != 'guest':
		unauthenticated = guest + nonguest
	else:
		unauthenticated = guest

	print
	print unicode(Bold(file('authbanner2.txt', 'r').read().decode('utf-8'))).encode('utf-8')

	authenticated = [
		('System Access', systemAccess), 
		('System Termination', systemTermination), 
		('Data Entry', dataEntry), 
		('Squad Tracker', tracker), 
		('Leaderboard', leaderboard), 
		#('Knowledgebase', knowledgebase)
	]

	print
	with Bold:
		print ' TYRELL CORPORATION CONFIDENTIAL SYSTEM'
		print '    UNAUTHORIZED ACCESS PROHIBITED'
		print Underline('                                        ')
	while True:
		try:
			curMenu = unauthenticated if squad is None else authenticated
			print
			if squad is not None:
				points = sum(rooms.rooms[rooms.indices[flag.index]][1] for flag in squad.foundFlags)
				print unicode(u'Current points: ' + Bold(u'¥%i' % points)).encode('utf-8')
			print Underline(Bold('Root Menu'))
			for i, (title, cb) in enumerate(curMenu):
				print Underline(i), ':=', title
			print
			line = getInput('ROOT> ')
			try:
				select = int(line)
			except:
				select = -1
			if select < 0 or select >= len(curMenu):
				print 'INVALID SELECTION'
			else:
				print
				curMenu[select][1]()
				print
		except KeyboardInterrupt:
			print
		except EOFError:
			print
			print Bold('<<Signing off>>')
			break

try:
	main()
except SystemExit:
	raise
except:
	if DEBUG:
		import traceback
		traceback.print_exc()
	else:
		print Bold('An error has occurred')
