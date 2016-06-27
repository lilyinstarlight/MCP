MCP
===

MCP, short for [Master Control Program](http://tron.wikia.com/wiki/MCP), is a complete multi-server management framework for [Armagetron Advanced](http://armagetronad.org). For more information see the forum post [here](http://forums3.armagetronad.net/viewtopic.php?f=2&t=23250).


What is this?
-------------

MCP is a complete package that will manage multiple server daemons, provide an easy to use web interface, and provide a python based scripting library for Armagetron Advanced. It was created out of a frustration with poorly written and unintuitive Armagetron server managers none of which provided a nice web interface. Most seemed to be quickly hacked up projects just to get something working and used bad or insecure techniques. This project solves these problems in a simple Python daemon that serves a RESTful HTTP API and a set of web pages that use it for control. This project is designed for a unix-like system and should run well on Linux, Mac OS, and FreeBSD but should also work on Windows in a unix-like environment (Cygwin) though it probably won't have server creation functionality.


Features
--------

### Daemon Manager

- Restarting a server if it crashes
- Saving rotated logs and error logs of the server and error logs of the script
- Killing unresponsive server/script
- Full support for scripting
- Clearing error log on startup
- Server port management

### Web Interface

- Start/Stop/Restart/Reload buttons
- Command box to send commands directly to the server
- Realtime server status and server log
- Full support for non-ascii characters
- Editing settings\_custom.cfg
- Editing script.py (with a documented scripting library)
- Script error log
- Full syntax highlighting for the settings and script
- Multiple people can administer the same server at once
- Full user and server creation from an administration panel

### Scripting Library

- Adding multiple callbacks to a single ladderlog command
- Chat command handlers
- Full support for non-ascii characters
- Default set of ladderlog handlers keep track of
	- Current round
	- The number of players
	- The players and their name, IP address, score, and status
	- The teams and their name, score, players, and player positions
	- The zones and their various features


Installing
----------

### Setup

Edit `config.py` to match your directory structure and preferences. Below is a list of the preferences and what they mean.
- `prefix` folder is mandatory and should be the folder set aside for Armagetron servers.
- `creation` indicated whether or not servers can be created.
- `sources` folder is optional and contains the source code to the server software from which the servers are created.
- `tmp` folder is optional and contains the located where servers will be built before being merged.
- `config` folder is optional and contains the default set of configuration copied to every server when created.
- `scripting` folder is also optional and contains the scripting library (in the `scripting` folder of the project).
- `maxlogsize` is maximum size a server log will get (in KB) before it is rotated into the `logs` folder.
- `user` is the user under which the servers (and scripts) will run.
- `portrange` is the range of ports from which servers will automatically be configured if their port is not set.
- `log` is the path of the manager log.
- `cmdlog` is the path of the external command log.
- `httpdlog` is the path of the HTTP daemon log.
- `accesslog` is the path of the HTTP access log.
- `host` is the address for which the server will accept requests but generally, you do not need to set this.
- `port` is the port on which the HTTP server will listen. If there is another web server running on the computer, you can change this port to something other than `80` then have the web server proxy an address to that port.

To create the user the servers will run under (if any), run the `useradd` command:
```
# useradd -m <user>
```

After the configuration is complete, run the setup script:
```
# ./setup.py install
```
The setup script will ask a few questions about your system then automatically install the files. It additionally creates the folders specified in `config.py` if they don't exist. The administrator user has access to all of the servers and to the administration interface.

Start the daemon using the init system specified in the setup script. If no init system was specified, start the daemon by running `mcp` as the desired user.

### Downloading sources

Before you can create your first server, you must download a copy of the Armagetron Advanced source code. To do this, first open a web browser to `http://localhost/` or the address specified in `config.py` and login as the administrator user. Click `Admin` in the upper right and then click the `Sources` tab in the administration interface. Click the `Add Source` button and fill out the form with the appropriate information. The source name is the name by which this source will be referred. For example, you can call one `sty+ct` if you download ct's patched version. The bzr address is the location of the bzr repository for the source code. For example, for `0.2.8-sty+ct`, the source is located at `lp:~armagetronad-ct/armagetronad/0.2.8-armagetronad-sty+ct`. Use the table below for a list of common versions and their bzr addresses.

| Version         | Bzr Address                                                     |
| --------------- | --------------------------------------------------------------- |
| 0.2.8           | `lp:armagetronad/0.2.8`                                         |
| 0.4             | `lp:armagetronad/0.4`                                           |
| 0.2.8 sty+ct    | `lp:~armagetronad-ct/armagetronad/0.2.8-armagetronad-sty+ct`    |
| 0.2.9 sty+ct+ap | `lp:~armagetronad-ap/armagetronad/0.2.9-armagetronad-sty+ct+ap` |

After the information is filled in and submitted, the source can then be used in the server creation form in a drop-down list. The source code will take some time to download, generally up to 30 seconds.

### Creating a server

Once you have added a source, you can create your first server. To do this, first open a web browser to `http://localhost/` or the address specified in `config.py` and login as the administrator user. Click `Admin` in the upper right and then click the `Servers` tab in the administration interface. Click the `Create Server` button and fill out the form with information about the server. The name of the server is the name by which it will be referred when assigning it to users. The source is the version that should be used to create the server. After the information is filled out, click `Create` and the manager will then begin server creation. This process can take up to 10 minutes depending on the processing power and load of the server computer.

### Creating a user

To create a user, first open a web browser to `http://localhost/` or the address specified in `config.py` and login as the administrator user. Click `Admin` in the upper right and then make sure you are on the `Users` tab in the administration interface. Click the `Create User` button and fill out the form with the user's information. The admin checkbox enables administrative rights to the user allowing them access to the administration interface. From the multi-select field, choose the user's servers, holding down control to select more than one. After the information is filled out, click `Create` and the user will be able to login and manage its servers.

### Server creation dependencies

To create servers, you must be on a unix-like system with a modern C++ compiler. Each server is compiled when it is created with a set of flags to keep them in their own prefixes and in a sane directory structure. This allows multiple servers to be kept on one system at the same time and allows easy access and configuration of the servers over FTP or SSH. Below are the necessary packages that must be installed to download sources and create servers.

#### Debian/Ubuntu

- build-essential
- automake
- bison
- libxml2-dev
- libprotobuf-dev
- libboost-thread-dev (optional, 0.4 only)
- libzthread-dev (optional, 0.2.8 only)
- bzr

#### Arch

- base-devel
- libxml2
- protobuf
- boost (optional, 0.4 only)
- zthread (optional, 0.2.8 only)
- bzr

#### Gentoo

- dev-libs/libxml2
- dev-libs/protobuf
- dev-libs/boost\[threads\] (optional, 0.4 only)
- dev-libs/zthread (optional, 0.2.8 only)
- dev-vcs/bzr


Upgrading
---------

To upgrade the software, follow the steps for setup under the installation section however replacing the install command with the uprade command:
```
# ./setup.py upgrade
```

The upgrade differs in that it does not write new databases or configuration files.


Questions
---------

### Is there a demo?

There is a live demo at http://mcp.fkmclane.net/. It shows off the web interface and the simplicity of the scripting library. The sample script shows how to reset the server settings when everyone leaves the server. It does not show off the administration page (yet) for security reasons. Simply login with user: `demo` and password: `demo`.

### What if I want to use my own scripting library?
Well, you simply need to place it in the `library` folder of the project and reinstall. You can also (optionally) create your own `api.html` so that the documentation is available in the web interface.

### I want to use this on Windows but it isn't working!
Well that isn't a question and I'm afraid I can't help you there. I don't mess with Windows often and don't have time to fiddle with an unsupported operating system for a single person. This could work on Windows if you had custom compiled servers (a lot of work to get the right flags) but honestly, it would take less time to install [Ubuntu](http://www.ubuntu.com/) then install this software.

### I found a bug! I found a bug!
Again, that isn't a question, but could you please report it on [GitHub](https://github.com/fkmclane/MCP/issues)?


Troubleshooting
---------------

### I can't create servers!
Make sure you have the dependencies and try again. Maybe your distribution does not come with `automake`?

### The web interface is very buggy!
Quit using Internet Explorer 8.

### The scripting library crashes!
Make sure it is running with Python 3. If it is, please report the crash and error log at [GitHub](https://github.com/fkmclane/MCP/issues).

### None of it works!
Make sure you installed the package with Python 3 and started the daemon properly.
