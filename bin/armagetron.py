#!/usr/bin/python
import sys
import grid

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
	armagetron.write(command + "\n")

def pauseBeforeRound():
	sendCommand("WAIT_FOR_EXTERNAL_SCRIPT 1")

def continueRound():
	sendCommand("WAIT_FOR_EXTERNAL_SCRIPT 0")

def chatCommand(command):
	if command[1] in chatcommands:
		chatcommands[command[1]]()
	else:
		sendCommand("PLAYER_MESSAGE " + command[3] + " Command " + command[1] + " not found.");

def run():
	sendCommand("INCLUDE script.cfg")

	ladderlog.seek(0, 2)
	line = None
	while line != "QUIT":
		line = ladderlog.readline().strip()
		if not line:
			continue
		command = line.split()
		if command[0] in commands:
			for handler in commands[command[0]]:
				handler(command)

ladderlog = open(sys.argv[1], 'r')
armagetron = open(sys.argv[2], 'w', 1)

commands = {	"NEW_ROUND": [ grid.newRound ],
		"NEW_MATCH": [ grid.newMatch ],
		"ROUND_SCORE": [ grid.roundScore ],
		"ROUND_SCORE_TEAM": [ grid.roundScoreTeam ],
		"TEAM_CREATED": [ grid.teamCreated ],
		"TEAM_DESTROYED": [ grid.teamDestroyed ],
		"TEAM_RENAMED": [ grid.teamRenamed ],
		"TEAM_PLAYER_ADDED": [ grid.teamPlayerAdded ],
		"TEAM_PLAYER_REMOVED": [ grid.teamPlayerRemoved ],
		"PLAYER_ENTERED": [ grid.playerEntered ],
		"PLAYER_LEFT": [ grid.playerLeft ],
		"PLAYER_RENAMED": [ grid.playerRenamed ],
		"NUM_HUMANS": [ grid.numHumans ],
		"POSITIONS": [ grid.positions ],
		"ZONE_SPAWNED": [ grid.zoneSpawned ],
		"ZONE_COLLAPSED": [ grid.zoneCollapsed ],
		"INVALID_COMMAND": [ chatCommand ] }

chatcommands = {}
