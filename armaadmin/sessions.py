import binascii
import os
import time

sessions = {}

def create(expires=24):
	id = binascii.hexlify(os.urandom(16)).decode()
	while id in sessions:
		id = binascii.hexlify(os.urandom(16)).decode()

	session = Session(id, expires * 3600)
	sessions[id] = session

	return session

def get(id):
	if id in sessions:
		if time.time() > sessions[id].expires + sessions[id].last:
			del sessions[id]
		else:
			return sessions[id]

	return None

def destroy(id):
	if id in sessions:
		del sessions[id]

class Session:
	def __init__(self, id, expires):
		self.id = id
		self.expires = expires
		self.last = time.time()
