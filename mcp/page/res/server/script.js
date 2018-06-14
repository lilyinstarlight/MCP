var servers, server;

var status_last;

var settings, settings_text;
var script, script_text;

var changeServer = function(name) {
	if (name) {
		document.getElementById('loading').className = '';
		document.getElementById('empty').className = 'none';
	}
	else {
		document.getElementById('loading').className = 'none';
		document.getElementById('empty').className = '';
	}

	document.getElementById('console').className = 'none';
	document.getElementById('settings').className = 'none';
	document.getElementById('script').className = 'none';

	server = name;

	document.title = name ? name + ' - Server - MCP' : 'Server - MCP';
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

		if (servers.length === 0)
			changeServer('');
		else if (!server)
			changeServer(servers[0]);

		var select = document.createElement('select');
		for (var name in servers) {
			var option = document.createElement('option');
			option.value = servers[name];
			option.innerHTML = servers[name];
			if (name === server)
				option.setAttribute('selected', 'selected');
			select.appendChild(option);
		}
		document.getElementById('server_select').innerHTML = select.innerHTML;
	});

	if (server) {
		getStatus(server, function(status) {
			if (status === status_last)
				return;

			switch (status) {
				case 'stopped':
					document.getElementById('started').className = 'none';
					document.getElementById('stopped').className = '';
					document.getElementById('command_box').disabled = true;
					document.getElementById('command_submit').disabled = true;
					document.getElementById('status').innerHTML = 'Stopped';

					break;

				case 'starting':
					document.getElementById('started').className = 'none';
					document.getElementById('stopped').className = '';
					document.getElementById('command_box').disabled = true;
					document.getElementById('command_submit').disabled = true;
					document.getElementById('status').innerHTML = 'Starting...';

					break;

				case 'started':
					document.getElementById('started').className = '';
					document.getElementById('stopped').className = 'none';
					document.getElementById('command_box').disabled = false;
					document.getElementById('command_submit').disabled = false;
					document.getElementById('status').innerHTML = 'Running';

					break;

				case 'stopping':
					document.getElementById('started').className = '';
					document.getElementById('stopped').className = 'none';
					document.getElementById('command_box').disabled = true;
					document.getElementById('command_submit').disabled = true;
					document.getElementById('status').innerHTML = 'Stopping...';

					break;

				case 'nonexistent':
					document.getElementById('started').className = 'none';
					document.getElementById('stopped').className = 'none';
					document.getElementById('command_box').disabled = true;
					document.getElementById('command_submit').disabled = true;
					document.getElementById('status').innerHTML = 'Server is nonexistent.  Contact the administrator to fix this problem.';

					break;
			}

			status_last = status;
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

		if (isVisible(document.getElementById('loading'))) {
			document.getElementById('loading').className = 'none';
			document.getElementById('console').className = '';
			document.getElementById('settings').className = 'none';
			document.getElementById('script').className = 'none';
		}
	}

	setTimeout(refresh, 500);
};

var load = function() {
	document.getElementById('console_button').addEventListener('click', function(ev) {
		change('console');

		ev.preventDefault();
	}, false);

	document.getElementById('settings_button').addEventListener('click', function(ev) {
		change('settings');

		ev.preventDefault();
	}, false);

	document.getElementById('script_button').addEventListener('click', function(ev) {
		change('script');

		ev.preventDefault();
	}, false);

	document.getElementById('server_select').addEventListener('change', function(ev) {
		change_server(document.getElementById('server_select').value);

		ev.preventDefault();
	}, false);

	document.getElementById('user_button').addEventListener('click', function(ev) {
		goto('/user');

		ev.preventDefault();
	}, false);

	document.getElementById('admin_button').addEventListener('click', function(ev) {
		goto('/admin');

		ev.preventDefault();
	}, false);

	document.getElementById('logout_button').addEventListener('click', function(ev) {
		unsetCookie();
		goto('/');

		ev.preventDefault();
	}, false);

	document.getElementById('start_button').addEventListener('click', function(ev) {
		start();

		ev.preventDefault();
	}, false);

	document.getElementById('stop_button').addEventListener('click', function(ev) {
		stop();

		ev.preventDefault();
	}, false);

	document.getElementById('reload_button').addEventListener('click', function(ev) {
		reload();

		ev.preventDefault();
	}, false);

	document.getElementById('settings_save_button').addEventListener('click', function(ev) {
		saveSettings();

		ev.preventDefault();
	}, false);

	document.getElementById('script_save_button').addEventListener('click', function(ev) {
		saveScript();

		ev.preventDefault();
	}, false);

	document.getElementById('script_editor_button').addEventListener('click', function(ev) {
		change('script', 'script_editor');

		ev.preventDefault();
	}, false);

	document.getElementById('script_console_button').addEventListener('click', function(ev) {
		change('script', 'script_console');

		ev.preventDefault();
	}, false);

	document.getElementById('command').addEventListener('submit', function(ev) {
		submitCommand();

		ev.preventDefault();
	}, false);

	check(function(admin) {
		if (admin)
			document.getElementById('admin_button').className = '';
	});

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
