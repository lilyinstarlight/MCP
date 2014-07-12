#!/usr/bin/python
import time
import sys.stdin as ladderlog
import sys.stdout as server

def add_handler(command, handler):
	if not command in commands:
		commands[command] = []

	commands[command].append(handler)

def remove_handler(command, handler):
	commands[command].remove(handler)

def set_chat_handler(command, handler):
	chat_commands[command] = handler

def remove_chat_handler(command):
	del chat_commands[command]

def send_command(command):
	server.write(command + '\n')

def say(message):
	send_command('SAY ' + message)

def console_message(message):
	send_command('CONSOLE_MESSAGE "' + message + '"')

def center_message(message):
	send_command('CENTER_MESSAGE "' + message + '"')

def send_message(player, message):
	if type(player) == Player:
		send_command('PLAYER_MESSAGE ' + player.name + ' "' + message + '"')
	else:
		send_command('PLAYER_MESSAGE ' + player + ' "' + message + '"')

def pause_round():
	send_command('WAIT_FOR_EXTERNAL_SCRIPT 1')

def continue_round():
	send_command('WAIT_FOR_EXTERNAL_SCRIPT 0')

def set_repository(address):
	send_command('RESOURCE_REPOSITORY_SERVER ' + address)

def set_map(resource):
	send_command('MAP_FILE ' + resource)

def include(config):
	send_command('INCLUDE ' + config)

def rinclude(config):
	send_command('RINCLUDE ' + config)

def reload():
	include('settings.cfg')
	include('server_info.cfg')
	include('settings_custom.cfg')
	send_command('START_NEW_MATCH')

def end_round():
	send_command('WIN_ZONE_MIN_LAST_DEATH 0')
	send_command('WIN_ZONE_MIN_ROUND_TIME 0')

def chat_command(command):
	if command[1] in chat_commands:
		chat_commands[command[1]](command[1:])
	else:
		send_message(command[2], 'Unknown chat command "' + command[1] + '".')

def init(command):
	send_command('LADDERLOG_WRITE_NUM_HUMANS 1')
	send_command('LADDERLOG_WRITE_POSITIONS 1')
	send_command('LADDERLOG_WRITE_INVALID_COMMAND 1')
	send_command('INTERCEPT_UNKNOWN_COMMANDS 1')
	send_command('WAIT_FOR_EXTERNAL_SCRIPT_TIMEOUT 10')

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

	def send_message(self, message):
		send_message(self, message)

	def kill(self):
		send_command('KILL ' + self.name)

	def kick(self, reason=None):
		command = [ 'KICK', self.name ]
		if reason:
			command.append(reason)

		send_command(' '.join(command))

	def ban(self, time=None, reason=None):
		command = [ 'BAN', self.name ]
		if time:
			command.append(time)
		if reason:
			command.append(reason)

		send_command(' '.join(command))

	def ban_ip(self, time, reason=None):
		command = [ 'BAN_IP', self.ip ]
		if time:
			command.append(time)
			if reason:
				command.append(reason)

		send_command(' '.join(command))

	def declare_winner(self):
		send_command('DECLARE_ROUND_WINNER ' + self.name)

	def teleport(self, x, y, xdir, ydir):
		send_command('TELEPORT_PLAYER ' + self.name + ' ' + x + ' ' + y + ' ' + xdir + ' ' + ydir)

	def respawn(self, x, y, xdir, ydir):
		if not self.alive:
			send_command('RESPAWN_PLAYER ' + self.name + ' 1 ' + x + ' ' + y + ' ' + xdir + ' ' + ydir)

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
			self.set_command(command)

	def __del__(self):
		self.change_size(0)

	def change_color(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b
		send_command('SET_ZONE_COLOR ' + self.name + ' ' + r + ' ' + g + ' ' + b)

	def change_expansion(self, growth):
		self.growth = growth
		send_command('SET_ZONE_EXPANSION ' + self.name + ' ' + growth)

	def change_position(self, x, y):
		self.x = x
		self.y = y
		send_command('SET_ZONE_POSITION ' + self.name + ' ' + x + ' ' + y)

	def change_size(self, size, growth=None):
		self.size = size

		command = [ 'SET_ZONE_RADIUS', self.name, size ]
		if growth:
			command.append(growth)

		send_command(' '.join(command))

	def change_speed(self, xdir, ydir):
		self.xdir = xdir
		self.ydir = ydir
		send_command('SET_ZONE_SPEED ' + self.name + ' ' + xdir + ' ' + ydir)

	def set_command(self, command):
		if zone.type == 'target':
			send_command('SET_TARGET_COMMAND ' + self.name + ' ' + command)

class Grid:
	def __init__(self):
		self.reset(None)

	def get_team(self, name):
		if name in self.teams:
			return self.teams[name]

	def get_player(self, name):
		if name in self.players:
			return self.players[name]

	def get_zone(self, name):
		if name in self.zones:
			return self.zones[name]

	def create_zone(self, name, type, x, y, size, growth=0, xdir=0, ydir=0, interactive=None, r=None, g=None, b=None, target_size=None, rubber=None, player=None, owner=None, target_command=None):
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

		send_command(' '.join(command))

		zone = Zone(name, type, x, y, size, growth, xdir, ydir, interactive, r, g, b, target_size, rubber, player, owner, target_command)
		self.zones[name] = zone

		return zone

	#Ladderlog commands

	def new_round(self, command):
		self.round += 1
		self.zones = {}
		for player in self.players.values():
			player.alive = True

	def new_match(self, command):
		self.round = 1
		for team in self.teams.values():
			team.score = 0
		for player in self.players.values():
			player.score = 0

	def round_score(self, command):
		if command[2] in self.players:
			self.players[command[2]].score += int(command[1])

	def round_score_team(self, command):
		if command[2] in self.teams:
			self.teams[command[2]].score += int(command[1])

	def team_created(self, command):
		self.teams[command[1]] = Team(command[1])

	def team_destroyed(self, command):
		if command[1] in self.teams:
			del self.teams[command[1]]

	def team_renamed(self, command):
		if command[1] in self.teams:
			self.teams[command[2]] = self.teams.pop(command[1])
			self.teams[command[2]].name = command[2]

	def team_player_added(self, command):
		if command[1] in self.teams and command[2] in self.players:
			self.teams[command[1]].players[command[2]] = self.players[command[2]]

	def team_player_removed(self, command):
		if command[1] in self.teams and command[2] in self.teams[command[1]].players:
			del self.teams[command[1]].players[command[2]]

	def player_entered(self, command):
		self.players[command[1]] = Player(command[1], command[3], command[2])

	def player_left(self, command):
		if command[1] in self.players:
			del self.players[command[1]]

	def player_renamed(self, command):
		if command[1] in self.players:
			if not command[2] in self.players:
				self.players[command[2]] = self.players.pop(command[1])
				self.players[command[2]].name = command[2]
			self.players[command[2]].screenname = command[5]

	def num_humans(self, command):
		self.num_players = command[1]

	def positions(self, command):
		if command[1] in self.teams:
			self.teams[command[1]].positions = []
			for i in range(2, len(command)):
				self.teams[command[1]].positions.append(self.getPlayer(command[i]))

	def zone_spawned(self, command):
		if command[2]:
			self.zones[command[2]] = Zone(command[2], None, command[3], command[4], None)
		else:
			self.zones[command[1]] = Zone(command[1], None, command[3], command[4], None)

	def zone_collapsed(self, command):
		if command[1] in self.zones:
			del self.zones[command[1]]
		elif command[2] in self.zones:
			del self.zones[command[2]]

	def death_frag(self, command):
		if command[1] in self.players:
			self.players[command[1]].alive = False

	def death_suicide(self, command):
		if command[1] in self.players:
			self.players[command[1]].alive = False

	def death_teamkill(self, command):
		if command[1] in self.players:
			self.players[command[1]].alive = False

	def death_basezone_conquered(self, command):
		if command[1] in self.players:
			self.players[command[1]].alive = False

	def death_deathzone(self, command):
		if command[1] in self.players:
			self.players[command[1]].alive = False

	def death_rubberzone(self, command):
		if command[1] in self.players:
			self.players[command[1]].alive = False

	def death_shot_frag(self, command):
		if command[1] in self.players:
			self.players[command[1]].alive = False

	def death_shot_suicide(self, command):
		if command[1] in self.players:
			self.players[command[1]].alive = False

	def death_shot_teamkill(self, command):
		if command[1] in self.players:
			self.players[command[1]].alive = False

	def reset(self, command):
		self.round = 0
		self.teams = {}
		self.num_players = 0
		self.players = {}
		self.zones = {}

grid = Grid()

commands = {
	'NEW_ROUND': [ grid.new_round ],
	'NEW_MATCH': [ grid.new_match ],
	'ROUND_SCORE': [ grid.round_score ],
	'ROUND_SCORE_TEAM': [ grid.round_score_team ],
	'TEAM_CREATED': [ grid.team_created ],
	'TEAM_DESTROYED': [ grid.team_destroyed ],
	'TEAM_RENAMED': [ grid.team_renamed ],
	'TEAM_PLAYER_ADDED': [ grid.team_player_added ],
	'TEAM_PLAYER_REMOVED': [ grid.team_player_removed ],
	'PLAYER_ENTERED': [ grid.player_entered ],
	'PLAYER_LEFT': [ grid.player_left ],
	'PLAYER_RENAMED': [ grid.player_renamed ],
	'NUM_HUMANS': [ grid.num_humans ],
	'POSITIONS': [ grid.positions ],
	'ZONE_SPAWNED': [ grid.zone_spawned ],
	'ZONE_COLLAPSED': [ grid.zone_collapsed ],
	'DEATH_FRAG': [ grid.death_frag ],
	'DEATH_SUICIDE': [ grid.death_suicide ],
	'DEATH_TEAMKILL': [ grid.death_teamkill ],
	'DEATH_BASEZONE_CONQUERED': [ grid.death_basezone_conquered ],
	'DEATH_DEATHZONE': [ grid.death_deathzone ],
	'DEATH_RUBBERZONE': [ grid.death_rubberzone ],
	'DEATH_SHOT_FRAG': [ grid.death_shot_frag ],
	'DEATH_SHOT_SUICIDE': [ grid.death_shot_suicide ],
	'DEATH_SHOT_TEAMKILL': [ grid.death_shot_teamkill ],
	'GAME_END': [ grid.reset ],
	'ENCODING': [ init ],
	'INVALID_COMMAND': [ chat_command ]
}

chat_commands = {}
