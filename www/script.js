var settings;
var script;

function change(element) {
	document.getElementById('console').style.display = 'none';
	document.getElementById('settings').style.display = 'none';
	document.getElementById('scripting').style.display = 'none';
	document.getElementById(element).style.display = 'block';
}

function scriptChange(element) {
	document.getElementById('script_editor').style.display = 'none';
	document.getElementById('script_console').style.display = 'none';
	document.getElementById(element).style.display = 'block';
}

function start() {
	document.getElementById('start').href = null;
	document.getElementById('start').className = 'button disabled';
	document.getElementById('status').innerHTML = 'Starting...';
	var ajax = new XMLHttpRequest();
	ajax.onload =	function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText == 'success') {
				document.getElementById('status').innerHTML = 'Running';
				document.getElementById('stopped').style.display = 'none';
				document.getElementById('started').style.display = 'inline';
				document.getElementById('command_box').disabled = false;
				document.getElementById('command_submit').href = 'javascript:sendCommand(document.getElementById(\'command_box\').value)';
				document.getElementById('command_submit').className = 'button';
			}
			else {
				document.getElementById('status').innerHTML = 'Stopped';
				alert('Error starting server: ' + ajax.responseText);
			}
			document.getElementById('start').href = 'javascript:start()';
			document.getElementById('start').className = 'button';
		}
	}
	ajax.open('POST', 'action.php', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('action=start');
}

function stop(restart) {
	document.getElementById('stop').href = null;
	document.getElementById('stop').className = 'button disabled';
	document.getElementById('restart').href = null;
	document.getElementById('restart').className = 'button disabled';
	document.getElementById('reload').href = null;
	document.getElementById('reload').className = 'button disabled';
	document.getElementById('status').innerHTML = 'Stopping...';
	var ajax = new XMLHttpRequest();
	ajax.onload =	function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText == 'success') {
				document.getElementById('status').innerHTML = 'Stopped';
				document.getElementById('stopped').style.display = 'inline';
				document.getElementById('started').style.display = 'none';
				document.getElementById('command_box').disabled = true;
				document.getElementById('command_submit').href = null;
				document.getElementById('command_submit').className = 'button disabled';

				if(restart)
					start();
			}
			else {
				document.getElementById('status').innerHTML = 'Running';
				alert('Error stopping server: ' + ajax.responseText);
			}
			document.getElementById('stop').href = 'javascript:stop()';
			document.getElementById('stop').className = 'button';
			document.getElementById('restart').href = 'javascript:stop();start()';
			document.getElementById('restart').className = 'button';
			document.getElementById('reload').href = 'javascript:reload()';
			document.getElementById('reload').className = 'button';
		}
	}
	ajax.open('POST', 'action.php', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('action=stop');
}

function reload() {
	document.getElementById('reload').href = null;
	document.getElementById('reload').className = 'button disabled';
	var ajax = new XMLHttpRequest();
	ajax.onload =	function() {
		if(ajax.readyState == 4) {
			if(ajax.status != 200 || ajax.responseText != 'success')
				alert('Error reloading server: ' + ajax.responseText);
			document.getElementById('reload').href = 'javascript:reload()';
			document.getElementById('reload').className = 'button';
		}
	}
	ajax.open('POST', 'action.php', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('action=reload');
}

function sendCommand(command) {
	document.getElementById('command_box').disabled = true;
	document.getElementById('command_submit').href = null;
	document.getElementById('command_submit').className = 'button disabled';
	var ajax = new XMLHttpRequest();
	ajax.onload =	function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText == 'success')
				document.getElementById('command_box').value = '';
			else
				alert('Error sending command "' + command + '"');
			document.getElementById('command_box').disabled = false;
			document.getElementById('command_submit').href = 'javascript:sendCommand(document.getElementById(\'command_box\').value)';
			document.getElementById('command_submit').className = 'button';
		}
	}
	ajax.open('POST', 'action.php', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('action=command&command=' + command);
}

function getLog() {
	if(document.getElementById('console').style.display == 'none')
		return;

	var ajax = new XMLHttpRequest();
	ajax.onload =	function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText != '')
				document.getElementById('log').innerHTML = ajax.responseText;
		}
	}
	ajax.open('POST', 'action.php', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('action=log');
}

function getScriptLog() {
	if(document.getElementById('script_console').style.display == 'none')
		return;

	var ajax = new XMLHttpRequest();
	ajax.onload =	function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText != '')
				document.getElementById('script_log').innerHTML = ajax.responseText;
		}
	}
	ajax.open('POST', 'action.php', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('action=script_log');
}

function updateSettings() {
	document.getElementById('settings_submit').href = null;
	document.getElementById('settings_submit').className = 'button disabled';
	settings.save();
	var ajax = new XMLHttpRequest();
	ajax.onload =	function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText == 'success')
				alert('Settings successfully updated!');
			else
				alert('Error updating settings: ' + ajax.responseText);
			document.getElementById('settings_submit').href = 'javascript:updateSettings()';
			document.getElementById('settings_submit').className = 'button';
		}
	}
	ajax.open('POST', 'action.php', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('action=settings&settings=' + document.getElementById('settings_text').value);
}

function updateScript() {
	document.getElementById('script_submit').href = null;
	document.getElementById('script_submit').className = 'button disabled';
	script.save();
	var ajax = new XMLHttpRequest();
	ajax.onload =	function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText == 'success')
				alert('Script successfully updated!');
			else
				alert('Error updating script: ' + ajax.responseText);
			document.getElementById('script_submit').href = 'javascript:updateScript()';
			document.getElementById('script_submit').className = 'button';
		}
	}
	ajax.open('POST', 'action.php', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('action=script&script=' + document.getElementById('script_text').value);
}

function load() {
	settings = CodeMirror.fromTextArea(document.getElementById('settings_text'), {
		mode: 'settings',
		lineNumbers: true,
		lineWrapping: true,
		showTrailingSpace: true,
		matchBrackets: true,
		theme: 'arma',
	});

	script = CodeMirror.fromTextArea(document.getElementById('script_text'), {
		mode: {
			name: 'python',
			version: 3,
		},
		lineNumbers: true,
		lineWrapping: true,
		showTrailingSpace: true,
		matchBrackets: true,
		theme: 'arma',
	});

	document.getElementById('settings').style.display = 'none'
	document.getElementById('scripting').style.display = 'none'
	document.getElementById('script_console').style.display = 'none'
	setInterval(getLog, 500);
	setInterval(getScriptLog, 500);
}

window.addEventListener('load', load, false);
