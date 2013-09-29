ArmaAdmin
=========
ArmaAdmin is a complete multi-server management framework for [Armagetron Advanced](http://armagetronad.org).  For more information see the forum post [here](http://forums3.armagetronad.net/viewtopic.php?f=2&t=23250).

What is this?
-------------
ArmaAdmin is a complete package that will manage multiple server daemons, provide an easy to use web interface, and provide a python based scripting API for Armagetron Advanced.  It was created out of a frustration with poorly created and unintuitive Armagetron server managers none of which provided a nice web interface.  Most seemed to be quickly hacked up projects just to get something working and used bad or insecure techniques.  This project solves these problems in a simple Python daemon that serves a set of web pages for control.  This project is designed for a unix-like system and should run well on Linux, Mac OS, or FreeBSD, but also should work on Windows in a unix-like environment (Cygwin) though it may not have server creation functionality.

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
	- All of the players and their name, IP address, score, and status
	- All of the teams and their name, score, players, and player positions
	- All of the zones and their various features

Installing
----------
###Setup###
Edit `config.py` to match your directory structure and preferences.  The `prefix` folder is mandatory and should be the folder set aside for Armagetron servers.  The `sources` folder is optional and contains the source code to the server software to allow server creation.  The `api` folder is also optional and contains the scripting api (in the `api` folder of the project).  The `user` is the user under which the servers (and scripts) will run.  If the `address` is filled in, the server will only accept requests from `address` but generally, you do not need to set this.  The `port` is the port on which the HTTP server will listen.  If there is another web server running on the computer, you can change this port to something other than `80` then have the web server proxy an address to that port.  The `log` is the path of the HTTP access log.

After the configuration is complete, run the setup script:
```
./setup.py
```
The setup script will ask a few questions about your system then automatically install the files.  It additionally creates the folders specified in the configuration if they don't exist.  The administrator user has access to all of the servers and to the administration interface.

Start the daemon using the init system specified in the setup script.  If no init system was specified, start the daemon by running `armaadmin` as root.  Theoretically, the daemon could run as a non-root user, but running the servers as a different user would most likely not work, the HTTP port would need to be greater than 1024, and server creation may not work.

###Creating a server###
Open a web browser to `http://localhost/` or the address specified in `config.py`.  Login as the administrator user then click `Administration`. ***How to make a server***

###Creating a user###
***How to make a user***

###Server creation dependencies###
To compile servers, you must be on a unix-like system with a modern compiler.

####Debian/Ubuntu####
- build-essential
- automake
- bison
- libzthread-dev (optional, 0.2.8 only)

####Arch####
- zthread (optional, 0.2.8 only)

####Gentoo####
- dev-libs/zthread (optional, 0.2.8 only)

Troubleshooting
---------------
###I can't create servers!###
Make sure you have the dependencies and try again.  Maybe your distribution does not come with `automake`?

###The web interface is very buggy!###
Quit using Internet Explorer.

###The scripting API crashes!###
Make sure you are using Python 3.

###None of it works!###
Make sure you installed the package with Python 3 and started it.
