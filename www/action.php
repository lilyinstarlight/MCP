<?php
require_once 'functions.php';

session_start();
if(isset($_SESSION['user']) && isset($_REQUEST['action'])) {
	switch($_REQUEST['action']) {
		case 'start':
			if(serverExists($_SESSION['server']) && !isRunning($_SESSION['server']) && startServer($_SESSION['server']))
				echo 'success';
			break;
		case 'stop':
			if(serverExists($_SESSION['server']) && isRunning($_SESSION['server']) && stopServer($_SESSION['server']))
				echo 'success';
			break;
		case 'reload':
			if(serverExists($_SESSION['server']) && isRunning($_SESSION['server']) && reloadServer($_SESSION['server']))
				echo 'success';
			break;
		case 'command':
			if(isset($_REQUEST['command']) && serverExists($_SESSION['server']) && isRunning($_SESSION['server']) && sendCommand($_SESSION['server'], $_REQUEST['command']))
				echo 'success';
			break;
		case 'log':
			if(serverExists($_SESSION['server'])) {
				header('Content-type: text/plain; charset=latin1');
				echo getLog($_SESSION['server']);
			}
			break;
		case 'script_log':
			if(serverExists($_SESSION['server'])) {
				header('Content-type: text/plain; charset=latin1');
				echo getScriptLog($_SESSION['server']);
			}
			break;
		case 'settings':
			if(serverExists($_SESSION['server']) && updateSettings($_SESSION['server'], $_REQUEST['settings'])) {
				if(isRunning($_SESSION['server']))
					reloadServer($_SESSION['server']);

				echo 'success';
			}
			break;
		case 'script':
			if(serverExists($_SESSION['server']) && updateScript($_SESSION['server'], $_REQUEST['script'])) {
				if(isRunning($_SESSION['server']))
					reloadScript($_SESSION['server']);

				echo 'success';
			}
			break;
	}
}
?>
