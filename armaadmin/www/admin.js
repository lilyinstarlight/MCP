var users, servers, sources;
var config;

function change(element) {
	document.getElementById('users').style.display = 'none';
	document.getElementById('servers').style.display = 'none';
	document.getElementById('sources').style.display = 'none';
	document.getElementById('config').style.display = 'none';
	document.getElementById(element).style.display = 'block';
}

function userChange(element) {
	document.getElementById('user_list').style.display = 'none';
	document.getElementById('user_create').style.display = 'none';
	document.getElementById(element).style.display = 'block';
}

function userSelect() {
}

function submitUser() {
	var servers = [];
	var options = document.getElementById('user_servers').options;
	for(var option in options) {
		if(options[option].selected)
			servers.append(options[option].value)
	}
	createUser(document.getElementById('user_name').value, document.getElementById('user_password').value, servers.join(','), document.getElementById('user_admin').checked);
}

function modifyUser() {
	var servers = [];
	var options = document.getElementById('user_change_servers').options;
	for(var option in options) {
		if(options[option].selected)
			servers.append(options[option].value)
	}
	changeUser(document.getElementById('user_change_name').value, document.getElementById('user_change_password').value, servers.join(','), document.getElementById('user_change_admin').checked);
}

function serverChange(element) {
	document.getElementById('server_list').style.display = 'none';
	document.getElementById('server_create').style.display = 'none';
	document.getElementById(element).style.display = 'block';
}

function serverSelect() {
}

function submitServer() {
	createServer(document.getElementById('server_name').value, document.getElementById('server_source').value);
}

function sourceChange(element) {
	document.getElementById('source_list').style.display = 'none';
	document.getElementById('source_add').style.display = 'none';
	document.getElementById(element).style.display = 'block';
}

function sourceSelect() {
}

function submitSource() {
	addSource(document.getElementById('source_name').value, document.getElementById('source_bzr').value);
}

function refresh() {
	if(document.getElementById('users').style.display != 'none' && document.getElementById('user_list').style.display != 'none') {
		getUsers(function(response) {
			users = response;
			var select = document.createElement('select');
			for(var user in response) {
				var option = document.createElement('option');
				option.value = user;
				option.innerHTML = user + (response[user].admin ? ' (Admin) - ' : ' - ') + response[user].servers.join(',');
				select.appendChild(option);
			}
			if(document.getElementById('user_listing').innerHTML != select.innerHTML)
				document.getElementById('user_listing').innerHTML = select.innerHTML;
		});
	}

	if(document.getElementById('servers').style.display != 'none' && document.getElementById('server_list').style.display != 'none') {
		getServers(function(response) {
			if(servers == response)
				return;
			servers = response;
			var select = document.createElement('select');
			for(var server in response) {
				var option = document.createElement('option');
				option.value = server;
				option.innerHTML = server + ' - ' + response[server].source + ' (' + response[server].revision + ')';
				select.appendChild(option);
			}
			if(document.getElementById('server_listing').innerHTML != select.innerHTML)
				document.getElementById('server_listing').innerHTML = select.innerHTML;
		});
	}

	if(document.getElementById('sources').style.display != 'none' && document.getElementById('source_list').style.display != 'none') {
		getSources(function(response) {
			if(sources == response)
				return;
			sources = response;
			var select = document.createElement('select');
			for(var source in response) {
				var option = document.createElement('option');
				option.value = source;
				option.innerHTML = source + ' - r' + response[source].revision;
				select.appendChild(option);
			}
			if(document.getElementById('source_listing').innerHTML != select.innerHTML)
				document.getElementById('source_listing').innerHTML = select.innerHTML;
		});
	}

	if(document.getElementById('config').style.display != 'none') {
		getConfig(function(response) {
			if(config.getValue() == response)
				return;
			config.setValue(response);
		});
	}
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
