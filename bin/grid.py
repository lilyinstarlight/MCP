#!/usr/bin/python
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
	def __init__(self, grid, name, type, x, y, size, growth=0, xdir=0, ydir=0, interactive=None, r=None, g=None, b=None, target_size=None, rubber=None, player=None, owner=None, command=None):
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
			self.addCommand(command)

	def __del__(self):
		self.changeSize(0)

	def addCommand(self, command):
		if zone.type == "target":
			grid.sendCommand("SET_TARGET_COMMAND " + self.name + " " + command)

	def changeColor(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b
		grid.sendCommand("SET_ZONE_COLOR " + self.name + " " + r + " " + g + " " + b)

	def changeExpansion(self, growth):
		self.growth = growth
		grid.sendCommand("SET_ZONE_EXPANSION " + self.name + " " + growth)

	def changePosition(self, x, y):
		self.x = x
		self.y = y
		grid.sendCommand("SET_ZONE_POSITION " + self.name + " " + x + " " + y)

	def changeSize(self, size, growth=None):
		self.size = size
		command = "SET_ZONE_RADIUS" + self.name + " " + size

		if growth != None:
			command += " " + growth

		grid.sendCommand(command)

	def changeSpeed(self, xdir, ydir):
		self.xdir = xdir
		self.ydir = ydir
		grid.sendCommand("SET_ZONE_SPEED " + self.name + " " + xdir + " " + ydir)
class Grid:
	def __init__(self, sendCommand):
		self.round = 0
		self.teams = {}
		self.num_players = 0
		self.players = {}
		self.zones = {}
		self.sendCommand = sendCommand

	def getTeam(self, name):
		if name in self.teams:
			return self.teams[name]

	def getPlayer(self, name):
		if name in self.players:
			return self.players[name]

	def getZone(self, name):
		if name in self.zones:
			return self.zones[name]

	def createZone(self, name, type, x, y, size, growth=0, xdir=0, ydir=0, interactive=None, r=None, g=None, b=None, target_size=None, rubber=None, player=None, owner=None, targetcommand=None):
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

		self.sendCommand(command)

		self.zones[name] = Zone(self, name, type, x, y, size, growth, xdir, ydir, interactive, r, g, b, target_size, rubber, player, owner, targetcommand)

		return self.zones[name]

	#Ladderlog commands

	def newRound(self, command):
		self.round += 1
		self.zones = {}

	def newMatch(self, command):
		self.round = 1
		for team in self.teams.values():
			team.score = 0
		for player in self.players.values():
			player.score = 0

	def roundScore(self, command):
		if command[2] in self.players:
			self.players[command[2]].score += command[1]

	def roundScoreTeam(self, command):
		if command[2] in self.teams:
			self.teams[command[2]].score += command[1]

	def teamCreated(self, command):
		self.teams[command[1]] = Team(command[1])

	def teamDestroyed(self, command):
		if command[1] in self.teams:
			del self.teams[command[1]]

	def teamRenamed(self, command):
		if command[1] in self.teams:
			self.teams[command[2]] = self.teams.pop(command[1])
			self.teams[command[2]].name = command[2]

	def teamPlayerAdded(self, command):
		if command[1] in self.teams and command[2] in self.players:
			self.teams[command[1]].players[command[2]] = self.players[command[2]]

	def teamPlayerRemoved(self, command):
		if command[1] in self.teams and command[2] in self.teams[command[1]].players:
			del self.teams[command[1]].players[command[2]]

	def playerEntered(self, command):
		self.players[command[1]] = Player(command[1], command[3], command[2])

	def playerLeft(self, command):
		if command[1] in self.players:
			del self.players[command[1]]

	def playerRenamed(self, command):
		if command[1] in self.players:
			if not command[2] in self.players:
				self.players[command[2]] = self.players.pop(command[1])
				self.players[command[2]].name = command[2]
			self.players[command[2]].screenname = command[5]

	def numHumans(self, command):
		self.num_players = command[1]

	def positions(self, command):
		if command[1] in self.teams:
			self.teams[command[1]].positions = []
			for i in range(2, len(command)):
				team.positions.append(getPlayer(command[i]))

	def zoneSpawned(self, command):
		if command[2] != "":
			self.zones[command[2]] = Zone(command[2], None, command[3], command[4], None)
		else:
			self.zones[command[1]] = Zone(command[1], None, command[3], command[4], None)

	def zoneCollapsed(self, command):
		if command[1] in self.zones:
			del self.zones[command[1]]
		elif command[2] in self.zones:
			del self.zones[command[2]]

	def reset(self, command):
		self.round = 0
		self.teams = {}
		self.num_players = 0
		self.players = {}
		self.zones = {}
