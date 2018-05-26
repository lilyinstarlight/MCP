function getServers(handler) {
	get('/server/', auth_key, function(request) {
		if(request.status == 200)
			handler(JSON.parse(request.responseText));
	});
}

function start(server, callback) {
	put('/server/' + server, auth_key, {'running': true}, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error starting server: ' + request.responseText);
	});
}

function stop(server, callback) {
	put('/server/' + server, auth_key, {'running': false}, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error stopping server: ' + request.responseText);
	});
}

function restart(server, callback) {
	put('/server/' + server, auth_key, {'running': true}, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error restarting server: ' + request.responseText);
	});
}

function sendCommand(server, command, callback) {
	post('/server/' + server, auth_key, {'command': command}, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error sending command "' + command + '": ' + request.responseText);
	});
}

function reload(server, callback) {
	sendCommand(server, 'INCLUDE settings.cfg', function() {
		sendCommand(server, 'INCLUDE server_info.cfg', function() {
			sendCommand(server, 'INCLUDE settings_custom.cfg', function() {
				typeof callback == 'function' && callback();
			});
		});
	});
}

function getStatus(server, handler) {
	get('/server/' + server, auth_key, function(request) {
		if(request.status == 200)
			handler(JSON.parse(request.responseText));
	});
}

function getLog(server, handler) {
	get('/server/' + server + '/log', auth_key, function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function getScriptLog(server, handler) {
	get('/server/' + server + '/script/log', auth_key, function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function getSettings(server, handler) {
	get('/server/' + server + '/settings', auth_key, function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function updateSettings(server, settings, callback) {
	post('/server/' + server + '/settings', auth_key, {'settings': settings}, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error updating settings: ' + request.responseText);
	});
}

function getScript(server, handler) {
	get('/server/' + server + '/script', auth_key, function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function updateScript(server, script, callback) {
	post('/server/' + server + '/script', auth_key, {'script': script}, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error updating script: ' + request.responseText);
	});
}
