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
	return strpos($running[0], 'Running') !== false;
}

function startServer($server) {
	global $CONFIG;

	exec($CONFIG['manager'] . ' start ' . $server, $started);
	return strpos($started[0], 'OK') !== false;
}

function stopServer($server) {
	global $CONFIG;

	exec($CONFIG['manager'] . ' stop ' . $server, $stopped);
	return strpos($stopped[0], 'OK') !== false;
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

function getLog($server) {
	global $CONFIG;

	$file = fopen($CONFIG['serverdir'] . '/' . $server . '/arma.log', 'r');
	$lines = 200;
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

	$file = $CONFIG['serverdir'] . '/' . $server . '/script/script.py';
	if(file_exists($file))
		return file_get_contents($file);
	else
		return '';
}

function updateScript($server, $script) {
	global $CONFIG;

	return file_put_contents($CONFIG['serverdir'] . '/' . $server . '/script/script.py', $script) !== false;
}
?>
