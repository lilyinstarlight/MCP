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
	var servers = ""
	createUser(document.getElementById('user_name').value, document.getElementById('user_password').value, servers, document.getElementById('user_admin').checked ? 'true' : 'false')
}

function submitServer() {
	createServer(document.getElementById('server_name').value, document.getElementById('server_source').value)
}

function submitSource() {
	addSource(document.getElementById('source_name').value, document.getElementById('source_bzr').value)
}

function createUser(user, password, servers, admin) {
	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status != 200 || ajax.responseText != 'success')
				alert('Error creating user: ' + ajax.responseText);
		}
	}
	ajax.open('POST', '/admin/create/user', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('user=' + encodeURIComponent(user) + '&password=' + encodeURIComponent(password)  + '&servers=' + encodeURIComponent(servers) + '&admin=' + encodeURIComponent(admin));
}

function destroyUser(user) {
	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status != 200 || ajax.responseText != 'success')
				alert('Error destroying user: ' + ajax.responseText);
		}
	}
	ajax.open('POST', '/admin/destroy/user', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('user=' + encodeURIComponent(user));
}

function createServer(server, source) {
	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status != 200 || ajax.responseText != 'success')
				alert('Error creating server: ' + ajax.responseText);
		}
	}
	ajax.open('POST', '/admin/create/server', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('server=' + encodeURIComponent(server) + '&source=' + encodeURIComponent(source));
}

function destroyServer(server) {
	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status != 200 || ajax.responseText != 'success')
				alert('Error destroying server: ' + ajax.responseText);
		}
	}
	ajax.open('POST', '/admin/destroy/server', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('server=' + encodeURIComponent(server));
}

function addSource(source, bzr) {
	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status != 200 || ajax.responseText != 'success')
				alert('Error adding source: ' + ajax.responseText);
		}
	}
	ajax.open('POST', '/admin/add/source', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('source=' + encodeURIComponent(source) + '&bzr=' + encodeURIComponent(bzr));
}

function removeSource(source) {
	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status != 200 || ajax.responseText != 'success')
				alert('Error removing source: ' + ajax.responseText);
		}
	}
	ajax.open('POST', '/admin/remove/source', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('source=' + encodeURIComponent(source));
}

function updateSource(source) {
	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status != 200 || ajax.responseText != 'success')
				alert('Error updating source: ' + ajax.responseText);
		}
	}
	ajax.open('POST', '/admin/update/source', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('source=' + encodeURIComponent(source));
}

function getUsers() {
	if(document.getElementById('users').style.display == 'none' || document.getElementById('user_list').style.display == 'none')
		return;

	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText != '')
				document.getElementById('user_listing').innerHTML = ajax.responseText;
		}
	}
	ajax.open('GET', '/admin/get/users', true);
	ajax.send();
}

function getServers() {
	if(document.getElementById('servers').style.display == 'none' || document.getElementById('server_list').style.display == 'none')
		return;

	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText != '')
				document.getElementById('server_listing').innerHTML = ajax.responseText;
		}
	}
	ajax.open('GET', '/admin/get/servers', true);
	ajax.send();
}

function getSources() {
	if(document.getElementById('sources').style.display == 'none' || document.getElementById('source_list').style.display == 'none')
		return;

	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText != '')
				document.getElementById('source_listing').innerHTML = ajax.responseText;
		}
	}
	ajax.open('GET', '/admin/get/sources', true);
	ajax.send();
}

function getConfig() {
	if(document.getElementById('config').style.display == 'none' || config.hasFocus())
		return;

	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText != '')
				config.setValue(ajax.responseText);
		}
	}
	ajax.open('GET', '/admin/get/config', true);
	ajax.send();
}

function updateConfig() {
	if(document.getElementById('config').style.display == 'none')
		return;

	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status != 200 || ajax.responseText != 'success')
				alert('Error updating config: ' + ajax.responseText);
		}
	}
	ajax.open('POST', '/admin/update/config', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('config=' + encodeURIComponent(config.getValue()));
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
