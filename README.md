ArmaAdmin
=========
ArmaAdmin is a complete multi-server management framework for [Armagetron Advanced](http://armagetronad.org).  For more information see the forum post [here](http://forums3.armagetronad.net/viewtopic.php?f=2&t=23250).

What is this?
-------------
ArmaAdmin is a complete package that will manage multiple server daemons, provide an easy to use web interface, and provide a python based scripting API for Armagetron Advanced.  It was created out of a frustration with poorly created and unintuitive Armagetron server managers none of which provided a nice web interface.  Most seemed to be quickly hacked up projects just to get something working and used bad or insecure techniques.  This project solves these problems in a simple Python daemon that serves a set of web pages for control.  This project is designed for a unix-like system and should run well on Linux, Mac OS, or FreeBSD, but also should work on Windows in a unix-like environment (Cygwin).

Features
--------
###Daemon Manager###
- Restarts a server if it crashes
- Saving a log, error log, and script error log
- Kill unresponsive server/script
- Full support for scripting
- Clears error log on startup

###Web Interface###
- Start/Stop/Restart/Reload buttons
- Command box to send commands to the server
- Reversed log that updates every half second
- Full support for fancy characters
- Editing settings\_custom.cfg
- Editing script.py (with a documented scripting API)
- Script error log
- Full syntax highlighting for the settings and script
- Realtime updates of server status
- Multiple people can administer the same server at once
- Full user and server creation from an administration panel

###Scripting API###
- Support for adding multiple callbacks to a single ladderlog command
- Support for special characters
- Support for chat command handlers
- Keeps track of and provides a nice interface to:
	- Current round
	- The number of players
	- All of the players and their name, IP address and score and whether they are alive or dead
	- All of the teams and their name, score, players, and player positions
	- All of the zones and various features about them

Installing
----------
TODO when it is complete

Troubleshooting
---------------
###The server does not compile!###
Make sure you have the dependencies and try again.  Maybe your distribution does not come with `automake`?

###The web interface is very buggy!###
Quit using Internet Explorer.

###The scripting API crashes!###
Make sure you are using Python 3.

###None of it works!###
TODO when it is complete
