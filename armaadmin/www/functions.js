function start(callback) {
	get('/start', function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error starting server: ' + request.responseText);
	});
}

function stop() {
	get('/stop', function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error stopping server: ' + request.responseText);
	});
}

function reload() {
	get('/reload', function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error reloading server: ' + request.responseText);
	});
}

function restart() {
	get('/restart', function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error restarting server: ' + request.responseText);
	});
}

function sendCommand(command) {
	post('/sendcommand', { 'command': command }, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error sending command "' + command + '": ' + request.responseText);
	});
}

function getStatus(handler) {
	get('/status', function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function getLog(handler) {
	get('/get/log', function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function getScriptLog(handler) {
	get('/get/scriptlog', function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function getSettings(handler) {
	get('/get/settings', function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function getScript(handler) {
	get('/get/script', function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function updateSettings() {
	textPost('/update/settings', { 'settings': settings.getValue() }, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error updating settings: ' + request.responseText);
	});
}

function updateScript() {
	textPost('/update/script', { 'script': script.getValue() }, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error updating script: ' + request.responseText);
	});
}
