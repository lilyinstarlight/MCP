#!/usr/bin/python
round = 0
teams = {}
num_players = 0
players = {}
zones = {}

class Team:
	def __init__(self, name):
		self.name = name
		self.score = 0
		self.players = {}
		self.positions = []

class Player:
	def __init__(self, name, screenname, ip):
		self.name = name
		self.screenname = screenname
		self.ip = ip
		self.score = 0
		self.alive = False

class Zone:
	def __init__(self, name, type, x, y, size, growth=0, xdir=0, ydir=0, interactive=None, r=None, g=None, b=None, target_size=None, rubber=None, player=None, owner=None, command=None):
		self.name = name
		self.type = type
		self.x = x
		self.y = y
		self.size = size
		self.growth = growth
		self.xdir = xdir
		self.ydir = ydir

		if interactive != None:
			self.interactive = interactive

		if r != None and g != None and b != None:
			self.r = r
			self.g = g
			self.b = b

		if target_size != None:
			self.target_size = target_size

		if type == "rubber":
			self.rubber = rubber

		if type == "zombie":
			self.player = player

		if type == "zombieOwner":
			self.player = player
			self.owner = owner

		if type == "target" and command != None:
			addCommand(command)

	def __del__(self):
		self.changeSize(0)

	def addCommand(command):
		if zone.type == "target":
			armagetron.sendCommand("SET_TARGET_COMMAND " + self.name + " " + command)

	def changeColor(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b
		armagetron.sendCommand("SET_ZONE_COLOR " + self.name + " " + r + " " + g + " " + b)

	def changeExpansion(self, growth):
		self.growth = growth
		armagetron.sendCommand("SET_ZONE_EXPANSION " + self.name + " " + growth)

	def changePosition(self, x, y):
		self.x = x
		self.y = y
		armagetron.sendCommand("SET_ZONE_POSITION " + self.name + " " + x + " " + y)

	def changeSize(self, size, growth=None):
		self.size = size
		command = "SET_ZONE_RADIUS" + self.name + " " + size

		if growth != None:
			command += " " + growth

		armagetron.sendCommand(command)

	def changeSpeed(self, xdir, ydir):
		self.xdir = xdir
		self.ydir = ydir
		armagetron.sendCommand("SET_ZONE_SPEED " + self.name + " " + xdir + " " + ydir)

def getTeam(name):
	if name in teams:
		return teams[name]

def getPlayer(name):
	if name in players:
		return players[name]

def getZone(name):
	if name in zones:
		return zones[name]

def createZone(name, type, x, y, size, growth=0, xdir=0, ydir=0, interactive=None, r=None, g=None, b=None, target_size=None, rubber=None, player=None, owner=None, targetcommand=None):
	command = "SPAWN_ZONE n " + name + " " + type

	if type == "zombie":
		if player == None:
			return None
		command += " " + player

	if type == "zombieOwner":
		if player == None or owner == None:
			return None
		command += " " + player + " " + owner

	command += " " + x + " " + y + " " + size + " " + growth + " " + xdir + " " + ydir

	if type == "rubber":
		if rubber == None:
			return None
		command += rubber

	if interactive != None:
		command += " " + interactive

	if r != None and g != None and b != None:
		command += " " + r + " " + g+ " " + b

	if target_size != None:
		command += " " + target_size

	armagetron.sendCommand(command)

	zones[name] = Zone(name, type, x, y, size, growth, xdir, ydir, interactive, r, g, b, target_size, rubber, player, owner, targetcommand)

	return zones[name]

#Ladderlog commands

def newRound(command):
	round += 1
	zones = {}

def newMatch(command):
	round = 1
	for team in teams:
		team.score = 0
	for player in players:
		player.score = 0

def roundScore(command):
	if command[2] in players:
		players[command[2]].score += command[1]

def roundScoreTeam(command):
	if command[2] in teams:
		teams[command[2]].score += command[1]

def teamCreated(command):
	teams[command[1]] = Team(command[1])

def teamDestroyed(command):
	if command[1] in teams:
		del teams[command[1]]

def teamRenamed(command):
	if command[1] in teams:
		teams[command[2]] = teams.pop(command[1])
		teams[command[2]].name = command[2]

def teamPlayerAdded(command):
	if command[1] in teams and command[2] in players:
		teams[command[1]].players[command[2]] = players[command[2]]

def teamPlayerRemoved(command):
	if command[1] in teams and command[2] in teams[command[1]].players:
		del teams[command[1]].players[command[2]]

def playerEntered(command):
	players[command[1]] = Player(command[1], command[3], command[2])

def playerLeft(command):
	if command[1] in players:
		del players[command[1]]

def playerRenamed(command):
	if command[1] in players:
		if not command[2] in players:
			players[command[2]] = players.pop(command[1])
			players[command[2]].name = command[2]
		players[command[2]].screenname = command[5]

def numHumans(command):
	num_players = command[1]

def positions(command):
	if command[1] in teams:
		teams[command[1]].positions = []
		for i in range(2, len(command)):
			team.positions.append(getPlayer(command[i]))

def zoneSpawned(command):
	if command[2] != "":
		zones[command[2]] = Zone(command[2], None, command[3], command[4], None)
	else:
		zones[command[1]] = Zone(command[1], None, command[3], command[4], None)

def zoneCollapsed(command):
	if command[1] in zones:
		del zones[command[1]]
	elif command[2] in zones:
		del zones[command[2]]
