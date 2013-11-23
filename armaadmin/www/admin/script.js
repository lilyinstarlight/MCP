var users, servers, sources;
var config, config_text;

function userSelect() {
}

function submitUser() {
	var servers = [];
	var options = document.getElementById('user_servers').options;
	for(var option in options) {
		if(options[option].selected)
			servers.push(options[option].value);
	}
	createUser(document.getElementById('user_name').value, document.getElementById('user_password').value, servers.join(','), document.getElementById('user_admin').checked);
}

function submitModifyUser() {
	var servers = [];
	var options = document.getElementById('user_modfy_servers').options;
	for(var option in options) {
		if(options[option].selected)
			servers.push(options[option].value);
	}
	modifyUser(document.getElementById('user_modfy_name').value, document.getElementById('user_modfy_password').value, servers.join(','), document.getElementById('user_modfy_admin').checked);
}

function serverSelect() {
}

function submitServer() {
	createServer(document.getElementById('server_name').value, document.getElementById('server_source').value);
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
			servers = response;
			var select = document.createElement('select');
			for(var server in response) {
				var option = document.createElement('option');
				option.value = server;
				option.innerHTML = server + ' - ' + response[server].source + ' (r' + response[server].revision + ')';
				select.appendChild(option);
			}
			if(document.getElementById('server_listing').innerHTML != select.innerHTML)
				document.getElementById('server_listing').innerHTML = select.innerHTML;
		});
	}

	if(document.getElementById('sources').style.display != 'none' && document.getElementById('source_list').style.display != 'none') {
		getSources(function(response) {
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
			if(config_text == response)
				return;
			config_text = response;
			config.setValue(config_text);
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
