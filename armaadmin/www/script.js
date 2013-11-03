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

function refresh() {
	switch(getStatus()) {
		case 'stopped':
			document.getElementById('started').style.display = 'none';
			document.getElementById('stopped').style.display = 'inline';
			document.getElementById('command_box').disabled = true;
			document.getElementById('command_submit').className = 'button disabled';
			document.getElementById('status').innerHTML = 'Stopped';
			break;
		case 'starting':
			document.getElementById('started').style.display = 'none';
			document.getElementById('stopped').style.display = 'inline';
			document.getElementById('command_box').disabled = true;
			document.getElementById('command_submit').className = 'button disabled';
			document.getElementById('status').innerHTML = 'Starting...';
			break;
		case 'started':
			document.getElementById('stopped').style.display = 'none';
			document.getElementById('started').style.display = 'inline';
			document.getElementById('command_box').disabled = false;
			document.getElementById('command_submit').className = 'button';
			document.getElementById('status').innerHTML = 'Running';
			break;
		case 'stopping':
			document.getElementById('stopped').style.display = 'none';
			document.getElementById('started').style.display = 'inline';
			document.getElementById('command_box').disabled = true;
			document.getElementById('command_submit').className = 'button disabled';
			document.getElementById('status').innerHTML = 'Stopping...';
			break;
		case 'nonexistent':
			document.getElementById('stopped').style.display = 'none';
			document.getElementById('started').style.display = 'none';
			document.getElementById('command_box').disabled = true;
			document.getElementById('command_submit').className = 'button disabled';
			document.getElementById('status').innerHTML = 'Server is nonexistent.  Contact the administrator to fix this problem.';
			break;
	}

	if(document.getElementById('console').style.display != 'none') {
		log = getLog();
		if(log != '')
			document.getElementById('log').innerHTML = log;
	}

	if(document.getElementById('scripting').style.display != 'none' && document.getElementById('script_console').style.display != 'none') {
		script_log = getScriptLog();
		if(script_log != '')
			document.getElementById('script_log').innerHTML = script_log;
	}

	if(document.getElementById('settings').style.display != 'none' && !settings.hasFocus()) {
		settings_text = getSettings();
		if(settings_text != '')
			settings.setValue(settings_text);
	}

	if(document.getElementById('scripting').style.display != 'none' && document.getElementById('script_editor').style.display != 'none' && !script.hasFocus()) {
		script_text = getScript();
		if(script_text != '')
			script.setValue(script_text);
	}
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

	setInterval(refresh, 500);
}

window.addEventListener('load', load, false);
