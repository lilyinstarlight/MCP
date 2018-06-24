var features = {};

var users, servers, sources, libraries;

var config, config_text;
var user_selected, server_selected, source_selected, library_selected;

var selectUser = function() {
	var selected = [];
	var options = document.getElementById('user_listing').options;
	for (var idx = 0; idx < options.length; idx++) {
		if (options[idx].selected)
			selected.push(options[idx].value);
	}
	user_selected = selected;

	if (selected.length > 0) {
		var user;
		users.forEach(function(user_element) {
			if (user_element.username === user_selected[0]) {
				user = user_element;
				return;
			}
		});

		document.getElementById('user_modify_button').disabled = false;
		document.getElementById('user_destroy_button').disabled = false;

		document.getElementById('user_modify_username').value = user.username;
		document.getElementById('user_modify_password').value = '';
		document.getElementById('user_modify_key').value = '';
		document.getElementById('user_modify_admin').checked = user.admin;
		document.getElementById('user_modify_active').checked = user.active;

		var select = document.createElement('select');
		servers.forEach(function(server) {
			var option = document.createElement('option');
			option.value = server.server;
			option.innerHTML = server.server;
			user.servers.forEach(function(user_server) {
				if (server.server === user_server)
					option.setAttribute('selected', 'selected');
			});
			select.appendChild(option);
		});
		document.getElementById('user_modify_servers').innerHTML = select.innerHTML;
	}
	else {
		document.getElementById('user_modify_button').disabled = true;
		document.getElementById('user_destroy_button').disabled = true;

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
	for (var idx = 0; idx < options.length; idx++) {
		if (options[idx].selected)
			servers.push(options[idx].value);
	}
	createUser(document.getElementById('user_create_username').value, document.getElementById('user_create_password').value, document.getElementById('user_create_key').value, servers, document.getElementById('user_create_admin').checked, document.getElementById('user_create_active').checked, function() {
		document.getElementById('user_create_username').value = '';
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
	for (var idx = 0; idx < options.length; idx++) {
		if (options[idx].selected)
			servers.push(options[idx].value);
	}
	modifyUser(document.getElementById('user_modify_username').value, document.getElementById('user_modify_password').value, document.getElementById('user_modify_key').value, servers, document.getElementById('user_modify_admin').checked, document.getElementById('user_modify_active').checked);
};

var submitDestroyUser = function() {
	user_selected.forEach(function(user) {
		destroyUser(user);
	});
};

var selectServer = function() {
	var selected = []
	var options = document.getElementById('server_listing').options;
	for (var idx = 0; idx < options.length; idx++) {
		if (options[idx].selected)
			selected.push(options[idx].value);
	}
	server_selected = selected;

	if (selected.length > 0) {
		document.getElementById('server_upgrade_button').disabled = false;
		document.getElementById('server_destroy_button').disabled = false;
	}
	else {
		document.getElementById('server_upgrade_button').disabled = true;
		document.getElementById('server_destroy_button').disabled = true;
	}
};

var submitServer = function() {
	createServer(document.getElementById('server_name').value, document.getElementById('server_source').value, document.getElementById('server_library').value, function() {
		document.getElementById('server_name').value = '';
		document.getElementById('server_source').value = '';
		document.getElementById('server_library').value = '';
	});
};

var submitUpgradeServer = function() {
	server_selected.forEach(function(server) {
		upgradeServer(server);
	});
};

var upgradeAllServers = function() {
	servers.forEach(function(server) {
		upgradeServer(server.server);
	});
};

var submitDestroyServer = function() {
	server_selected.forEach(function(server) {
		destroyServer(server);
	});
};

var selectSource = function() {
	var selected = [];
	var options = document.getElementById('source_listing').options;
	for (var idx = 0; idx < options.length; idx++) {
		if (options[idx].selected)
			selected.push(options[idx].value);
	}
	source_selected = selected;

	if (selected.length > 0) {
		document.getElementById('source_update_button').disabled = false;
		document.getElementById('source_remove_button').disabled = false;
	}
	else {
		document.getElementById('source_update_button').disabled = true;
		document.getElementById('source_remove_button').disabled = true;
	}
};

var submitSource = function() {
	addSource(document.getElementById('source_name').value, document.getElementById('source_bzr').value, function() {
		document.getElementById('source_name').value = '';
		document.getElementById('source_bzr').value = '';
	});
};

var submitUpdateSource = function() {
	source_selected.forEach(function(source) {
		updateSource(source);
	});
};

var updateAllSources = function() {
	sources.forEach(function(source) {
		updateSource(source.source)
	});
};

var submitRemoveSource = function() {
	source_selected.forEach(function(source) {
		removeSource(source);
	});
};

var selectLibrary = function() {
	var selected = [];
	var options = document.getElementById('library_listing').options;
	for (var idx = 0; idx < options.length; idx++) {
		if (options[idx].selected)
			selected.push(options[idx].value);
	}
	library_selected = selected;

	if (selected.length > 0) {
		document.getElementById('library_update_button').disabled = false;
		document.getElementById('library_remove_button').disabled = false;
	}
	else {
		document.getElementById('library_update_button').disabled = true;
		document.getElementById('library_remove_button').disabled = true;
	}
};

var submitLibrary = function() {
	addLibrary(document.getElementById('library_name').value, document.getElementById('library_bzr').value, function() {
		document.getElementById('library_name').value = '';
		document.getElementById('library_bzr').value = '';
	});
};

var submitUpdateLibrary = function() {
	library_selected.forEach(function(library) {
		updateLibrary(library);
	});
};

var updateAllLibraries = function() {
	libraries.forEach(function(library) {
		updateLibrary(library.library)
	});
};

var submitRemoveLibrary = function() {
	library_selected.forEach(function(library) {
		removeLibrary(library);
	});
};

var saveConfig = function() {
	updateConfig(config.getValue(), function() {
		alert('Config successfully saved');
	});
};

var restartDaemon = function() {
	restart(function() {
		alert('Daemon successfully restarted');
	});
};

var refresh = function(force) {
	if (typeof force !== 'boolean')
		force = false;

	if (count > 0) {
		setTimeout(refresh, 200);
		return;
	}

	getFeatures(function(response) {
		if (response === features)
			return;

		features = response;

		if (features.creation) {
			document.getElementById('config_button').disabled = false;
			if (isVisible(document.getElementById('server_button')) || force)
				document.getElementById('server_button').disabled = false;
		}
		else {
			document.getElementById('config_button').disabled = true;
			if (isVisible(document.getElementById('server_button')) || force)
				document.getElementById('server_button').disabled = true;
		}
	});

	getUsers(function(response) {
		if (response === users)
			return;

		users = response;

		if (isVisible(document.getElementById('user_listing')) || force) {
			var select = document.createElement('select');
			users.forEach(function(user) {
				var option = document.createElement('option');
				option.value = user.username;
				option.innerHTML = user.username + (user.admin ? ' (Admin)' : '') + (user.active ? '' : ' (Inactive)') + (user.servers.length > 0 ? ' - ' + user.servers.join(', ') : '');
				select.appendChild(option);
			});
			if (document.getElementById('user_listing').innerHTML !== select.innerHTML) {
				document.getElementById('user_listing').innerHTML = select.innerHTML;
				selectUser();
			}
		}
	});

	getServers(function(response) {
		if (response === servers)
			return;

		servers = response;

		if (isVisible(document.getElementById('server_listing')) || force) {
			var select = document.createElement('select');
			servers.forEach(function(server) {
				var option = document.createElement('option');
				option.value = server.server;
				option.innerHTML = server.server + ' - ' + server.source + ' (r' + server.revision + ')';
				select.appendChild(option);
			});
			if (document.getElementById('server_listing').innerHTML !== select.innerHTML) {
				document.getElementById('server_listing').innerHTML = select.innerHTML;
				selectServer();
			}
		}

		if (isVisible(document.getElementById('user_create_servers')) || force) {
			var select = document.createElement('select');
			servers.forEach(function(server) {
				var option = document.createElement('option');
				option.value = server.server;
				option.innerHTML = server.server;
				select.appendChild(option);
			});
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
			sources.forEach(function(source) {
				var option = document.createElement('option');
				option.value = source.source;
				option.innerHTML = source.source + ' - r' + source.revision;
				select.appendChild(option);
			});
			if (document.getElementById('source_listing').innerHTML !== select.innerHTML) {
				document.getElementById('source_listing').innerHTML = select.innerHTML;
				selectSource();
			}
		}

		if (isVisible(document.getElementById('server_source')) || force) {
			var select = document.createElement('select');
			sources.forEach(function(source) {
				var option = document.createElement('option');
				option.value = source.source;
				option.innerHTML = source.source;
				select.appendChild(option);
			});
			if (document.getElementById('server_source').innerHTML !== select.innerHTML)
				document.getElementById('server_source').innerHTML = select.innerHTML;
		}
	});

	getLibraries(function(response) {
		if (response === libraries)
			return;

		libraries = response;

		if (isVisible(document.getElementById('library_listing')) || force) {
			var select = document.createElement('select');
			libraries.forEach(function(library) {
				var option = document.createElement('option');
				option.value = library.library;
				option.innerHTML = library.library + ' - r' + library.revision;
				select.appendChild(option);
			});
			if (document.getElementById('library_listing').innerHTML !== select.innerHTML) {
				document.getElementById('library_listing').innerHTML = select.innerHTML;
				selectLibrary();
			}
		}

		if (isVisible(document.getElementById('server_library')) || force) {
			var select = document.createElement('select');
			var option = document.createElement('option');
			option.value = '';
			option.innerHTML = 'None';
			select.appendChild(option);
			libraries.forEach(function(library) {
				var option = document.createElement('option');
				option.value = library.library;
				option.innerHTML = library.library;
				select.appendChild(option);
			});
			if (document.getElementById('server_library').innerHTML !== select.innerHTML)
				document.getElementById('server_library').innerHTML = select.innerHTML;
		}
	});

	if ((isVisible(document.getElementById('config_editor')) || force) && features.creation) {
		getConfig(function(response) {
			if (config_text === response)
				return;

			config_text = response;
			config.setValue(config_text);
		});
	}

	if (isVisible(document.getElementById('loading'))) {
		document.getElementById('loading').className = 'none';
		document.getElementById('users').className = '';
		document.getElementById('servers').className = 'none';
		document.getElementById('sources').className = 'none';
		document.getElementById('config').className = 'none';
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

	document.getElementById('libraries_button').addEventListener('click', function(ev) {
		change('libraries');

		ev.preventDefault();
	}, false);

	document.getElementById('config_button').addEventListener('click', function(ev) {
		change('config');
		config.refresh();

		ev.preventDefault();
	}, false);

	document.getElementById('restart_button').addEventListener('click', function(ev) {
		restartDaemon();

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
		submitDestroyUser();

		ev.preventDefault();
	}, false);

	document.getElementById('user_listing').addEventListener('change', function(ev) {
		selectUser();

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
		submitUser();
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
		submitModifyUser();
		change('users', 'user_list');

		ev.preventDefault();
	}, false);

	document.getElementById('server_create_button').addEventListener('click', function(ev) {
		change('servers', 'server_create');

		ev.preventDefault();
	}, false);

	document.getElementById('server_upgrade_button').addEventListener('click', function(ev) {
		submitUpgradeServer();

		ev.preventDefault();
	}, false);

	document.getElementById('server_destroy_button').addEventListener('click', function(ev) {
		submitDestroyServer();

		ev.preventDefault();
	}, false);

	document.getElementById('server_upgrade_all_button').addEventListener('click', function(ev) {
		upgradeAllServers();

		ev.preventDefault();
	}, false);

	document.getElementById('server_listing').addEventListener('change', function(ev) {
		selectServer();

		ev.preventDefault();
	}, false);

	document.getElementById('server_cancel').addEventListener('click', function(ev) {
		change('servers', 'server_list');

		ev.preventDefault();
	}, false);

	document.getElementById('server_submit').addEventListener('click', function(ev) {
		submitServer();
		change('servers', 'server_list');

		ev.preventDefault();
	}, false);

	document.getElementById('source_add_button').addEventListener('click', function(ev) {
		change('sources', 'source_add');

		ev.preventDefault();
	}, false);

	document.getElementById('source_update_button').addEventListener('click', function(ev) {
		submitUpdateSource();

		ev.preventDefault();
	}, false);

	document.getElementById('source_remove_button').addEventListener('click', function(ev) {
		submitRemoveSource();

		ev.preventDefault();
	}, false);

	document.getElementById('source_update_all_button').addEventListener('click', function(ev) {
		updateAllSources();

		ev.preventDefault();
	}, false);

	document.getElementById('source_listing').addEventListener('change', function(ev) {
		selectSource();

		ev.preventDefault();
	}, false);

	document.getElementById('source_cancel').addEventListener('click', function(ev) {
		change('sources', 'source_list');

		ev.preventDefault();
	}, false);

	document.getElementById('source_submit').addEventListener('click', function(ev) {
		submitSource();
		change('sources', 'source_list');

		ev.preventDefault();
	}, false);

	document.getElementById('library_add_button').addEventListener('click', function(ev) {
		change('libraries', 'library_add');

		ev.preventDefault();
	}, false);

	document.getElementById('library_update_button').addEventListener('click', function(ev) {
		submitUpdateLibrary();

		ev.preventDefault();
	}, false);

	document.getElementById('library_remove_button').addEventListener('click', function(ev) {
		submitRemoveLibrary();

		ev.preventDefault();
	}, false);

	document.getElementById('library_update_all_button').addEventListener('click', function(ev) {
		updateAllLibraries();

		ev.preventDefault();
	}, false);

	document.getElementById('library_listing').addEventListener('change', function(ev) {
		selectLibrary();

		ev.preventDefault();
	}, false);

	document.getElementById('library_cancel').addEventListener('click', function(ev) {
		change('libraries', 'library_list');

		ev.preventDefault();
	}, false);

	document.getElementById('library_submit').addEventListener('click', function(ev) {
		submitLibrary();
		change('libraries', 'library_list');

		ev.preventDefault();
	}, false);

	document.getElementById('config_submit').addEventListener('click', function(ev) {
		saveConfig();

		ev.preventDefault();
	}, false);

	config = CodeMirror(document.getElementById('config_codemirror'), {
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
