var auth_token = 'Token ' + get_cookie().split(':')[0];

var getFeatures = function(handler) {
	get('/api/features', auth_token, function(request) {
		if (request.status === 200)
			handler(JSON.parse(request.responseText));
	});
};

var getUsers = function(handler) {
	get('/api/user/', auth_token, function(request) {
		if (request.status === 200)
			handler(JSON.parse(request.responseText));
	});
};

var createUser = function(user, password, key, servers, admin, active, callback) {
	post('/api/user/', auth_token, {'user': user, 'key': key, 'password': password, 'servers': servers, 'admin': admin ? 'true' : 'false', 'active': active ? 'true' : 'false'}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error creating user: ' + request.responseText);
	});
};

var modifyUser = function(user, password, key, servers, admin, active, callback) {
	put('/api/user/' + user, auth_token, {'password': password, 'key': key, 'servers': servers, 'admin': admin ? 'true' : 'false', 'active': active ? 'true' : 'false'}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error modifying user: ' + request.responseText);
	});
};

var destroyUser = function(user, callback) {
	del('/api/user/' + user, auth_token, function(request) {
		if (request.status === 204)
			typeof callback === 'function' && callback();
		else
			alert('Error destroying user: ' + request.responseText);
	});
};

var getServers = function(handler) {
	get('/api/server/', auth_token, function(request) {
		if (request.status === 200)
			handler(JSON.parse(request.responseText));
	});
};

var createServer = function(server, source, callback) {
	post('/api/server/', auth_token, {'server': server, 'source': source}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error creating server: ' + request.responseText);
	});
};

var upgradeServer = function(server, callback) {
	put('/api/server/' + server, auth_token, {'revision': null}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error upgrading server: ' + request.responseText);
	});
};

var destroyServer = function(server, callback) {
	del('/api/server/' + server, auth_token, {}, function(request) {
		if (request.status === 204)
			typeof callback === 'function' && callback();
		else
			alert('Error destroying server: ' + request.responseText);
	});
};

var getSources = function(handler) {
	get('/api/source/', auth_token, function(request) {
		if (request.status === 200)
			handler(JSON.parse(request.responseText));
	});
};

var addSource = function(source, url, callback) {
	post('/api/source/', auth_token, {'source': source, 'url': url}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error adding source: ' + request.responseText);
	});
};

var updateSource = function(source, callback) {
	put('/api/source/' + source, auth_token, {}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error updating source: ' + request.responseText);
	});
};

var removeSource = function(source, callback) {
	del('/api/source/' + source, auth_token, {}, function(request) {
		if (request.status === 204)
			typeof callback === 'function' && callback();
		else
			alert('Error removing source: ' + request.responseText);
	});
};

var getConfig = function(handler) {
	get('/api/config', auth_token, function(request) {
		if (request.status === 200)
			handler(request.responseText);
	});
};

var updateConfig = function(config, callback) {
	put('/api/config', auth_token, config, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error updating config: ' + request.responseText);
	});
};
