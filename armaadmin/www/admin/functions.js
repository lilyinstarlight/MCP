function getUsers(handler) {
	get('/admin/get/users', function(request) {
		if(request.status == 200)
			handler(JSON.parse(request.responseText));
	});
}

function createUser(user, password, servers, admin, callback) {
	post('/admin/create/user', { 'user': user, 'password': password, 'servers': servers, 'admin': admin ? 'true' : 'false' }, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error creating user: ' + request.responseText);
	});
}

function modifyUser(user, password, servers, admin, callback) {
	post('/admin/modify/user', { 'user': user, 'password': password, 'servers': servers, 'admin': admin ? 'true' : 'false' }, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error modifying user: ' + request.responseText);
	});
}

function destroyUser(user, callback) {
	post('/admin/destroy/user', { 'user': user }, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error destroying user: ' + request.responseText);
	});
}

function getServers(handler) {
	get('/admin/get/servers', function(request) {
		if(request.status == 200)
			handler(JSON.parse(request.responseText));
	});
}

function createServer(server, source, callback) {
	post('/admin/create/server', { 'server': server, 'source': source }, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error creating server: ' + request.responseText);
	});
}

function upgradeServer(server, callback) {
	post('/admin/upgrade/server', { 'server': server }, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error upgrading server: ' + request.responseText);
	});
}

function destroyServer(server, callback) {
	post('/admin/destroy/server', { 'server': server }, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error destroying server: ' + request.responseText);
	});
}

function upgradeServers(callback) {
	get('/admin/upgrade/servers', function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error upgrading servers: ' + request.responseText);
	});
}

function getSources(handler) {
	get('/admin/get/sources', function(request) {
		if(request.status == 200)
			handler(JSON.parse(request.responseText));
	});
}

function addSource(source, bzr, callback) {
	post('/admin/add/source', { 'source': source, 'bzr': bzr }, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error adding source: ' + request.responseText);
	});
}

function updateSource(source, callback) {
	post('/admin/update/source', { 'source': source }, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error updating source: ' + request.responseText);
	});
}

function removeSource(source, callback) {
	post('/admin/remove/source', { 'source': source }, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error removing source: ' + request.responseText);
	});
}

function updateSources(callback) {
	get('/admin/update/sources', function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error updating sources: ' + request.responseText);
	});
}

function getConfig(handler) {
	get('/admin/get/config', function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function updateConfig(callback) {
	post('/admin/update/config', { 'config': config.getValue() }, function(request) {
		if(request.status == 200)
			typeof callback == 'function' && callback();
		else
			alert('Error updating config: ' + request.responseText);
	});
}
