var auth_token = 'Token ' + get_cookie();

function getFeatures(handler) {
	get('/api/features', auth_token, function(request) {
		if (request.status === 200)
			handler(JSON.parse(request.responseText));
	});
}

function getUsers(handler) {
	get('/api/user/', auth_token, function(request) {
		if (request.status === 200)
			handler(JSON.parse(request.responseText));
	});
}

function createUser(user, password, servers, admin, callback) {
	post('/api/user/', auth_token, {'user': user, 'password': password, 'servers': servers, 'admin': admin ? 'true' : 'false'}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error creating user: ' + request.responseText);
	});
}

function modifyUser(user, password, servers, admin, callback) {
	put('/api/user/' + user, auth_token, {'password': password, 'servers': servers, 'admin': admin ? 'true' : 'false'}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error modifying user: ' + request.responseText);
	});
}

function destroyUser(user, callback) {
	delete('/api/user/' + user, auth_token, function(request) {
		if (request.status === 204)
			typeof callback === 'function' && callback();
		else
			alert('Error destroying user: ' + request.responseText);
	});
}

function getServers(handler) {
	get('/api/server/', auth_token, function(request) {
		if (request.status === 200)
			handler(JSON.parse(request.responseText));
	});
}

function createServer(server, source, callback) {
	post('/api/server/', auth_token, {'server': server, 'source': source}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error creating server: ' + request.responseText);
	});
}

function upgradeServer(server, callback) {
	put('/api/server/' + server, auth_token, {'revision': null}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error upgrading server: ' + request.responseText);
	});
}

function destroyServer(server, callback) {
	delete('/api/server/' + server, auth_token, {}, function(request) {
		if (request.status === 204)
			typeof callback === 'function' && callback();
		else
			alert('Error destroying server: ' + request.responseText);
	});
}

function getSources(handler) {
	get('/api/source/', auth_token, function(request) {
		if (request.status === 200)
			handler(JSON.parse(request.responseText));
	});
}

function addSource(source, url, callback) {
	post('/api/source/', auth_token, {'source': source, 'url': url}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error adding source: ' + request.responseText);
	});
}

function updateSource(source, callback) {
	put('/api/source/' + source, auth_token, {}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error updating source: ' + request.responseText);
	});
}

function removeSource(source, callback) {
	delete('/api/source/' + source, auth_token, {}, function(request) {
		if (request.status === 204)
			typeof callback === 'function' && callback();
		else
			alert('Error removing source: ' + request.responseText);
	});
}

function getConfig(handler) {
	get('/api/config', auth_token, function(request) {
		if (request.status === 200)
			handler(request.responseText);
	});
}

function updateConfig(config, callback) {
	put('/api/config', auth_token, config, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error updating config: ' + request.responseText);
	});
}
