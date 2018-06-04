var auth_token = 'Token ' + get_cookie().split(':')[0];

function getServers(handler) {
	get('/api/server/', auth_token, function(request) {
		if (request.status === 200)
			handler(JSON.parse(request.responseText));
	});
}

function start(server, callback) {
	put('/api/server/' + server, auth_token, {'running': true}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error starting server: ' + request.responseText);
	});
}

function stop(server, callback) {
	put('/api/server/' + server, auth_token, {'running': false}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error stopping server: ' + request.responseText);
	});
}

function restart(server, callback) {
	put('/api/server/' + server, auth_token, {'running': true}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error restarting server: ' + request.responseText);
	});
}

function sendCommand(server, command, callback) {
	post('/api/server/' + server, auth_token, {'command': command}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error sending command "' + command + '": ' + request.responseText);
	});
}

function reload(server, callback) {
	sendCommand(server, 'INCLUDE settings.cfg', function() {
		sendCommand(server, 'INCLUDE server_info.cfg', function() {
			sendCommand(server, 'INCLUDE settings_custom.cfg', function() {
				typeof callback === 'function' && callback();
			});
		});
	});
}

function getStatus(server, handler) {
	get('/api/server/' + server, auth_token, function(request) {
		if (request.status === 200)
			handler(JSON.parse(request.responseText));
	});
}

function getLog(server, handler) {
	get('/api/server/' + server + '/log', auth_token, function(request) {
		if (request.status === 200)
			handler(request.responseText);
	});
}

function getScriptLog(server, handler) {
	get('/api/server/' + server + '/script/log', auth_token, function(request) {
		if (request.status === 200)
			handler(request.responseText);
	});
}

function getSettings(server, handler) {
	get('/api/server/' + server + '/settings', auth_token, function(request) {
		if (request.status === 200)
			handler(request.responseText);
	});
}

function updateSettings(server, settings, callback) {
	post('/api/server/' + server + '/settings', auth_token, {'settings': settings}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error updating settings: ' + request.responseText);
	});
}

function getScript(server, handler) {
	get('/api/server/' + server + '/script', auth_token, function(request) {
		if (request.status === 200)
			handler(request.responseText);
	});
}

function updateScript(server, script, callback) {
	post('/api/server/' + server + '/script', auth_token, {'script': script}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error updating script: ' + request.responseText);
	});
}
