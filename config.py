#Prefix where servers are kept
prefix = '/home/armagetron/servers'

#Whether or not to allow server creation
creation = True

#Directory where the sources are kept; ignored if creation is disabled
sources = '/home/armagetron/sources'

#Temprorary directory to build under; ignored if creation is disabled
tmp = '/tmp/mcp'

#Directory where default configuration is kept; ignored if creation is disabled
config = '/home/armagetron/config'

#Directory where the scripting library is kept; None to disable the scripting library
scripting = '/home/armagetron/scripting'

#Max size of server log files in MB before they are rotated; None to disable server log rotation
maxlogsize = 2

#User to run each server under; None to disable running the servers as a different user
user = 'armagetron'

#Path to manager log; None to disable logging
log = '/var/log/mcp/manager.log'

#Path to command output log; None to disable logging
cmdlog = '/var/log/mcp/command.log'

#Path to HTTP log; None to disable logging
httpdlog = '/var/log/mcp/httpd.log'

#Path to HTTP access log; None to disable logging
accesslog = '/var/log/mcp/access.log'

#Host of the web interface (leave blank unless you know what you are doing)
host = ''

#Port to listen on for the web interface
port = 80
