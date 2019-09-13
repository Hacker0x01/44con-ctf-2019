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
	('The term "bladerunner" did not come from the original book. In the story from which "bladerunner" originated, bladerunners distributed illegal instruments for what?', 'surgery'), 
	('Which musician was first choice for a role in Blade Runner 2049 prior to his death? (Surname only)', 'Bowie'), 
	('The androids in Blade Runner and the original book were referred to by several different terms. What was the most commonly used in the book?', 'andy'), 
	('Cut footage from a movie by a famous director was used in the original ending of the first film. What was the director\'s surname?', 'Kubrick'),  
]

wait = 10
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
				wait *= 2
	print 'COMPLETE'
	print 'A11 7he_courage in the w0rld cannot^alter.fact.'
	print 'COMPLETE'
	print
except EOFError:
	pass
