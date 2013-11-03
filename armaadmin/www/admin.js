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

function serverChange(element) {
	document.getElementById('server_list').style.display = 'none';
	document.getElementById('server_create').style.display = 'none';
	document.getElementById(element).style.display = 'block';
}

function sourceChange(element) {
	document.getElementById('source_list').style.display = 'none';
	document.getElementById('source_add').style.display = 'none';
	document.getElementById(element).style.display = 'block';
}

function submitUser() {
	var servers = "";
	createUser(document.getElementById('user_name').value, document.getElementById('user_password').value, servers, document.getElementById('user_admin').checked);
}

function submitServer() {
	createServer(document.getElementById('server_name').value, document.getElementById('server_source').value);
}

function submitSource() {
	addSource(document.getElementById('source_name').value, document.getElementById('source_bzr').value);
}

function refresh() {
	if(document.getElementById('users').style.display != 'none' && document.getElementById('user_list').style.display != 'none') {
		users = getUsers();

		var select = document.createElement('select');
		for(user in users) {
			var option = document.createElement('option');
			option.value = user;
			option.innerHTML = user + (users[user].admin ? ' (Admin) - ' : ' - ') + users[user].servers.join(',');
			select.appendChild(option);
		}
		document.getElementById('user_listing').innerHTML = select.innerHTML;
	}

	if(document.getElementById('servers').style.display != 'none' && document.getElementById('server_list').style.display != 'none') {
		servers = getServers();

		var select = document.createElement('select');
		for(server in servers) {
			var option = document.createElement('option');
			option.value = server;
			option.innerHTML = server + ' - ' + servers[server].source + ' (' + servers[server].revision + ')';
			select.appendChild(option);
		}
		document.getElementById('server_listing').innerHTML = select.innerHTML;
	}

	if(document.getElementById('sources').style.display != 'none' && document.getElementById('source_list').style.display != 'none') {
		sources = getSources();

		var select = document.createElement('select');
		for(source in sources) {
			var option = document.createElement('option');
			option.value = source;
			option.innerHTML = source + ' - ' + sources[source].revision;
			select.appendChild(option);
		}
		document.getElementById('source_listing').innerHTML = select.innerHTML;
	}

	if(document.getElementById('config').style.display != 'none' && !config.hasFocus()) {
		config_text = getConfig();
		if(config_text != '')
			config.setValue(config_text);
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
