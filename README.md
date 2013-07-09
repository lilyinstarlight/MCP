ArmaAdmin
=========
ArmaAdmin is a complete multi-server management framework for [Armagetron Advanced](http://armagetronad.org).  For more information see the forum post [here](http://forums3.armagetronad.net/viewtopic.php?f=2&t=23250).

What is this?
-------------
This is a complete package that will manage multiple server daemons, provide an easy to use web interface, and provide a python based scripting API.  It is designed for unix-like systems so it can easily work on Mac OS, Linux, or FreeBSD.  It might work on Windows too assuming you have all of the dependencies for each module you want to use.  It is modular so you do not have to use all three parts (although the web interface requires the daemon manager).

Features
--------
###Daemon Manager###
- Restarts a server if it crashes
- Saving a log, error log, and script error log
- PID file locking
- Will remove lock file if the process no longer exists (useful in case of system power failure)
- Kill unresponsive server/script
- Full support for scripting
- Clears error log on startup

###Web Interface###
- User management
- Start/Stop/Restart/Reload buttons
- Command box to send commands to the server
- Reversed log that updates every half second
- Log supports fancy characters
- Changing settings\_custom.cfg
- Changing script.py (with a documented scripting API)
- Script error log
- Full syntax highlighting for the settings and script

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
If you just want a generic and basic installation, all you need to do is just clone repository into a folder and follow the daemon manager's and web interface's configuration instructions.

###Daemon Manager###
The daemon manager is all of the files and folders with the exception of `bin/armagetron.py` and the `www` folder.  Install is simply putting these files where you want them to go then configuring them for that directory.

####Daemonize####
The daemon manager requires the daemonize tool to run armagetron in the background.  Installation of the daemonize tool is very simple, even if there isn't a package for your system.  Gentoo has a package in the main repository for daemonize and Arch has it in its AUR.  Neither Debian nor Ubuntu have it as a package, but it is very simple to install from source.

To install from source, run:

```
git clone http://github.com/bmc/daemonize.git
cd daemonize
sh configure
make
sudo make install
```

This will put the daemonize binary in `/usr/local/sbin/daemonize`.

####Configuration####
To configure the daemon manager, first open up `manager.sh`.  Edit the line that starts with `homedir=` to point to the directory of the script.  If you want a different directory structure than the default, edit the corresponding lines below it.  Next, go down to the line that starts with `daemonize=` and edit it to point to the daemonize binary.

Next, you must configure the server compilation tool.  Open up `sources/makeserver.sh` and edit the line that starts with `homedir=` to point to the same location as the `$homedir` in `manager.sh`.  If you changed any of the other directories, change the corresponding ones in `sources/makeserver.sh` as well.  See Creating Servers below for instructions on how to make your first server.

You can now put your own custom configuration in the `sources/config` folder and your custom scripts in the `sources/scripts` folder that will be copied to every server.  There is a default `server\_info.cfg` in the `sources/config` folder that enables GLOBAL\_ID and TALK\_TO\_MASTER.  I would also recommend that you add a SERVER\_DNS entry here, especially if you have a dynamic IP address.

Note: If you do not want to use the scripting API, edit `bin/script` to reflect how you start scripts.

###Web Interface###
The web interface is composed of all files in the `www` folder.  Simply put the contents of that folder into your web directory or set your (PHP enabled) web server to that directory.

####Configuration####
All of the configuration for the web interface is done in `www/config.php`.  Simply enter the MySQL (or MariaDB) server information then put the directories that are configured in the daemon manager.  The file acts as an example configuration and documents itself so read the file's comments for more help.

####MySQL Table####
Creating the MySQL table is somewhat straightforward.  Simply use a database of your choice then issue this MySQL command:

`CREATE TABLE <table name> ( username VARCHAR(31), password CHAR(64), servers VARCHAR(200) );`

The basic table layout are the columns username, password, and servers.  The username column simply contains that user's name.  The password column contains a sha256 hash of the user's password.  The servers column contains a comma separated list of servers that the user owns.  See Creating Servers below for instructions on adding each row.

###Scripting API###
The scripting API is entirely contained in `bin/armagetron.py`.  If you would like to use it, simply copy it into your script folder and use it just like you would with the rest of the framework.  The API, however, requires that `sys.argv[1]` is the ladderlog file and `sys.argv[2]` is the input file to armagetron.

The scripting API is documented in `www/api.html` (which uses only `www/common.css`, `www/api.css` and the images) where there are a few examples.

Creating Servers
----------------
Creating servers is relatively simple thanks to the `sources/makeserver.sh` script.  It will do everything to make a server for you in the proper directory structure with the appropriate settings.  If you are using the web interface, you either need to append the server to an existing user or create a new user for it.

###Sources###
Before you can make a server, you need to source code to it.  You can get this by changing to the `sources` directory and running one of the following commands:

| Version      | Command                                                                        |
| ------------ | ------------------------------------------------------------------------------ |
| 0.2.8        | `bzr branch lp:armagetronad/0.2.8`                                             |
| 0.4          | `bzr branch lp:armagetronad/0.4`                                               |
| 0.2.8 sty+ct | `bzr branch lp:~armagetronad-ct/armagetronad/0.2.8-armagetronad-sty+ct sty+ct` |

The only build dependencies of the armagetron server are the `build-essential`, `automake`, `bison`, and `libzthread-dev` packages in Debian/Ubuntu.  In Arch, you only need to install `zthread` from the AUR, and in Gentoo, you only need to install `dev-libs/zthread`.

After you have the sources and the dependencies, simply run `./makeserver.sh <server> <source>` where `<server>` is the server's name and `<source>` is the directory name of the source you just downloaded.  After that, you will have a server ready to start with `manager.sh`.

The configuration for the server is in `servers/<server>/config/settings\_custom.cfg`.  If you are not using the web interface, you will need to create the file and populate it with your own settings.

###Updating the Web Interface###
Next, you must tell the web interface who owns your new server.  If you already have a user in the database that will own this server, simply add a comma, without any spaces, and the server name to the user's `servers` column.  Do this by running:

`UPDATE <table name> SET servers=concat(servers,',<server>') WHERE username=<username>;`

If you want to add a new user to the database, then you must run:

`INSERT INTO <table name> VALUES (<username>, <sha256 hash of password>, <server>);`

After that, you can login as the new user from the main page and immediately control the new server.  You can change the settings or add a script using the interface and everytime you save the settings or the script, it will automatically reload the settings or restart the script.

Troubleshooting
---------------
###The server does not compile!###
Make sure you have the dependencies and try again.  Maybe your distribution does not come with `automake`?

###The servers won't start!###
Make sure you have `daemonize` installed and the location in `manager.sh` is correct.

###I can't login to the web interface!###
Make sure you put a sha256 hash of the password in the password field; its name is misleading.  If you are getting problems with MySQL, then make sure you have mysqli support in PHP.

###The controls in the web interface do not work!###
Make sure that PHP requests and sessions are working properly.

###The web interface is very buggy!###
Quit using Internet Explorer.

###The scripting API crashes!###
Make sure you are using Python 3.

###None of it works!###
Did you set the `homedir` and `daemonize` in `manager.sh` and `sources/makeserver.sh` and update the configuration in `www/config.php`?  If so, then do you have all of the dependencies?
