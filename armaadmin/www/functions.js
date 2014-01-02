function getServers(handler) {
	get('/servers', function(request) {
		if(request.status == 200)
			handler(JSON.parse(request.responseText));
	});
}

function start(server, callback) {
	get('/server/' + server + '/start', function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error starting server: ' + request.responseText);
	});
}

function stop(server, callback) {
	get('/server/' + server + '/stop', function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error stopping server: ' + request.responseText);
	});
}

function reload(server, callback) {
	get('/server/' + server + '/reload', function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error reloading server: ' + request.responseText);
	});
}

function restart(server, callback) {
	get('/server/' + server + '/restart', function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error restarting server: ' + request.responseText);
	});
}

function sendCommand(server, command, callback) {
	post('/server/' + server + '/sendcommand', { 'command': command }, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error sending command "' + command + '": ' + request.responseText);
	});
}

function getStatus(server, handler) {
	get('/server/' + server + '/status', function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function getLog(server, handler) {
	get('/server/' + server + '/get/log', function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function getScriptLog(server, handler) {
	get('/server/' + server + '/get/scriptlog', function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function getSettings(server, handler) {
	get('/server/' + server + '/get/settings', function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function updateSettings(server, settings, callback) {
	post('/server/' + server + '/update/settings', { 'settings': settings }, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error updating settings: ' + request.responseText);
	});
}

function getScript(server, handler) {
	get('/server/' + server + '/get/script', function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function updateScript(server, script, callback) {
	post('/server/' + server + '/update/script', { 'script': script }, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error updating script: ' + request.responseText);
	});
}
