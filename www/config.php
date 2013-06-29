<?php
$CONFIG = array(
	//Database information

	//MySQL host address, use localhost if unsure
	'host'		=> 'localhost',

	//Username for database
	'user'		=> 'root',

	//Password for database
	'pass'		=> 'letmein',

	//MySQL database to connect to
	'database'	=> 'database',

	//Table containing the login information
	//Table format: username (varchar, 31)   password (char, 64)   server (varchar, 23)
	'table'		=> 'armaadmin',

	//Path to management script
	'manager'	=> '/home/armagetron/manager.sh',

	//Path to server directory
	'serverdir'	=> '/home/armagetron/servers'
);
?>
