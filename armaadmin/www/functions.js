function start(callback) {
	textGet('/start', function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error starting server: ' + request.responseText);
	});
}

function stop() {
	textGet('/stop', function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error stopping server: ' + request.responseText);
	});
}

function reload() {
	textGet('/reload', function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error reloading server: ' + request.responseText);
	});
}

function restart() {
	textGet('/restart', function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error restarting server: ' + request.responseText);
	});
}

function sendCommand(command) {
	textPost('/sendcommand', { 'command': command }, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error sending command "' + command + '": ' + request.responseText);
	});
}

function getStatus(handler) {
	textGet('/status', function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function getLog(handler) {
	textGet('/get/log', function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function getScriptLog(handler) {
	textGet('/get/scriptlog', function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function getSettings(handler) {
	textGet('/get/settings', function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function getScript(handler) {
	textGet('/get/script', function(request) {
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
