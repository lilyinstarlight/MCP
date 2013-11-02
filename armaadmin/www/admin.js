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

function createUser(user, password, servers, admin) {
	ajaxPost('/admin/create/user', { 'user': user, 'password': password, 'servers': servers, 'admin': admin ? 'true' : 'false' }, function(ajax) {
		if(ajax.status != 200 || ajax.responseText != 'success')
			alert('Error creating user: ' + ajax.responseText);
	});
}

function destroyUser(user) {
	ajaxPost('/admin/destroy/user', { 'user': user }, function(ajax) {
		if(ajax.status != 200 || ajax.responseText != 'success')
			alert('Error destroying user: ' + ajax.responseText);
	});
}

function createServer(server, source) {
	ajaxPost('/admin/create/server', { 'server': server, 'source': source }, function(ajax) {
		if(ajax.status != 200 || ajax.responseText != 'success')
			alert('Error creating server: ' + ajax.responseText);
	});
}

function destroyServer(server) {
	ajaxPost('/admin/destroy/server', { 'server': server }, function(ajax) {
		if(ajax.status != 200 || ajax.responseText != 'success')
			alert('Error destroying server: ' + ajax.responseText);
	});
}

function upgradeServer(server) {
	ajaxPost('/admin/upgrade/server', { 'server': server }, function(ajax) {
		if(ajax.status != 200 || ajax.responseText != 'success')
			alert('Error upgrading server: ' + ajax.responseText);
	});
}

function upgradeServers() {
	ajaxGet('/admin/upgrade/servers', function(ajax) {
		if(ajax.status != 200 || ajax.responseText != 'success')
			alert('Error upgrading servers: ' + ajax.responseText);
	});
}

function addSource(source, bzr) {
	ajaxPost('/admin/add/source', { 'source': source, 'bzr': bzr }, function(ajax) {
		if(ajax.status != 200 || ajax.responseText != 'success')
			alert('Error adding source: ' + ajax.responseText);
	});
}

function removeSource(source) {
	ajaxPost('/admin/remove/source', { 'source': source }, function(ajax) {
		if(ajax.status != 200 || ajax.responseText != 'success')
			alert('Error removing source: ' + ajax.responseText);
	});
}

function updateSource(source) {
	ajaxPost('/admin/update/source', { 'source': source }, function(ajax) {
		if(ajax.status != 200 || ajax.responseText != 'success')
			alert('Error updating source: ' + ajax.responseText);
	});
}

function updateSources() {
	ajaxGet('/admin/update/sources', function(ajax) {
		if(ajax.status != 200 || ajax.responseText != 'success')
			alert('Error updating sources: ' + ajax.responseText);
	});
}

function getUsers() {
	if(document.getElementById('users').style.display == 'none' || document.getElementById('user_list').style.display == 'none')
		return;

	ajaxGet('/admin/get/users', function(ajax) {
		if(ajax.status == 200 && ajax.responseText != '')
			document.getElementById('user_listing').innerHTML = ajax.responseText;
	});
}

function getServers() {
	if(document.getElementById('servers').style.display == 'none' || document.getElementById('server_list').style.display == 'none')
		return;

	ajaxGet('/admin/get/servers', function(ajax) {
		if(ajax.status == 200 && ajax.responseText != '')
			document.getElementById('server_listing').innerHTML = ajax.responseText;
	});
}

function getSources() {
	if(document.getElementById('sources').style.display == 'none' || document.getElementById('source_list').style.display == 'none')
		return;

	ajaxGet('/admin/get/sources', function(ajax) {
		if(ajax.status == 200 && ajax.responseText != '')
			document.getElementById('source_listing').innerHTML = ajax.responseText;
	});
}

function getConfig() {
	if(document.getElementById('config').style.display == 'none' || config.hasFocus())
		return;

	ajaxGet('/admin/get/config', function(ajax) {
		if(ajax.status == 200 && ajax.responseText != '')
			config.setValue(ajax.responseText);
	});
}

function updateConfig() {
	ajaxPost('/admin/update/config', { 'config': config.getValue() }, function(ajax) {
		if(ajax.status != 200 || ajax.responseText != 'success')
			alert('Error updating config: ' + ajax.responseText);
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

	setInterval(getUsers, 500);
	setInterval(getServers, 500);
	setInterval(getSources, 500);
	setInterval(getConfig, 500);
}

window.addEventListener('load', load, false);
