<?php
require_once 'config.php';
require_once 'functions.php';

$message = '';

session_start();
if(!isset($_SESSION['user']) && isset($_REQUEST['user'])) {
	$mysql = new mysqli($CONFIG['host'], $CONFIG['user'], $CONFIG['pass'], $CONFIG['database']);
	$result = $mysql->query('SELECT * FROM ' . $CONFIG['table'] . ' WHERE username="' . $mysql->real_escape_string($_REQUEST['user']) . '" AND password="' . $mysql->real_escape_string(hash('sha256', $_REQUEST['password'])) . '"');
	if($result->num_rows === 1) {
		$array = $result->fetch_array(MYSQLI_ASSOC);
		$_SESSION['user'] = $array['username'];
		$servers = explode(",", $array['servers']);
		$_SESSION['servers'] = $servers;
		if(isset($_SESSION['servers'][0]))
			$_SESSION['server'] = $_SESSION['servers'][0];
	}
	else {
		$message = '<span class="failure">Error: Wrong password.</span><br /><br />';
	}

	$result->close();
	$mysql->close();
}

if(isset($_REQUEST['logout'])) {
	unset($_SESSION['user']);
}

if(isset($_SESSION['user'])) {
	if(isset($_REQUEST['server']) && isset($_SESSION['servers'][$_REQUEST['server']]))
		$_SESSION['server'] = $_SESSION['servers'][$_REQUEST['server']];

	$exists = serverExists($_SESSION['server']);
	$running = $exists && isRunning($_SESSION['server']);
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<title><?php echo $_SESSION['server']; ?> - Server Administration</title>
		<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
		<link href="common.css" rel="stylesheet" type="text/css" />
		<link href="stylesheet.css" rel="stylesheet" type="text/css" />
		<script src="script.js" type="text/javascript"></script>

		<link href="codemirror/codemirror.css" rel="stylesheet" />
		<script src="codemirror/codemirror.js" type="text/javascript"></script>
		<script src="codemirror/python.js" type="text/javascript"></script>
		<script src="codemirror/settings.js" type="text/javascript"></script>
		<script src="codemirror/matchbrackets.js" type="text/javascript"></script>
		<script src="codemirror/placeholder.js" type="text/javascript"></script>
		<script src="codemirror/dialog.js" type="text/javascript"></script>
		<link href="codemirror/dialog.css" rel="stylesheet" />
		<script src="codemirror/searchcursor.js" type="text/javascript"></script>
		<script src="codemirror/search.js" type="text/javascript"></script>
		<script src="codemirror/trailingspace.js" type="text/javascript"></script>
		<link href="codemirror/style.css" rel="stylesheet" />
		<link href="codemirror/arma.css" rel="stylesheet" />
	</head>
	<body>
		<div class="header">
			<img src="aalogo.png" alt="" class="logo" />
			<span class="title">Server Administration</span>
		</div>
		<div class="menu">
			<span class="left">
				<a href="javascript:change('console')" class="button">Console</a><a href="javascript:change('settings')" class="button">Settings</a><a href="javascript:change('scripting')" class="button">Scripting</a>
			</span>
			<span class="right">
				<form id="change_server" action="index.php" method="post" enctype="multipart/form-data">
					<select name="server" onchange="document.getElementById('change_server').submit()"><?php foreach($_SESSION['servers'] as $key => $name) echo "\n\t\t\t\t\t\t" . '<option value="' . $key . '"' . ($name == $_SESSION['server'] ? ' selected="selected"' : '') . '>' . $name . '</option>'; ?>
					</select>
				</form>
				<a href="<?php echo $_SERVER['PHP_SELF']; ?>?logout" class="button">Logout</a>
			</span>
		</div>
		<div class="content">
			<div id="console">
				<div class="controller">
					<span class="left">
						<span id="stopped"<?php echo $running ? ' style="display: none"' : ''; ?>>
							<a id="start" href="javascript:start()" class="button">Start</a>
						</span>
						<span id="started"<?php echo $running ? '' : ' style="display: none"'; ?>>
							<a id="stop" href="javascript:stop()" class="button">Stop</a>
							<a id="restart" href="javascript:stop(true)" class="button">Restart</a>
							<a id="reload" href="javascript:reload()" class="button">Reload</a>
						</span>
					</span>
					<span class="status right">Status: <span id="status"><?php echo $running ? 'Running' : 'Stopped'; ?></span></span>
				</div>
				<table id="commands" class="commands">
					<tr>
						<td style="width: 100%">
							<input id="command_box" type="text"<?php echo $running ? '' : ' disabled="disabled"'; ?> class="command_box" onkeypress="if(event.keyCode == 13) sendCommand(this.value)" />
						</td>
						<td>
							<a id="command_submit"<?php echo $running ? ' href="javascript:sendCommand(document.getElementById(\'command_box\').value)" class="button"' : ' class="button disabled"'; ?>>Send</a>
						</td>
					</tr>
				</table>
				<pre id="log" class="log"></pre>
			</div>
			<div id="settings">
				<div class="controller">
					<span class="right">
						<a id="settings_submit" href="javascript:updateSettings()" class="button">Save</a>
					</span>
				</div>
				<div id="settings_editor">
					<textarea id="settings_text" placeholder="Here you can specify your server's custom settings.  There is no need to set TALK_TO_MASTER or GLOBAL_ID here, but you should set your server's name and set yourself as an Owner."><?php if($exists) echo getSettings($_SESSION['server']); ?></textarea>
				</div>
			</div>
			<div id="scripting">
				<div class="controller">
					<span class="right">
						<a href="javascript:scriptChange('script_editor')" class="button">Editor</a>
						<a href="api.html" target="_blank" class="button">API</a>
						<a href="javascript:scriptChange('script_console')" class="button">Log</a>
						<a id="script_submit" href="javascript:updateScript()" class="button">Save</a>
					</span>
				</div>
				<div id="script_editor">
					<textarea id="script_text" placeholder="Here you can add a custom server script written in Python 3.  There is an API available that makes it easy to add ladderlog event handlers and chat commands but also keeps track of various game elements.  Check the API for details."><?php if($exists) echo getScript($_SESSION['server']); ?></textarea>
				</div>
				<div id="script_console">
					<pre id="script_log" class="log"></pre>
				</div>
			</div>

		</div>
	</body>
</html>
<?php
}
else {
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<title>Server Administration</title>
		<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
		<link href="common.css" rel="stylesheet" type="text/css" />
		<link href="login.css" rel="stylesheet" type="text/css" />
	</head>
	<body>
		<div class="header">
			<img src="aalogo.png" alt="" class="logo" />
			<span class="title">Server Administration</span>
		</div>
		<div class="content"><?php echo $message; ?>
			<form id="login" action="<?php echo $_SERVER['PHP_SELF']; ?>" method="post" enctype="multipart/form-data">
				<table>
					<tr>
						<td><label for="user">Username: </label></td>
						<td><input id="user" name="user" type="text" value="<?php echo isset($_REQUEST['user']) ? $_REQUEST['user'] : ''; ?>" /></td>
					</tr>
					<tr>
						<td><label for="password">Password: </label></td>
						<td><input id="password" name="password" type="password" /></td>
					</tr>
					<tr>
						<td><input type="submit" style="visibility: hidden" /></td>
						<td><br /><a href="javascript:document.getElementById('login').submit()" class="button">Submit</a></td>
					</tr>
				</table>
			</form>
		</div>
	</body>
</html>
<?php
}
?>
