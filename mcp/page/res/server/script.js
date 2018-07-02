var servers, selected;

var server_last;

var log_last = 0;
var script_log_last = 0;

var settings, settings_text;
var script, script_text;
var library;

var changeServer = function(name) {
	if (name) {
		document.getElementById('loading').className = '';
		document.getElementById('empty').className = 'none';

		document.getElementById('console_button').disabled = false;
		document.getElementById('settings_button').disabled = false;
		document.getElementById('script_button').disabled = false;

		document.getElementById('console').className = '';
		document.getElementById('settings').className = 'none';
		document.getElementById('script').className = 'none';
	}
	else {
		document.getElementById('loading').className = 'none';
		document.getElementById('empty').className = '';

		document.getElementById('console_button').disabled = true;
		document.getElementById('settings_button').disabled = true;
		document.getElementById('script_button').disabled = true;

		document.getElementById('console').className = 'none';
		document.getElementById('settings').className = 'none';
		document.getElementById('script').className = 'none';
	}

	selected = name;

	document.title = name ? name + ' - Server - MCP' : 'Server - MCP';
};

var startServer = function() {
	document.getElementById('started').className = 'none';
	document.getElementById('stopped').className = 'none';
	document.getElementById('command_input').disabled = true;
	document.getElementById('command_submit').disabled = true;
	document.getElementById('status').innerHTML = 'Starting';

	start(selected);
};

var stopServer = function() {
	document.getElementById('started').className = 'none';
	document.getElementById('stopped').className = 'none';
	document.getElementById('command_input').disabled = true;
	document.getElementById('command_submit').disabled = true;
	document.getElementById('status').innerHTML = 'Stopping';

	stop(selected);
};

var restartServer = function() {
	document.getElementById('started').className = 'none';
	document.getElementById('stopped').className = 'none';
	document.getElementById('command_input').disabled = true;
	document.getElementById('command_submit').disabled = true;
	document.getElementById('status').innerHTML = 'Restarting';

	restart(selected);
};

var reloadServer = function() {
	reload(selected);
};

var submitCommand = function() {
	sendCommand(selected, document.getElementById('command_input').value);
	document.getElementById('command_input').value = '';
};

var saveSettings = function() {
	updateSettings(selected, settings.getValue(), function() {
		alert('Settings successfully saved');
	});
};

var saveScript = function() {
	updateScript(selected, script.getValue(), function() {
		alert('Script successfully saved');
	});
};

var refresh = function(force) {
	if (typeof force !== 'boolean')
		force = false;

	if (count > 0 && !force) {
		setTimeout(refresh, 200);
		return;
	}

	getServers(function(response) {
		if (response === servers)
			return;

		servers = response;

		if (servers.length === 0)
			changeServer('');
		else if (!selected)
			changeServer(servers[0].server);

		var select = document.createElement('select');
		servers.forEach(function(server) {
			var option = document.createElement('option');
			option.value = server.server;
			option.innerHTML = server.server;
			if (server.server === selected)
				option.setAttribute('selected', 'selected');
			select.appendChild(option);
		});
		document.getElementById('server_select').innerHTML = select.innerHTML;
	});

	if (selected) {
		getStatus(selected, function(server) {
			if (server === server_last)
				return;

			if (server.running) {
				if (server.waiting) {
					document.getElementById('started').className = 'none';
					document.getElementById('stopped').className = 'none';
					document.getElementById('command_input').disabled = true;
					document.getElementById('command_submit').disabled = true;
					document.getElementById('status').innerHTML = 'Starting';
				}
				else {
					document.getElementById('started').className = '';
					document.getElementById('stopped').className = 'none';
					document.getElementById('command_input').disabled = false;
					document.getElementById('command_submit').disabled = false;
					document.getElementById('status').innerHTML = 'Running';
				}
			}
			else {
				if (server.waiting) {
					document.getElementById('started').className = 'none';
					document.getElementById('stopped').className = 'none';
					document.getElementById('command_input').disabled = true;
					document.getElementById('command_submit').disabled = true;
					document.getElementById('status').innerHTML = 'Stopping';
				}
				else {
					document.getElementById('started').className = 'none';
					document.getElementById('stopped').className = '';
					document.getElementById('command_input').disabled = true;
					document.getElementById('command_submit').disabled = true;
					document.getElementById('status').innerHTML = 'Stopped';
				}
			}

			library = server.library;

			server_last = server;
		});

		if (isVisible(document.getElementById('log')) || force) {
			getLog(selected, log_last, function(response, last) {
				log_last = last;

				var scroll = Math.floor(document.getElementById('log').scrollTop + document.getElementById('log').clientHeight) == document.getElementById('log').scrollHeight || force;

				document.getElementById('log').innerHTML += response;

				if (scroll) {
					if (force) {
						setTimeout(function() {
							document.getElementById('log').scrollTop = document.getElementById('log').scrollHeight - document.getElementById('log').clientHeight;
						}, 500);
					}
					else {
						document.getElementById('log').scrollTop = document.getElementById('log').scrollHeight - document.getElementById('log').clientHeight;
					}
				}
			});
		}

		if (isVisible(document.getElementById('script_log')) || force) {
			getScriptLog(selected, script_log_last, function(response, last) {
				script_log_last = last;

				var scroll = Math.floor(document.getElementById('script_log').scrollTop + document.getElementById('script_log').clientHeight) == document.getElementById('script_log').scrollHeight || force;

				document.getElementById('script_log').innerHTML += response;

				if (scroll) {
					if (force) {
						setTimeout(function() {
							document.getElementById('script_log').scrollTop = document.getElementById('script_log').scrollHeight - document.getElementById('script_log').clientHeight;
						}, 500);
					}
					else {
						document.getElementById('script_log').scrollTop = document.getElementById('script_log').scrollHeight - document.getElementById('script_log').clientHeight;
					}
				}
			});
		}

		if (isVisible(document.getElementById('settings_editor')) || force) {
			getSettings(selected, function(response) {
				if (settings_text === response)
					return;

				settings_text = response;
				settings.setValue(settings_text);
			});
		}

		if (isVisible(document.getElementById('script_editor')) || force) {
			getScript(selected, function(response) {
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
		settings.refresh();

		ev.preventDefault();
	}, false);

	document.getElementById('script_button').addEventListener('click', function(ev) {
		change('script');
		script.refresh();

		ev.preventDefault();
	}, false);

	document.getElementById('server_select').addEventListener('change', function(ev) {
		changeServer(document.getElementById('server_select').value);

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
		startServer();

		ev.preventDefault();
	}, false);

	document.getElementById('stop_button').addEventListener('click', function(ev) {
		stopServer();

		ev.preventDefault();
	}, false);

	document.getElementById('restart_button').addEventListener('click', function(ev) {
		restartServer();

		ev.preventDefault();
	}, false);

	document.getElementById('reload_button').addEventListener('click', function(ev) {
		reloadServer();

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
		script.refresh();

		ev.preventDefault();
	}, false);

	document.getElementById('script_console_button').addEventListener('click', function(ev) {
		change('script', 'script_console');

		ev.preventDefault();
	}, false);

	document.getElementById('script_doc_button').addEventListener('click', function(ev) {
		goto('/api/script/' + library + '/doc', true);

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

	settings = CodeMirror(document.getElementById('settings_codemirror'), {
		mode: 'settings',
		lineNumbers: true,
		lineWrapping: true,
		showTrailingSpace: true,
		theme: 'mcp',
		placeholder: 'Here you can specify your server\'s custom settings.  There is no need to set TALK_TO_MASTER or GLOBAL_ID here, but you should set your server\'s name and set yourself as an Owner.'
	});

	script = CodeMirror(document.getElementById('script_codemirror'), {
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
