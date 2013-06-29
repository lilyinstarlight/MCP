ArmaAdmin
=========
ArmaAdmin is a complete multi-server management framework for [Armagetron Advanced](http://armagetronad.org).

Installing
----------
There are three main parts to the framework.  The daemon and management tool can be installed alone as well as the scripting API.  However, the web interface depends on the daemon tool to start, stop, and reload servers.  All three can be installed at once simply by using this directory structure.

###Management Tool###
The management tool is composed of 4 files and 6 folders: manager.sh, bin/armagetronad, bin/script, sources/makeserver.sh, bin/, sources/, sources/config/, sources/scripts/, running/, and servers/.  Simply put these files and folders in the directory you want to keep all of the servers.  You must configure `manager.sh` and `makeserver.sh` before you can use them.  In `manager.sh`, you must modify, at the least, the second line and set `homedir` to the directory you put the files.  You can optionally modify the other three variables if your directory structure is different than the default.  You must also set `homedir` on the second line of `makeserver.sh` to the same as the one in `manager.sh` and optionally set the other two variables if you directory structure is different than the default.

To make your first server, put the source code in a directory under `sources`.  You can do this by opening a terminal in the directory and using `bzr branch lp:armagetronad/0.2.8` to download the sources into the `0.2.8` folder.  You can then run `./makeserver.sh <server_name> 0.2.8` to create the server.  Edit the configuration in config directory under your newly made server's directory to your liking.  You can then go the directory with `manager.sh` and run `./manager.sh start <server_name>` to start your server.

You can customize the server creation process by adding configuration that will automatically be added to the `config` folder under `sources`, and add scripts that will automatically be added (such as the API by default) under the `scripts` folder.

If `script.cfg` is in the `config` folder and `armagetron.py` and `grid.py` are in the `scripts` folder, the scripting API is already installed and will be started automatically with your server.  The scripting API will load `script.py` under the `script` under your server if it exists.

###Scripting API###
The scripting API is written in Python 3 and is composed of `armagetron.py`, `grid.py`, and `script.cfg` in the `scripts` and `config` folders under `sources`.  Here they will be automatically added and run by the management tool for each server.  If you wish to add it to another server without the management tool, simply drop them under your scripts folder and create a file called `script.py` in the same folder.  You can then run `python armagetron.py <path_to_ladderlog.txt> <path_to_input.txt>` and it will automatically start `script.py`.  In `script.py`, there is no need to import `armagetron` or `grid`, but you can use then according to the API that is documented in the web interface under `www/api.html`.

###Web Interface###
The web interface is a set of PHP scripts that utilize `manager.sh` to manage servers.  The interface is updated dynamically with AJAX and uses Code Mirror to highlight the Armagetron settings and the Python script.  Simply drop everything in the `www` folder to the place where it will be used and edit `config.php` to your liking.  It depends on a MySQL database to store users and their server's name.
