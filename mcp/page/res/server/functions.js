var username = getCookie()['username'];
var auth_token = 'Token ' + getCookie()['token'];

var check = function(handler) {
	get('/api/user/' + username, auth_token, function(request) {
		handler(JSON.parse(request.responseText)['admin']);
	});
};

var getServers = function(handler) {
	get('/api/server/', auth_token, function(request) {
		if (request.status === 200)
			handler(JSON.parse(request.responseText));
	});
};

var start = function(server, callback) {
	put('/api/server/' + server, auth_token, {'running': true}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error starting server: ' + request.responseText);
	});
};

var stop = function(server, callback) {
	put('/api/server/' + server, auth_token, {'running': false}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error stopping server: ' + request.responseText);
	});
};

var restart = function(server, callback) {
	put('/api/server/' + server, auth_token, {'running': true}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error restarting server: ' + request.responseText);
	});
};

var sendCommand = function(server, command, callback) {
	post('/api/server/' + server, auth_token, {'command': command}, function(request) {
		if (request.status === 204)
			typeof callback === 'function' && callback();
		else
			alert('Error sending command "' + command + '": ' + request.responseText);
	});
};

var reload = function(server, callback) {
	sendCommand(server, 'INCLUDE settings.cfg', function() {
		sendCommand(server, 'INCLUDE server_info.cfg', function() {
			sendCommand(server, 'INCLUDE settings_custom.cfg', function() {
				typeof callback === 'function' && callback();
			});
		});
	});
};

var getStatus = function(server, handler) {
	get('/api/server/' + server, auth_token, function(request) {
		if (request.status === 200)
			handler(JSON.parse(request.responseText));
	});
};

var getLog = function(server, last, handler) {
	get('/api/server/' + server + '/log?last=' + last, auth_token, function(request) {
		if (request.status === 200) {
			var log = request.responseText.split('\n');
			handler(log.slice(-300).join('\n'), last + log.length - 1);
		}
		else if (request.status === 204)
			handler(request.responseText, last);
		else if (request.status === 201)
			handler(request.responseText, 0);
	});
};

var getScriptLog = function(server, last, handler) {
	get('/api/server/' + server + '/script/log?last=' + last, auth_token, function(request) {
		if (request.status === 200)
			handler(request.responseText, last + request.responseText.split('\n').length - 1);
		else if (request.status === 204)
			handler(request.responseText, last);
		else if (request.status === 201)
			handler(request.responseText, 0);
	});
};

var getSettings = function(server, handler) {
	get('/api/server/' + server + '/settings', auth_token, function(request) {
		if (request.status === 200)
			handler(request.responseText);
	});
};

var updateSettings = function(server, settings, callback) {
	put('/api/server/' + server + '/settings', auth_token, {'settings': settings}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error updating settings: ' + request.responseText);
	});
};

var getScript = function(server, handler) {
	get('/api/server/' + server + '/script', auth_token, function(request) {
		if (request.status === 200)
			handler(request.responseText);
	});
};

function updateScript(server, script, callback) {
	put('/api/server/' + server + '/script', auth_token, {'script': script}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error updating script: ' + request.responseText);
	});
};
