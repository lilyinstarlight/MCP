var config;

function change(element) {
	document.getElementById('users').style.display = 'none';
	document.getElementById('servers').style.display = 'none';
	document.getElementById('config').style.display = 'none';
	document.getElementById(element).style.display = 'block';
}

function userChange(element) {
	document.getElementById('user_list').style.display = 'none';
	document.getElementById('user_setup').style.display = 'none';
	document.getElementById(element).style.display = 'block';
}

function serverChange(element) {
	document.getElementById('server_list').style.display = 'none';
	document.getElementById('server_setup').style.display = 'none';
	document.getElementById(element).style.display = 'block';
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
	ajax.send('user=' + encodeURIComponent(user) + '&password=' + ecnodeURIComponent(password)  + '&servers=' + encodeURIComponent(servers) + '&admin=' + encodeURIComponent(admin));
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

function createServer(server) {
	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status != 200 || ajax.responseText != 'success')
				alert('Error creating server: ' + ajax.responseText);
		}
	}
	ajax.open('POST', '/admin/create/server', true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.send('server=' + encodeURIComponent(server));
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

function getUsers() {
	if(document.getElementById('users').style.display == 'none' || document.getElementById('user_list').style.display == 'none')
		return;

	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText != '')
				document.getElementById('user_list').innerHTML = ajax.responseText;
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
				document.getElementById('server_list').innerHTML = ajax.responseText;
		}
	}
	ajax.open('GET', '/admin/get/servers', true);
	ajax.send();
}

function getConfig() {
	if(document.getElementById('config').style.display == 'none')
		return;

	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4) {
			if(ajax.status == 200 && ajax.responseText != '')
				document.getElementById('config_text').innerHTML = ajax.responseText;
		}
	}
	ajax.open('GET', '/admin/get/config', true);
	ajax.send();
}

function load() {
	config = CodeMirror.fromTextArea(document.getElementById('config_text'), {
		mode: 'settings',
		lineNumbers: true,
		lineWrapping: true,
		showTrailingSpace: true,
		theme: 'arma',
	});

	setInterval(getUsers, 500);
	setInterval(getServers, 500);
	setInterval(getConfig, 500);
}

window.addEventListener('load', load, false);
