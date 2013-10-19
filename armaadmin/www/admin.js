function change(element) {
	document.getElementById('users').style.display = 'none';
	document.getElementById('servers').style.display = 'none';
	document.getElementById('config').style.display = 'none';
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

function load() {
	;
}

window.addEventListener('load', load, false);
