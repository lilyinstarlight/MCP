function start() {
	var request = sjaxGet('/start');
	if(request.status != 200)
		alert('Error starting server: ' + request.responseText);
}

function stop() {
	var request = sjaxGet('/stop');
	if(request.status != 200)
		alert('Error stopping server: ' + request.responseText);
}

function reload() {
	var request = sjaxGet('/reload');
	if(request.status != 200)
		alert('Error reloading server: ' + request.responseText);
}

function restart() {
	var request = sjaxGet('/restart');
	if(request.status != 200)
		alert('Error restarting server: ' + request.responseText);
}

function sendCommand(command) {
	var request = sjaxPost('/sendcommand', { 'command': command });
	if(request.status != 200)
		alert('Error sending command "' + command + '": ' + request.responseText);
}

function getStatus() {
	var request = sjaxGet('/status');
	if(ajax.status == 200)
		return request.responseText;
	else
		return '';
}

function getLog() {
	var request = sjaxGet('/get/log');
	if(ajax.status == 200)
		return request.responseText;
	else
		return '';
}

function getScriptLog() {
	var request = sjaxGet('/get/scriptlog');
	if(ajax.status == 200)
		return request.responseText;
	else
		return '';
}

function getSettings() {
	var request = sjaxGet('/get/settings');
	if(ajax.status == 200)
		return request.responseText;
	else
		return '';
}

function getScript() {
	var request = sjaxGet('/get/script');
	if(ajax.status == 200)
		return request.responseText;
	else
		return '';
}

function updateSettings() {
	var request = sjaxPost('/update/settings', { 'settings': settings.getValue() });
	if(request.status != 200)
		alert('Error updating settings: ' + request.responseText);
}

function updateScript() {
	var request = sjaxPost('/update/script', { 'script': script.getValue() });
	if(request.status != 200)
		alert('Error updating script: ' + request.responseText);
}


