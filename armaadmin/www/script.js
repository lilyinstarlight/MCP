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
	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status != 200 || ajax.responseText != 'success')
				alert('Error starting server: ' + ajax.responseText);
		}
	}
	ajax.open('GET', '/start', true);
	ajax.send();
}

function stop() {
	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status != 200 || ajax.responseText != 'success')
				alert('Error stopping server: ' + ajax.responseText);
		}
	}
	ajax.open('GET', '/stop', true);
	ajax.send();
}

function reload() {
	document.getElementById('reload').href = null;
	document.getElementById('reload').className = 'button disabled';
	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status != 200 || ajax.responseText != 'success')
				alert('Error reloading server: ' + ajax.responseText);
		}
	}
	ajax.open('GET', '/reload', true);
	ajax.send();
}

function restart() {
	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status != 200 || ajax.responseText != 'success')
				alert('Error restarting server: ' + ajax.responseText);
		}
	}
	ajax.open('GET', '/restart', true);
	ajax.send();
}

function sendCommand(command) {
	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText == 'success')
				document.getElementById('command_box').value = '';
			else
				alert('Error sending command "' + command + '": ' + ajax.responseText);
		}
	}
	ajax.open('POST', '/sendcommand', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('command=' + encodeURIComponent(command));
}

function getStatus() {
	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText != '') {
				if(ajax.responseText == 'stopped') {
					document.getElementById('started').style.display = 'none';
					document.getElementById('stopped').style.display = 'inline';
					document.getElementById('command_box').disabled = true;
					document.getElementById('command_submit').className = 'button disabled';
					document.getElementById('status').innerHTML = 'Stopped';
				}
				else if(ajax.responseText == 'starting') {
					document.getElementById('started').style.display = 'none';
					document.getElementById('stopped').style.display = 'inline';
					document.getElementById('command_box').disabled = true;
					document.getElementById('command_submit').className = 'button disabled';
					document.getElementById('status').innerHTML = 'Starting...';
				}
				else if(ajax.responseText == 'started') {
					document.getElementById('stopped').style.display = 'none';
					document.getElementById('started').style.display = 'inline';
					document.getElementById('command_box').disabled = false;
					document.getElementById('command_submit').className = 'button';
					document.getElementById('status').innerHTML = 'Running';
				}
				else if(ajax.responseText == 'stopping') {
					document.getElementById('stopped').style.display = 'none';
					document.getElementById('started').style.display = 'inline';
					document.getElementById('command_box').disabled = true;
					document.getElementById('command_submit').className = 'button disabled';
					document.getElementById('status').innerHTML = 'Stopping...';
				}
				else if(ajax.responseText == 'nonexistent') {
					document.getElementById('stopped').style.display = 'none';
					document.getElementById('started').style.display = 'none';
					document.getElementById('command_box').disabled = true;
					document.getElementById('command_submit').className = 'button disabled';
					document.getElementById('status').innerHTML = 'Server is nonexistent.  Contact the administrator to fix this problem.';
				}
			}
		}
	}
	ajax.open('GET', '/status', true);
	ajax.send();
}

function getLog() {
	if(document.getElementById('console').style.display == 'none')
		return;

	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText != '')
				document.getElementById('log').innerHTML = ajax.responseText;
		}
	}
	ajax.open('GET', '/get/log', true);
	ajax.send();
}

function getScriptLog() {
	if(document.getElementById('scripting').style.display == 'none' || document.getElementById('script_console').style.display == 'none')
		return;

	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText != '')
				document.getElementById('script_log').innerHTML = ajax.responseText;
		}
	}
	ajax.open('GET', '/get/scriptlog', true);
	ajax.send();
}

function getSettings() {
	if(document.getElementById('settings').style.display == 'none')
		return;

	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText != '')
				document.getElementById('settings_text').innerHTML = ajax.responseText;
		}
	}
	ajax.open('GET', '/get/settings', true);
	ajax.send();
}

function getScript() {
	if(document.getElementById('scripting').style.display == 'none' || document.getElementById('script_editor').style.display == 'none')
		return;

	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText != '')
				document.getElementById('script_text').innerHTML = ajax.responseText;
		}
	}
	ajax.open('GET', '/get/script', true);
	ajax.send();
}

function updateSettings() {
	settings.save();
	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText == 'success')
				alert('Settings successfully updated!');
			else
				alert('Error updating settings: ' + ajax.responseText);
		}
	}
	ajax.open('POST', '/update/settings', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('settings=' + encodeURIComponent(document.getElementById('settings_text').value));
}

function updateScript() {
	script.save();
	var ajax = new XMLHttpRequest();
	ajax.onload =	function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText == 'success')
				alert('Script successfully updated!');
			else
				alert('Error updating script: ' + ajax.responseText);
		}
	}
	ajax.open('POST', '/update/script', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('script=' + encodeURIComponent(document.getElementById('script_text').value));
}

function load() {
	settings = CodeMirror.fromTextArea(document.getElementById('settings_text'), {
		mode: 'settings',
		lineNumbers: true,
		lineWrapping: true,
		showTrailingSpace: true,
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

	setInterval(getStatus, 50);
	setInterval(getLog, 500);
	setInterval(getScriptLog, 500);
	setInterval(getSettings, 500);
	setInterval(getScript, 500);
}

window.addEventListener('load', load, false);
