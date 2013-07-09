<?php
require_once 'functions.php';

session_start();
if(isset($_SESSION['user']) && isset($_REQUEST['action'])) {
	switch($_REQUEST['action']) {
		case 'start':
			if(!serverExists($_SESSION['server'])) {
				echo 'Server does not exist.';
				break;
			}

			if(isRunning($_SESSION['server'])) {
				echo 'Server already running.';
				break;
			}

			if(startServer($_SESSION['server']))
				echo 'success';
			else
				echo 'Unknown error.';

			break;
		case 'stop':
			if(!serverExists($_SESSION['server'])) {
				echo 'Server does not exist.';
				break;
			}

			if(!isRunning($_SESSION['server'])) {
				echo 'Server not running.';
				break;
			}

			if(stopServer($_SESSION['server']))
				echo 'success';
			else
				echo 'Unknown error.';

			break;
		case 'reload':
			if(!serverExists($_SESSION['server'])) {
				echo 'Server does not exist.';
				break;
			}

			if(!isRunning($_SESSION['server'])) {
				echo 'Server not running.';
				break;
			}

			if(reloadServer($_SESSION['server']))
				echo 'success';
			else
				echo 'Unknown error.';

			break;
		case 'command':
			if(!serverExists($_SESSION['server'])) {
				echo 'Server does not exist.';
				break;
			}

			if(!isRunning($_SESSION['server'])) {
				echo 'Server not running.';
				break;
			}

			if(!isset($_REQUEST['command'])) {
				echo 'No command.';
				break;
			}

			if(sendCommand($_SESSION['server'], $_REQUEST['command']))
				echo 'success';
			else
				echo 'Unknown error.';

			break;
		case 'log':
			if(serverExists($_SESSION['server'])) {
				header('Content-type: text/plain; charset=latin1');
				echo getLog($_SESSION['server']);
			}
			else {
				echo 'Server does not exist.';
			}

			break;
		case 'script_log':
			if(serverExists($_SESSION['server'])) {
				header('Content-type: text/plain; charset=latin1');
				echo getScriptLog($_SESSION['server']);
			}
			else {
				echo 'Server does not exist.';
			}

			break;
		case 'settings':
			if(!serverExists($_SESSION['server'])) {
				echo 'Server does not exist.';
				break;
			}

			if(updateSettings($_SESSION['server'], $_REQUEST['settings'])) {
				if(isRunning($_SESSION['server']))
					reloadServer($_SESSION['server']);

				echo 'success';
			}
			else {
				echo 'Unknown error.';
			}

			break;
		case 'script':
			if(!serverExists($_SESSION['server'])) {
				echo 'Server does not exist.';
				break;
			}

			if(updateScript($_SESSION['server'], $_REQUEST['script'])) {
				if(isRunning($_SESSION['server']))
					reloadScript($_SESSION['server']);

				echo 'success';
			}
			else {
				echo 'Unknown error.';
			}

			break;
	}
}
?>
