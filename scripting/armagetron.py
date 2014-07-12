#!/usr/bin/python
import time
import sys.stdin as ladderlog
import sys.stdout as server

def addHandler(command, handler):
	if not command in commands:
		commands[command] = []
	commands[command].append(handler)

def removeHandler(command, handler):
	if command in commands and handler in commands[command]:
		commands[command].remove(handler)

def setChatHandler(command, handler):
	chatcommands[command] = handler

def removeChatHandler(command):
	if command in chatcommands:
		del chatcommands[command]

def sendCommand(command):
	server.write(command + '\n')

def say(message):
	sendCommand('SAY ' + message)

def consoleMessage(message):
	sendCommand('CONSOLE_MESSAGE "' + message + '"')

def centerMessage(message):
	sendCommand('CENTER_MESSAGE "' + message + '"')

def sendMessage(player, message):
	if type(player) == Player:
		sendCommand('PLAYER_MESSAGE ' + player.name + ' "' + message + '"')
	else:
		sendCommand('PLAYER_MESSAGE ' + player + ' "' + message + '"')

def pauseRound():
	sendCommand('WAIT_FOR_EXTERNAL_SCRIPT 1')

def continueRound():
	sendCommand('WAIT_FOR_EXTERNAL_SCRIPT 0')

def setRepository(address):
	sendCommand('RESOURCE_REPOSITORY_SERVER ' + address)

def setMap(resource):
	sendCommand('MAP_FILE ' + resource)

def include(config):
	sendCommand('INCLUDE ' + config)

def rinclude(config):
	sendCommand('RINCLUDE ' + config)

def reload():
	include('settings.cfg')
	include('server_info.cfg')
	include('settings_custom.cfg')
	sendCommand('START_NEW_MATCH')

def endRound():
	sendCommand('WIN_ZONE_MIN_LAST_DEATH 0')
	sendCommand('WIN_ZONE_MIN_ROUND_TIME 0')

def chatCommand(command):
	if command[1] in chatcommands:
		chatcommands[command[1]](command[1:])
	else:
		sendMessage(command[2], 'Unknown chat command "' + command[1] + '".')

def init(command):
	sendCommand('LADDERLOG_WRITE_NUM_HUMANS 1')
	sendCommand('LADDERLOG_WRITE_POSITIONS 1')
	sendCommand('LADDERLOG_WRITE_INVALID_COMMAND 1')
	sendCommand('INTERCEPT_UNKNOWN_COMMANDS 1')
	sendCommand('WAIT_FOR_EXTERNAL_SCRIPT_TIMEOUT 10')

def run():
	while True:
		line = ladderlog.readline()
		if not line:
			time.sleep(0.1)
			continue
		if line.startswith('QUIT'):
			break
		command = line.split()
		if command and command[0] in commands:
			for handler in commands[command[0]]:
				handler(command)

#Grid stuff

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

	def sendMessage(self, message):
		sendMessage(self, message)

	def kill(self):
		sendCommand('KILL ' + self.name)

	def kick(self, reason=None):
		command = [ 'KICK', self.name ]
		if reason:
			command.append(reason)

		sendCommand(' '.join(command))

	def ban(self, time=None, reason=None):
		command = [ 'BAN', self.name ]
		if time:
			command.append(time)
		if reason:
			command.append(reason)

		sendCommand(' '.join(command))

	def banIP(self, time, reason=None):
		command = [ 'BAN_IP', self.ip ]
		if time:
			command.append(time)
			if reason:
				command.append(reason)

		sendCommand(' '.join(command))

	def declareWinner(self):
		sendCommand('DECLARE_ROUND_WINNER ' + self.name)

	def teleport(self, x, y, xdir, ydir):
		sendCommand('TELEPORT_PLAYER ' + self.name + ' ' + x + ' ' + y + ' ' + xdir + ' ' + ydir)

	def respawn(self, x, y, xdir, ydir):
		if not self.alive:
			sendCommand('RESPAWN_PLAYER ' + self.name + ' 1 ' + x + ' ' + y + ' ' + xdir + ' ' + ydir)

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

		if interactive:
			self.interactive = interactive

		if r and g and b:
			self.r = r
			self.g = g
			self.b = b

		if target_size:
			self.target_size = target_size

		if type == 'rubber':
			self.rubber = rubber

		if type == 'zombie':
			self.player = player

		if type == 'zombieOwner':
			self.player = player
			self.owner = owner

		if type == 'target' and command != None:
			self.setCommand(command)

	def __del__(self):
		self.changeSize(0)

	def changeColor(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b
		sendCommand('SET_ZONE_COLOR ' + self.name + ' ' + r + ' ' + g + ' ' + b)

	def changeExpansion(self, growth):
		self.growth = growth
		sendCommand('SET_ZONE_EXPANSION ' + self.name + ' ' + growth)

	def changePosition(self, x, y):
		self.x = x
		self.y = y
		sendCommand('SET_ZONE_POSITION ' + self.name + ' ' + x + ' ' + y)

	def changeSize(self, size, growth=None):
		self.size = size
		command = [ 'SET_ZONE_RADIUS', self.name, size ]

		if growth:
			command.append(growth)

		sendCommand(' '.join(command))

	def changeSpeed(self, xdir, ydir):
		self.xdir = xdir
		self.ydir = ydir
		sendCommand('SET_ZONE_SPEED ' + self.name + ' ' + xdir + ' ' + ydir)

	def setCommand(self, command):
		if zone.type == 'target':
			sendCommand('SET_TARGET_COMMAND ' + self.name + ' ' + command)

class Grid:
	def __init__(self):
		self.reset(None)

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
		command = [ 'SPAWN_ZONE', 'n', name, type ]

		if type == 'zombie':
			if player == None:
				return None
			command.append(player)

		if type == 'zombieOwner':
			if player == None or owner == None:
				return None
			command.append(player)
			command.append(owner)

		command.extend([ x, y, size, growth, xdir, ydir ])

		if type == 'rubber':
			if rubber == None:
				return None
			command.append(rubber)

		if interactive:
			command.append(interactive)

			if r and g and b:
				command.extend([ r, g, b ])

				if target_size:
					command.append(target_size)

		sendCommand(' '.join(command))

		self.zones[name] = Zone(name, type, x, y, size, growth, xdir, ydir, interactive, r, g, b, target_size, rubber, player, owner, targetcommand)

		return self.zones[name]

	#Ladderlog commands

	def newRound(self, command):
		self.round += 1
		self.zones = {}
		for player in self.players.values():
			player.alive = True

	def newMatch(self, command):
		self.round = 1
		for team in self.teams.values():
			team.score = 0
		for player in self.players.values():
			player.score = 0

	def roundScore(self, command):
		if command[2] in self.players:
			self.players[command[2]].score += int(command[1])

	def roundScoreTeam(self, command):
		if command[2] in self.teams:
			self.teams[command[2]].score += int(command[1])

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
				self.teams[command[1]].positions.append(self.getPlayer(command[i]))

	def zoneSpawned(self, command):
		if command[2]:
			self.zones[command[2]] = Zone(command[2], None, command[3], command[4], None)
		else:
			self.zones[command[1]] = Zone(command[1], None, command[3], command[4], None)

	def zoneCollapsed(self, command):
		if command[1] in self.zones:
			del self.zones[command[1]]
		elif command[2] in self.zones:
			del self.zones[command[2]]

	def deathFrag(self, command):
		if command[1] in self.players:
			self.players[command[1]].alive = False

	def deathSuicide(self, command):
		if command[1] in self.players:
			self.players[command[1]].alive = False

	def deathTeamkill(self, command):
		if command[1] in self.players:
			self.players[command[1]].alive = False

	def deathBasezoneConquered(self, command):
		if command[1] in self.players:
			self.players[command[1]].alive = False

	def deathDeathzone(self, command):
		if command[1] in self.players:
			self.players[command[1]].alive = False

	def deathRubberzone(self, command):
		if command[1] in self.players:
			self.players[command[1]].alive = False

	def deathShotFrag(self, command):
		if command[1] in self.players:
			self.players[command[1]].alive = False

	def deathShotSuicide(self, command):
		if command[1] in self.players:
			self.players[command[1]].alive = False

	def deathShotTeamkill(self, command):
		if command[1] in self.players:
			self.players[command[1]].alive = False

	def reset(self, command):
		self.round = 0
		self.teams = {}
		self.num_players = 0
		self.players = {}
		self.zones = {}

grid = Grid()

commands = {	'NEW_ROUND': [ grid.newRound ],
		'NEW_MATCH': [ grid.newMatch ],
		'ROUND_SCORE': [ grid.roundScore ],
		'ROUND_SCORE_TEAM': [ grid.roundScoreTeam ],
		'TEAM_CREATED': [ grid.teamCreated ],
		'TEAM_DESTROYED': [ grid.teamDestroyed ],
		'TEAM_RENAMED': [ grid.teamRenamed ],
		'TEAM_PLAYER_ADDED': [ grid.teamPlayerAdded ],
		'TEAM_PLAYER_REMOVED': [ grid.teamPlayerRemoved ],
		'PLAYER_ENTERED': [ grid.playerEntered ],
		'PLAYER_LEFT': [ grid.playerLeft ],
		'PLAYER_RENAMED': [ grid.playerRenamed ],
		'NUM_HUMANS': [ grid.numHumans ],
		'POSITIONS': [ grid.positions ],
		'ZONE_SPAWNED': [ grid.zoneSpawned ],
		'ZONE_COLLAPSED': [ grid.zoneCollapsed ],
		'DEATH_FRAG': [ grid.deathFrag ],
		'DEATH_SUICIDE': [ grid.deathSuicide ],
		'DEATH_TEAMKILL': [ grid.deathTeamkill ],
		'DEATH_BASEZONE_CONQUERED': [ grid.deathBasezoneConquered ],
		'DEATH_DEATHZONE': [ grid.deathDeathzone ],
		'DEATH_RUBBERZONE': [ grid.deathRubberzone ],
		'DEATH_SHOT_FRAG': [ grid.deathShotFrag ],
		'DEATH_SHOT_SUICIDE': [ grid.deathShotSuicide ],
		'DEATH_SHOT_TEAMKILL': [ grid.deathShotTeamkill ],
		'GAME_END': [ grid.reset ],
		'ENCODING': [ init ],
		'INVALID_COMMAND': [ chatCommand ] }

chatcommands = {}
