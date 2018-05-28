function getFeatures(handler) {
	get('/api/features', function(request) {
		if (request.status == 200)
			handler(JSON.parse(request.responseText));
	});
}

function getUsers(handler) {
	get('/api/user/', function(request) {
		if (request.status == 200)
			handler(JSON.parse(request.responseText));
	});
}

function createUser(user, password, servers, admin, callback) {
	post('/api/user/', {'user': user, 'password': password, 'servers': servers, 'admin': admin ? 'true' : 'false'}, function(request) {
		if (request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error creating user: ' + request.responseText);
	});
}

function modifyUser(user, password, servers, admin, callback) {
	put('/api/user/' + user, {'password': password, 'servers': servers, 'admin': admin ? 'true' : 'false'}, function(request) {
		if (request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error modifying user: ' + request.responseText);
	});
}

function destroyUser(user, callback) {
	delete('/api/user/' + user, function(request) {
		if (request.status == 204)
			typeof callback == 'function' && callback();
		else
			alert('Error destroying user: ' + request.responseText);
	});
}

function getServers(handler) {
	get('/api/server/', function(request) {
		if (request.status == 200)
			handler(JSON.parse(request.responseText));
	});
}

function createServer(server, source, callback) {
	post('/api/server/', {'server': server, 'source': source}, function(request) {
		if (request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error creating server: ' + request.responseText);
	});
}

function upgradeServer(server, callback) {
	put('/api/server/' + server, {'revision': null}, function(request) {
		if (request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error upgrading server: ' + request.responseText);
	});
}

function destroyServer(server, callback) {
	delete('/api/server/' + server, {}, function(request) {
		if (request.status == 204)
			typeof callback == 'function' && callback();
		else
			alert('Error destroying server: ' + request.responseText);
	});
}

function getSources(handler) {
	get('/api/source/', function(request) {
		if (request.status == 200)
			handler(JSON.parse(request.responseText));
	});
}

function addSource(source, url, callback) {
	post('/api/source/', {'source': source, 'url': url}, function(request) {
		if (request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error adding source: ' + request.responseText);
	});
}

function updateSource(source, callback) {
	put('/api/source/' + source, {}, function(request) {
		if (request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error updating source: ' + request.responseText);
	});
}

function removeSource(source, callback) {
	delete('/api/source/' + source, {}, function(request) {
		if (request.status == 204)
			typeof callback == 'function' && callback();
		else
			alert('Error removing source: ' + request.responseText);
	});
}

function getConfig(handler) {
	get('/api/config', function(request) {
		if (request.status == 200)
			handler(request.responseText);
	});
}

function updateConfig(config, callback) {
	put('/api/config', config, function(request) {
		if (request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error updating config: ' + request.responseText);
	});
}
