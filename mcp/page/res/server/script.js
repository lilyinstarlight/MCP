var servers, server;

var settings, settings_text;
var script, script_text;

var changeServer = function(name) {
	server = name;
	document.title = name ? name + ' - Server Administration' : 'Server Administration';
};

var startServer = function() {
	start(server);
};

var stopServer = function() {
	stop(server);
};

var restartServer = function() {
	restart(server);
};

var reloadServer = function() {
	reload(server);
};

var submitCommand = function() {
	sendCommand(server, document.getElementById('command_box').value);
	document.getElementById('command_box').value = '';
};

var saveSettings = function() {
	updateSettings(server, settings.getValue(), function() {
		alert('Settings successfully saved');
	});
};

var saveScript = function() {
	updateScript(server, script.getValue(), function() {
		alert('Script successfully saved');
	});
};

var refresh = function(force) {
	if (typeof force !== 'boolean')
		force = false;

	getServers(function(response) {
		servers = response;

		if (servers.length === 0) {
			changeServer('');
			document.getElementById('content').style.display = 'none';
			document.getElementById('navigation').style.display = 'none';
		}
		else if (!server) {
			changeServer(servers[0]);
			document.getElementById('content').style.display = 'block';
			document.getElementById('navigation').style.display = 'inline';
		}

		var select = document.createElement('select');
		for (var name in servers) {
			var option = document.createElement('option');
			option.value = servers[name];
			option.innerHTML = servers[name];
			if (name === server)
				option.setAttribute('selected', 'selected');
			select.appendChild(option);
		}
		document.getElementById('servers').innerHTML = select.innerHTML;
	});

	if (server) {
		getStatus(server, function(status) {
			switch (status) {
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
		});

		if (isVisible(document.getElementById('log')) || force) {
			getLog(server, function(response) {
				document.getElementById('log').innerHTML = response;
			});
		}

		if (isVisible(document.getElementById('script_log')) || force) {
			getScriptLog(server, function(response) {
				document.getElementById('script_log').innerHTML = response;
			});
		}

		if (isVisible(document.getElementById('settings_editor')) || force) {
			getSettings(server, function(response) {
				if (settings_text === response)
					return;
				settings_text = response;
				settings.setValue(settings_text);
			});
		}

		if (isVisible(document.getElementById('script_editor')) || force) {
			getScript(server, function(response) {
				if (script_text === response)
					return;

				script_text = response;
				script.setValue(script_text);
			});
		}
	}

	setTimeout(refresh, 500);
};

var load = function() {
	settings = CodeMirror(document.getElementById('settings_editor'), {
		mode: 'settings',
		lineNumbers: true,
		lineWrapping: true,
		showTrailingSpace: true,
		theme: 'mcp',
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
		theme: 'mcp',
		placeholder: 'Here you can add a custom server script written in Python.  There is an API available that makes it easy to add ladderlog event handlers and chat commands but also keeps track of various game elements.  Check the API for details.'
	});

	refresh(true);
};

window.addEventListener('load', load, false);
