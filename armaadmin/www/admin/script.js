var users, servers, sources;
var config, config_text;
var user_selected, server_selected, source_selected;

function userSelect() {
	var selected = []
	var options = document.getElementById('user_listing').options;
	for(var option in options) {
		if(options[option].selected)
			selected.push(options[option].value);
	}
	user_selected = selected;

	if(selected.length > 0) {
		document.getElementById('user_modify_button').className = 'button';
		document.getElementById('user_destroy_button').className = 'button';

		document.getElementById('user_modify_name').value = selected[0];
		document.getElementById('user_modify_password').value = '';
		document.getElementById('user_modify_admin').checked = users[selected[0]].admin;

		var user_servers = users[selected[0]].servers;
		var select = document.createElement('select');
		for(var server in servers) {
			var option = document.createElement('option');
			option.value = server;
			option.innerHTML = server;
			for(var user_server in user_servers) {
				if(server == user_servers[user_server])
					option.setAttribute('selected', 'selected');
			}
			select.appendChild(option);
		}
		document.getElementById('user_modify_servers').innerHTML = select.innerHTML;
	}
	else {
		document.getElementById('user_modify_button').className = 'button disabled';
		document.getElementById('user_destroy_button').className = 'button disabled';

		document.getElementById('user_modify_name').value = '';
		document.getElementById('user_modify_password').value = '';
		document.getElementById('user_modify_admin').checked = false;
		document.getElementById('user_modify_servers').innerHTML = '';
	}
}

function submitUser() {
	var servers = [];
	var options = document.getElementById('user_create_servers').options;
	for(var option in options) {
		if(options[option].selected)
			servers.push(options[option].value);
	}
	createUser(document.getElementById('user_create_name').value, document.getElementById('user_create_password').value, servers.join(','), document.getElementById('user_create_admin').checked);
}

function submitModifyUser() {
	var servers = [];
	var options = document.getElementById('user_modify_servers').options;
	for(var option in options) {
		if(options[option].selected)
			servers.push(options[option].value);
	}
	modifyUser(document.getElementById('user_modify_name').value, document.getElementById('user_modify_password').value, servers.join(','), document.getElementById('user_modify_admin').checked);
}

function userDestroy() {
	for(var user in user_selected)
		destroyUser(user_selected[user])
}

function serverSelect() {
	var selected = []
	var options = document.getElementById('server_listing').options;
	for(var option in options) {
		if(options[option].selected)
			selected.push(options[option].value);
	}
	server_selected = selected;

	if(selected.length > 0) {
		document.getElementById('server_upgrade_button').className = 'button';
		document.getElementById('server_destroy_button').className = 'button';
	}
	else {
		document.getElementById('server_upgrade_button').className = 'button disabled';
		document.getElementById('server_destroy_button').className = 'button disabled';
	}
}

function submitServer() {
	createServer(document.getElementById('server_name').value, document.getElementById('server_source').value);
}

function serverUpgrade() {
	for(var server in server_selected)
		upgradeServer(server_selected[server])
}

function serverDestroy() {
	for(var server in server_selected)
		destroyServer(server_selected[server])
}

function sourceSelect() {
	var selected = []
	var options = document.getElementById('source_listing').options;
	for(var option in options) {
		if(options[option].selected)
			selected.push(options[option].value);
	}
	source_selected = selected;

	if(selected.length > 0) {
		document.getElementById('source_update_button').className = 'button';
		document.getElementById('source_remove_button').className = 'button';
	}
	else {
		document.getElementById('source_update_button').className = 'button disabled';
		document.getElementById('source_remove_button').className = 'button disabled';
	}
}

function submitSource() {
	addSource(document.getElementById('source_name').value, document.getElementById('source_bzr').value);
}

function sourceUpdate() {
	for(var source in source_selected)
		updateSource(source_selected[source])
}

function sourceRemove() {
	for(var source in source_selected)
		removeSource(source_selected[source])
}

function refresh() {
	getUsers(function(response) {
		users = response;

		if(isVisible(document.getElementById('user_listing'))) {
			var select = document.createElement('select');
			for(var user in response) {
				var option = document.createElement('option');
				option.value = user;
				option.innerHTML = user + (response[user].admin ? ' (Admin)' : '') + (response[user].servers.length > 0 ? ' - ' + response[user].servers.join(',') : '');
				select.appendChild(option);
			}
			if(document.getElementById('user_listing').innerHTML != select.innerHTML) {
				document.getElementById('user_listing').innerHTML = select.innerHTML;
				userSelect();
			}
		}
	});

	getServers(function(response) {
		servers = response;

		if(isVisible(document.getElementById('server_listing'))) {
			var select = document.createElement('select');
			for(var server in response) {
				var option = document.createElement('option');
				option.value = server;
				option.innerHTML = server + ' - ' + response[server].source + ' (r' + response[server].revision + ')';
				select.appendChild(option);
			}
			if(document.getElementById('server_listing').innerHTML != select.innerHTML) {
				document.getElementById('server_listing').innerHTML = select.innerHTML;
				serverSelect();
			}
		}

		if(isVisible(document.getElementById('user_create_servers'))) {
			var select = document.createElement('select');
			for(var server in response) {
				var option = document.createElement('option');
				option.value = server;
				option.innerHTML = server;
				select.appendChild(option);
			}
			if(document.getElementById('user_create_servers').innerHTML != select.innerHTML)
				document.getElementById('user_create_servers').innerHTML = select.innerHTML;
		}
	});

	getSources(function(response) {
		sources = response;

		if(isVisible(document.getElementById('source_listing'))) {
			var select = document.createElement('select');
			for(var source in response) {
				var option = document.createElement('option');
				option.value = source;
				option.innerHTML = source + ' - r' + response[source].revision;
				select.appendChild(option);
			}
			if(document.getElementById('source_listing').innerHTML != select.innerHTML) {
				document.getElementById('source_listing').innerHTML = select.innerHTML;
				sourceSelect();
			}
		}
	});

	getConfig(function(response) {
		if(config_text == response)
			return;
		config_text = response;
		if(isVisible(document.getElementById('config_editor')))
			config.setValue(config_text);
	});
}

function load() {
	config = CodeMirror(document.getElementById('config_editor'), {
		mode: 'settings',
		lineNumbers: true,
		lineWrapping: true,
		showTrailingSpace: true,
		theme: 'arma',
		placeholder: 'Here you can specify configuration global to every server.  Generally GLOBAL_ID and TALK_TO_MASTER are turned on here but you should also specify a SERVER_DNS.'
	});

	setInterval(refresh, 500);
}

window.addEventListener('load', load, false);
