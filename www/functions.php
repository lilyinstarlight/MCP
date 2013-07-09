<?php
require_once 'config.php';

function serverExists($server) {
	global $CONFIG;

	exec($CONFIG['manager'] . ' list', $list);
	$servers = preg_replace('/Server ([a-zA-Z0-9]*) status: (Stopped|Running)\./', '$1', $list);
	return in_array($server, $servers);
}

function isRunning($server) {
	global $CONFIG;

	exec($CONFIG['manager'] . ' status ' . $server, $running);
	return preg_match('/Server [a-zA-Z0-9]* status: Running\./', $running[0]) === 1;
}

function startServer($server) {
	global $CONFIG;

	exec($CONFIG['manager'] . ' start ' . $server, $started);
	return preg_match('/\* Starting server [a-zA-Z0-9]*\... OK!/', $started[0]) === 1;
}

function stopServer($server) {
	global $CONFIG;

	exec($CONFIG['manager'] . ' stop ' . $server, $stopped);
	return preg_match('/\* Stopping server [a-zA-Z0-9]*\... OK!/', $stopped[0]) === 1;
}

function reloadServer($server) {
	global $CONFIG;

	exec($CONFIG['manager'] . ' reload ' . $server, $reloaded);
	return count($reloaded) === 0;
}

function reloadScript($server) {
	global $CONFIG;

	exec($CONFIG['manager'] . ' restart-script ' . $server, $reloaded);
	return count($reloaded) === 0;
}

function sendCommand($server, $command) {
	global $CONFIG;

	return file_put_contents($CONFIG['serverdir'] . '/' . $server . '/var/input.txt', $command . "\n", FILE_APPEND) !== false;
}

function getTail($filename, $lines) {
	$file = fopen($filename, 'r');
	$pos = -2;
	$text = array();
	$line = 0;

	while($lines > 0) {
		do {
			if(fseek($file, $pos, SEEK_END) == -1) {
				$lines = 0;
				rewind($file);
				break;
			}

			$pos--;
		}
		while(fgetc($file) != "\n");

		$lines--;
		$text[$lines] = fgets($file);
	}

	fclose($file);
	return implode($text);
}

function getLog($server) {
	global $CONFIG;

	$file = $CONFIG['serverdir'] . '/' . $server . '/arma.log';
	if(file_exists($file))
		return getTail($file, $CONFIG['lines']);
	else
		return '';
}

function getScriptLog($server) {
	global $CONFIG;

	$file = $CONFIG['serverdir'] . '/' . $server . '/script-error.log';
	if(file_exists($file))
		return getTail($file, $CONFIG['lines']);
	else
		return '';
}

function getSettings($server) {
	global $CONFIG;

	$file = $CONFIG['serverdir'] . '/' . $server . '/config/settings_custom.cfg';
	if(file_exists($file))
		return file_get_contents($file);
	else
		return '';
}

function updateSettings($server, $settings) {
	global $CONFIG;

	return file_put_contents($CONFIG['serverdir'] . '/' . $server . '/config/settings_custom.cfg', $settings) !== false;
}

function getScript($server) {
	global $CONFIG;

	$file = $CONFIG['serverdir'] . '/' . $server . '/scripts/script.py';
	if(file_exists($file))
		return file_get_contents($file);
	else
		return '';
}

function updateScript($server, $script) {
	global $CONFIG;

	return file_put_contents($CONFIG['serverdir'] . '/' . $server . '/scripts/script.py', $script) !== false;
}
?>
