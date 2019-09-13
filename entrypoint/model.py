import math, hashlib, json, os, random
from datetime import datetime, timedelta
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.types import *
from metamodel import *
import bcrypt

@Model
def FoundFlag():
	squad_id = ForeignKey(Integer, 'Squad.id')
	index = Integer
	at = DateTime

	@staticmethod
	def add(squad, index):
		if FoundFlag.one(squad_id=squad.id, index=index):
			return False
		with transact:
			FoundFlag.create(
				squad_id=squad.id, 
				index=index, 
				at=datetime.now()
			)
			return True

@Model
def Event():
	squad_id = ForeignKey(Integer, 'Squad.id')
	at = DateTime
	message = Unicode

	@staticmethod
	def add(squad, message):
		with transact:
			Event.create(
				squad_id=squad.id, 
				message=message, 
				at=datetime.now()
			)

@Model
def Squad():
	username = Unicode(255)
	password = String(88)
	displayName = Unicode(255)
	h1usernames = Unicode(255)
	
	foundFlags = FoundFlag.relation(backref='squad')
	events = Event.relation(backref='squad')
	
	@staticmethod
	def hash(password):
		return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))

	@staticmethod
	def checkHash(hash, password):
		try:
			hash = hash.encode('utf-8')
			return bcrypt.hashpw(password.encode('utf-8'), hash) == hash
		except:
			return False

	@staticmethod
	def add(username, password, h1usernames, displayName):
		if Squad.one(username=username) or Squad.one(displayName=displayName):
			return None
		with transact:
			return Squad.create(
				username=username,
				password=Squad.hash(password),
				h1usernames=h1usernames, 
				displayName=displayName
			)

	@staticmethod
	def login(username, password):
		squad = Squad.one(username=username)
		if squad is not None and Squad.checkHash(squad.password, password):
			return squad
		return None

db = 'postgresql://postgres:b806024fcf9155c55f19377db0a450d7@db/postgres'
#db = 'sqlite:///sqlite.db'

@setup(db)
def init():
	pass
