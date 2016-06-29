# prefix where servers are kept
prefix = '/var/lib/mcp/servers'

# whether or not to allow server creation
creation = True

# directory where the sources are kept; ignored if creation is disabled
sources = '/var/lib/mcp/sources'

# temprorary directory to build under; ignored if creation is disabled
tmp = '/tmp/mcp'

# directory where default configuration is kept; ignored if creation is disabled
config = '/var/lib/mcp/config'

# directory where the scripting library is kept; None to disable the scripting library
scripting = '/var/lib/mcp/scripting'

# directory where the databases are kept
database = '/var/db/mcp'

# max size of server log files in kB before they are rotated; None to disable server log rotation
maxlogsize = 100

# range to automatically choose server ports
portrange = (4534, 4634)

# path to manager log; None to disable logging
log = '/var/log/mcp/manager.log'

# path to command output log; None to disable logging
cmdlog = '/var/log/mcp/command.log'

# path to HTTP log; None to disable logging
httpdlog = '/var/log/mcp/httpd.log'

# path to HTTP access log; None to disable logging
accesslog = '/var/log/mcp/access.log'

# host of the web interface (leave blank unless you know what you are doing)
host = ''

# port to listen on for the web interface
port = 8080

# path to TLS/SSL key and certificate files; None to disable TLS encryption
tlskey = None
tlscert = None