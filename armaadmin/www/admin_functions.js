function getUsers(handler) {
	textGet('/admin/get/users', function(request) {
		if(request.status == 200)
			handler(JSON.parse(request.responseText));
	});
}

function createUser(user, password, servers, admin) {
	textPost('/admin/create/user', { 'user': user, 'password': password, 'servers': servers, 'admin': admin ? 'true' : 'false' }, function(request) {
		if(request.status != 200)
			alert('Error creating user: ' + request.responseText);
	});
}

function changeUser(user, password, servers, admin) {
	textPost('/admin/create/user', { 'user': user, 'password': password, 'servers': servers, 'admin': admin ? 'true' : 'false' }, function(request) {
		if(request.status != 200)
			alert('Error changing user: ' + request.responseText);
	});
}

function destroyUser(user) {
	textPost('/admin/destroy/user', { 'user': user }, function(request) {
		if(request.status != 200)
			alert('Error destroying user: ' + request.responseText);
	});
}

function getServers(handler) {
	jsonGet('/admin/get/servers', function(request) {
		if(request.status == 200)
			handler(JSON.parse(request.responseText));
	});
}

function createServer(server, source) {
	textPost('/admin/create/server', { 'server': server, 'source': source }, function(request) {
		if(request.status != 200)
			alert('Error creating server: ' + request.responseText);
	});
}

function destroyServer(server) {
	textPost('/admin/destroy/server', { 'server': server }, function(request) {
		if(request.status != 200)
			alert('Error destroying server: ' + request.responseText);
	});
}

function upgradeServer(server) {
	textPost('/admin/upgrade/server', { 'server': server }, function(request) {
		if(request.status != 200)
			alert('Error upgrading server: ' + request.responseText);
	});
}

function upgradeServers() {
	textGet('/admin/upgrade/servers', function(request) {
		if(request.status != 200)
			alert('Error upgrading servers: ' + request.responseText);
	});
}

function getSources(handler) {
	jsonGet('/admin/get/sources', function(request) {
		if(request.status == 200)
			handler(JSON.parse(request.responseText));
	});
}

function addSource(source, bzr) {
	textPost('/admin/add/source', { 'source': source, 'bzr': bzr }, function(request) {
		if(request.status != 200)
			alert('Error adding source: ' + request.responseText);
	});
}

function removeSource(source) {
	textPost('/admin/remove/source', { 'source': source }, function(request) {
		if(request.status != 200)
			alert('Error removing source: ' + request.responseText);
	});
}

function updateSource(source) {
	textPost('/admin/update/source', { 'source': source }, function(request) {
		if(request.status != 200)
			alert('Error updating source: ' + request.responseText);
	});
}

function updateSources() {
	textGet('/admin/update/sources', function(request) {
		if(request.status != 200)
			alert('Error updating sources: ' + request.responseText);
	});
}

function getConfig(handler) {
	textGet('/admin/get/config', function(request) {
		if(request.status == 200)
			handler(request.responseText);
	});
}

function updateConfig() {
	textPost('/admin/update/config', { 'config': config.getValue() }, function(request) {
		if(request.status != 200)
			alert('Error updating config: ' + request.responseText);
	});
}
