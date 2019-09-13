#!/usr/local/bin/python

import time

def getInput(prompt, password=False):
	value = ''
	while len(value) == 0:
		try:
			value = (getpass if password else raw_input)(prompt).strip()
		except KeyboardInterrupt:
			print
	return value.decode('utf-8')

questions = [
	('What is the surname of the actor who almost played Deckard?', 'Hoffman'), 
	('Which early film was a direct inspiration for the urban setting of the first film?', 'Metropolis'), 
	('What are the initials of the creator of the artificial language?', 'EJO')
]

wait = 5
try:
	for q, a in questions:
		while True:
			print q
			value = getInput('ANSWER> ')
			if value.strip().lower() == a.strip().lower():
				print 'CORRECT'
				print
				break
			else:
				print 'INCORRECT -- %i second penalty' % wait
				print
				time.sleep(wait)
				wait *= 1.5
	print 'COMPLETE'
	print 'Chew,^if 0nly y0u could_see_what I\'ve se3n with your ey3s...'
	print 'COMPLETE'
	print
except EOFError:
	pass
