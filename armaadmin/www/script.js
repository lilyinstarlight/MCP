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

function submitCommand() {
	sendCommand(document.getElementById('command_box').value);
	document.getElementById('command_box').value = '';
}

function start() {
	ajaxGet('/start', function(ajax) {
		if(ajax.status != 200 || ajax.responseText != 'success')
			alert('Error starting server: ' + ajax.responseText);
	});
}

function stop() {
	ajaxGet('/stop', function(ajax) {
		if(ajax.status != 200 || ajax.responseText != 'success')
			alert('Error stopping server: ' + ajax.responseText);
	});
}

function reload() {
	ajaxGet('/reload', function(ajax) {
		if(ajax.status != 200 || ajax.responseText != 'success')
			alert('Error reloading server: ' + ajax.responseText);
	});
}

function restart() {
	ajaxGet('/restart', function(ajax) {
		if(ajax.status != 200 || ajax.responseText != 'success')
			alert('Error restarting server: ' + ajax.responseText);
	});
}

function sendCommand(command) {
	ajaxPost('/sendcommand', { 'command': command }, function(ajax) {
		if(ajax.status != 200 || ajax.responseText != 'success')
			alert('Error sending command "' + command + '": ' + ajax.responseText);
	});
}

function getStatus() {
	ajaxGet('/status', function(ajax) {
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
	});
}

function getLog() {
	if(document.getElementById('console').style.display == 'none')
		return;

	ajaxGet('/get/log', function(ajax) {
		if(ajax.status == 200 && ajax.responseText != '')
			document.getElementById('log').innerHTML = ajax.responseText;
	});
}

function getScriptLog() {
	if(document.getElementById('scripting').style.display == 'none' || document.getElementById('script_console').style.display == 'none')
		return;

	ajaxGet('/get/scriptlog', function(ajax) {
		if(ajax.status == 200 && ajax.responseText != '')
			document.getElementById('script_log').innerHTML = ajax.responseText;
	});
}

function getSettings() {
	if(document.getElementById('settings').style.display == 'none' || settings.hasFocus())
		return;

	ajaxGet('/get/settings', function(ajax) {
		if(ajax.status == 200 && ajax.responseText != '')
			settings.setValue(ajax.responseText);
	});
}

function getScript() {
	if(document.getElementById('scripting').style.display == 'none' || document.getElementById('script_editor').style.display == 'none' || script.hasFocus())
		return;

	ajaxGet('/get/script', function(ajax) {
		if(ajax.status == 200 && ajax.responseText != '')
			script.setValue(ajax.responseText);
	});
}

function updateSettings() {
	ajaxPost('/update/settings', { 'settings': settings.getValue() }, function(ajax) {
		if(ajax.status != 200 || ajax.responseText != 'success')
			alert('Error updating settings: ' + ajax.responseText);
	});
}

function updateScript() {
	ajaxPost('/update/script', { 'script': script.getValue() }, function(ajax) {
		if(ajax.status != 200 || ajax.responseText != 'success')
			alert('Error updating script: ' + ajax.responseText);
	});
}

function load() {
	settings = CodeMirror(document.getElementById('settings_editor'), {
		mode: 'settings',
		lineNumbers: true,
		lineWrapping: true,
		showTrailingSpace: true,
		theme: 'arma',
		placeholder: 'Here you can specify your server\'s custom settings.  There is no need to set TALK_TO_MASTER or GLOBAL_ID here, but you should set your server\'s name and set yourself as an Owner.'
	});

	script = CodeMirror(document.getElementById('script_editor'), {
		mode: {
			name: 'python',
			version: 3,
		},
		lineNumbers: true,
		lineWrapping: true,
		showTrailingSpace: true,
		matchBrackets: true,
		theme: 'arma',
		placeholder: 'Here you can add a custom server script written in Python.  There is an API available that makes it easy to add ladderlog event handlers and chat commands but also keeps track of various game elements.  Check the API for details.'
	});

	setInterval(getStatus, 50);
	setInterval(getLog, 500);
	setInterval(getScriptLog, 500);
	setInterval(getSettings, 500);
	setInterval(getScript, 500);
}

window.addEventListener('load', load, false);
