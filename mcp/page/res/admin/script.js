var features = {};

var users, servers, sources;

var config, config_text;
var user_selected, server_selected, source_selected;

var userSelect = function() {
	var selected = []
	var options = document.getElementById('user_listing').options;
	for (var option in options) {
		if (options[option].selected)
			selected.push(options[option].value);
	}
	user_selected = selected;

	if (selected.length > 0) {
		document.getElementById('user_modify_button').className = 'button';
		document.getElementById('user_destroy_button').className = 'button';

		document.getElementById('user_modify_username').value = selected[0];
		document.getElementById('user_modify_password').value = '';
		document.getElementById('user_modify_key').value = '';
		document.getElementById('user_modify_admin').checked = users[selected[0]].admin;
		document.getElementById('user_modify_active').checked = users[selected[0]].active;

		var user_servers = users[selected[0]].servers;
		var select = document.createElement('select');
		for (var server in servers) {
			var option = document.createElement('option');
			option.value = server;
			option.innerHTML = server;
			for (var user_server in user_servers) {
				if (server === user_servers[user_server])
					option.setAttribute('selected', 'selected');
			}
			select.appendChild(option);
		}
		document.getElementById('user_modify_servers').innerHTML = select.innerHTML;
	}
	else {
		document.getElementById('user_modify_button').className = 'button disabled';
		document.getElementById('user_destroy_button').className = 'button disabled';

		document.getElementById('user_modify_username').value = '';
		document.getElementById('user_modify_password').value = '';
		document.getElementById('user_modify_key').value = '';
		document.getElementById('user_modify_admin').checked = false;
		document.getElementById('user_modify_active').checked = false;
		document.getElementById('user_modify_servers').innerHTML = '';
	}
};

var generateKey = function() {
	var chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

	var key = '';
	for (var i = 0; i < 24; i++)
		key += chars.charAt(Math.floor(Math.random() * chars.length));

	return key;
};

var submitUser = function() {
	var servers = [];
	var options = document.getElementById('user_create_servers').options;
	for (var option in options) {
		if (options[option].selected)
			servers.push(options[option].value);
	}
	createUser(document.getElementById('user_create_name').value, document.getElementById('user_create_password').value, document.getElementById('user_create_key').value, servers.join(','), document.getElementById('user_create_admin').checked, document.getElementById('user_create_active').checked, function() {
		document.getElementById('user_create_name').value = '';
		document.getElementById('user_create_password').value = '';
		document.getElementById('user_create_key').value = '';
		document.getElementById('user_create_admin').checked = false;
		document.getElementById('user_create_active').checked = true;
		document.getElementById('user_create_servers').innerHTML = '';
	});
};

var submitModifyUser = function() {
	var servers = [];
	var options = document.getElementById('user_modify_servers').options;
	for (var option in options) {
		if (options[option].selected)
			servers.push(options[option].value);
	}
	modifyUser(document.getElementById('user_modify_username').value, document.getElementById('user_modify_password').value, document.getElementById('user_modify_key').value, servers.join(','), document.getElementById('user_modify_admin').checked, document.getElementById('user_modify_active').checked);
};

var userDestroy = function() {
	for (var user in user_selected)
		destroyUser(user_selected[user])
};

var serverSelect = function() {
	var selected = []
	var options = document.getElementById('server_listing').options;
	for (var option in options) {
		if (options[option].selected)
			selected.push(options[option].value);
	}
	server_selected = selected;

	if (selected.length > 0) {
		document.getElementById('server_upgrade_button').className = 'button';
		document.getElementById('server_destroy_button').className = 'button';
	}
	else {
		document.getElementById('server_upgrade_button').className = 'button disabled';
		document.getElementById('server_destroy_button').className = 'button disabled';
	}
};

var submitServer = function() {
	createServer(document.getElementById('server_name').value, document.getElementById('server_source').value, function() {
		document.getElementById('server_name').value = '';
		document.getElementById('server_source').innerHTML = '';
	});
};

var serverUpgrade = function() {
	for (var server in server_selected)
		upgradeServer(server_selected[server])
};

var serverUpgradeAll = function() {
	for (var server in servers)
		upgradeServer(server['name'])
};

var serverDestroy = function() {
	for (var server in server_selected)
		destroyServer(server_selected[server])
};

var sourceSelect = function() {
	var selected = []
	var options = document.getElementById('source_listing').options;
	for (var option in options) {
		if (options[option].selected)
			selected.push(options[option].value);
	}
	source_selected = selected;

	if (selected.length > 0) {
		document.getElementById('source_update_button').className = 'button';
		document.getElementById('source_remove_button').className = 'button';
	}
	else {
		document.getElementById('source_update_button').className = 'button disabled';
		document.getElementById('source_remove_button').className = 'button disabled';
	}
};

var submitSource = function() {
	addSource(document.getElementById('source_name').value, document.getElementById('source_bzr').value, function() {
		document.getElementById('source_name').value = '';
		document.getElementById('source_bzr').value = '';
	});
};

var sourceUpdate = function() {
	for (var source in source_selected)
		updateSource(source_selected[source])
};

var sourceRemove = function() {
	for (var source in source_selected)
		removeSource(source_selected[source])
};

var saveConfig = function() {
	updateConfig(config.getValue(), function() {
		alert('Config successfully saved');
	});
};

var refresh = function(force) {
	if (typeof force !== 'boolean')
		force = false;

	getFeatures(function(response) {
		if (response === features)
			return;

		features = response;

		if (features.creation) {
			document.getElementById('config_button').className = 'button';
			if (isVisible(document.getElementById('server_create_button')) || force)
				document.getElementById('server_create_button').className = 'button';
		}
		else {
			document.getElementById('config_button').className = 'button disabled';
			if (isVisible(document.getElementById('server_create_button')) || force)
				document.getElementById('server_create_button').className = 'button disabled';
		}
	});

	getUsers(function(response) {
		if (response === users)
			return;

		users = response;

		if (isVisible(document.getElementById('user_listing')) || force) {
			var select = document.createElement('select');
			for (var user in users) {
				var option = document.createElement('option');
				option.value = user;
				option.innerHTML = user + (response[user].admin ? ' (Admin)' : '') + (response[user].active ? '' : ' (Inactive)') + (response[user].servers.length > 0 ? ' - ' + response[user].servers.join(', ') : '');
				select.appendChild(option);
			}
			if (document.getElementById('user_listing').innerHTML !== select.innerHTML) {
				document.getElementById('user_listing').innerHTML = select.innerHTML;
				userSelect();
			}
		}
	});

	getServers(function(response) {
		if (response === servers)
			return;

		servers = response;

		if (isVisible(document.getElementById('server_listing')) || force) {
			var select = document.createElement('select');
			for (var server in servers) {
				var option = document.createElement('option');
				option.value = server;
				option.innerHTML = server + ' - ' + response[server].source + ' (r' + response[server].revision + ')';
				select.appendChild(option);
			}
			if (document.getElementById('server_listing').innerHTML !== select.innerHTML) {
				document.getElementById('server_listing').innerHTML = select.innerHTML;
				serverSelect();
			}
		}

		if (isVisible(document.getElementById('user_create_servers')) || force) {
			var select = document.createElement('select');
			for (var server in servers) {
				var option = document.createElement('option');
				option.value = server;
				option.innerHTML = server;
				select.appendChild(option);
			}
			if (document.getElementById('user_create_servers').innerHTML !== select.innerHTML)
				document.getElementById('user_create_servers').innerHTML = select.innerHTML;
		}
	});

	getSources(function(response) {
		if (response === sources)
			return;

		sources = response;

		if (isVisible(document.getElementById('source_listing')) || force) {
			var select = document.createElement('select');
			for (var source in sources) {
				var option = document.createElement('option');
				option.value = source;
				option.innerHTML = source + ' - r' + response[source].revision;
				select.appendChild(option);
			}
			if (document.getElementById('source_listing').innerHTML !== select.innerHTML) {
				document.getElementById('source_listing').innerHTML = select.innerHTML;
				sourceSelect();
			}
		}

		if (isVisible(document.getElementById('server_source')) || force) {
			var select = document.createElement('select');
			for (var source in sources) {
				var option = document.createElement('option');
				option.value = source;
				option.innerHTML = source;
				select.appendChild(option);
			}
			if (document.getElementById('server_source').innerHTML !== select.innerHTML)
				document.getElementById('server_source').innerHTML = select.innerHTML;
		}
	});

	if ((isVisible(document.getElementById('config_editor')) || force) && features.creation) {
		getConfig(function(response) {
			if (config_text === response)
				return;

			config_text = response;
			config.setValue(response);
		});
	}

	setTimeout(refresh, 500);
};

var load = function() {
	document.getElementById('users_button').addEventListener('click', function(ev) {
		change('users');

		ev.preventDefault();
	}, false);

	document.getElementById('servers_button').addEventListener('click', function(ev) {
		change('servers');

		ev.preventDefault();
	}, false);

	document.getElementById('sources_button').addEventListener('click', function(ev) {
		change('sources');

		ev.preventDefault();
	}, false);

	document.getElementById('config_button').addEventListener('click', function(ev) {
		change('config');

		ev.preventDefault();
	}, false);

	document.getElementById('server_button').addEventListener('click', function(ev) {
		goto('/server');

		ev.preventDefault();
	}, false);

	document.getElementById('user_button').addEventListener('click', function(ev) {
		goto('/user');

		ev.preventDefault();
	}, false);

	document.getElementById('logout_button').addEventListener('click', function(ev) {
		unsetCookie();
		goto('/');

		ev.preventDefault();
	}, false);

	document.getElementById('user_create_button').addEventListener('click', function(ev) {
		change('users', 'user_create');

		ev.preventDefault();
	}, false);

	document.getElementById('user_modify_button').addEventListener('click', function(ev) {
		change('users', 'user_modify');

		ev.preventDefault();
	}, false);

	document.getElementById('user_destroy_button').addEventListener('click', function(ev) {
		userDestroy();

		ev.preventDefault();
	}, false);

	document.getElementById('user_listing').addEventListener('change', function(ev) {
		userSelect();

		ev.preventDefault();
	}, false);

	document.getElementById('user_create_generate').addEventListener('click', function(ev) {
		document.getElementById('user_create_form').elements['key'].value = generateKey();

		ev.preventDefault();
	}, false);

	document.getElementById('user_create_cancel').addEventListener('click', function(ev) {
		change('users', 'user_list');

		ev.preventDefault();
	}, false);

	document.getElementById('user_create_submit').addEventListener('click', function(ev) {
		userCreate();
		change('users', 'user_list');

		ev.preventDefault();
	}, false);

	document.getElementById('user_modify_generate').addEventListener('click', function(ev) {
		document.getElementById('user_modify_form').elements['key'].value = generateKey();

		ev.preventDefault();
	}, false);

	document.getElementById('user_modify_cancel').addEventListener('click', function(ev) {
		change('users', 'user_list');

		ev.preventDefault();
	}, false);

	document.getElementById('user_modify_submit').addEventListener('click', function(ev) {
		userCreate();
		change('users', 'user_list');

		ev.preventDefault();
	}, false);

	document.getElementById('server_create_button').addEventListener('click', function(ev) {
		change('servers', 'server_create');

		ev.preventDefault();
	}, false);

	document.getElementById('server_upgrade_button').addEventListener('click', function(ev) {
		serverUpgrade();

		ev.preventDefault();
	}, false);

	document.getElementById('server_destroy_button').addEventListener('click', function(ev) {
		serverDestroy();

		ev.preventDefault();
	}, false);

	document.getElementById('server_upgrade_all_button').addEventListener('click', function(ev) {
		serverUpgradeAll();

		ev.preventDefault();
	}, false);

	document.getElementById('server_listing').addEventListener('change', function(ev) {
		serverSelect();

		ev.preventDefault();
	}, false);

	document.getElementById('server_cancel').addEventListener('click', function(ev) {
		change('servers', 'server_list');

		ev.preventDefault();
	}, false);

	document.getElementById('server_submit').addEventListener('click', function(ev) {
		serverSubmit();
		change('servers', 'server_list');

		ev.preventDefault();
	}, false);

	document.getElementById('source_add_button').addEventListener('click', function(ev) {
		change('sources', 'source_add');

		ev.preventDefault();
	}, false);

	document.getElementById('source_update_button').addEventListener('click', function(ev) {
		sourceUpdate();

		ev.preventDefault();
	}, false);

	document.getElementById('source_remove_button').addEventListener('click', function(ev) {
		sourceRemove();

		ev.preventDefault();
	}, false);

	document.getElementById('source_update_all_button').addEventListener('click', function(ev) {
		sourceUpdateAll();

		ev.preventDefault();
	}, false);

	document.getElementById('source_listing').addEventListener('change', function(ev) {
		sourceSelect();

		ev.preventDefault();
	}, false);

	document.getElementById('source_cancel').addEventListener('click', function(ev) {
		change('sources', 'source_list');

		ev.preventDefault();
	}, false);

	document.getElementById('source_submit').addEventListener('click', function(ev) {
		serverSubmit();
		change('sources', 'source_list');

		ev.preventDefault();
	}, false);

	document.getElementById('config_submit').addEventListener('click', function(ev) {
		configSave();

		ev.preventDefault();
	}, false);

	config = CodeMirror(document.getElementById('config_editor'), {
		mode: 'settings',
		lineNumbers: true,
		lineWrapping: true,
		showTrailingSpace: true,
		theme: 'mcp',
		placeholder: 'Here you can specify configuration global to every server.  Generally GLOBAL_ID and TALK_TO_MASTER are turned on here but you should also specify a SERVER_DNS.'
	});

	refresh(true);
};

window.addEventListener('load', load, false);
