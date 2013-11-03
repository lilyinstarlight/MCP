function createUser(user, password, servers, admin) {
	var request = sjaxPost('/admin/create/user', { 'user': user, 'password': password, 'servers': servers, 'admin': admin ? 'true' : 'false' });
	if(request.status != 200)
		alert('Error creating user: ' + request.responseText);
}

function destroyUser(user) {
	var request = sjaxPost('/admin/destroy/user', { 'user': user });
	if(request.status != 200)
		alert('Error destroying user: ' + request.responseText);
}

function createServer(server, source) {
	var request = sjaxPost('/admin/create/server', { 'server': server, 'source': source });
	if(request.status != 200)
		alert('Error creating server: ' + request.responseText);
}

function destroyServer(server) {
	var request = sjaxPost('/admin/destroy/server', { 'server': server });
	if(request.status != 200)
		alert('Error destroying server: ' + request.responseText);
}

function upgradeServer(server) {
	var request = sjaxPost('/admin/upgrade/server', { 'server': server });
	if(request.status != 200)
		alert('Error upgrading server: ' + request.responseText);
}

function upgradeServers() {
	var request = sjaxGet('/admin/upgrade/servers');
	if(request.status != 200)
		alert('Error upgrading servers: ' + request.responseText);
}

function addSource(source, bzr) {
	var request = sjaxPost('/admin/add/source', { 'source': source, 'bzr': bzr });
	if(request.status != 200)
		alert('Error adding source: ' + request.responseText);
}

function removeSource(source) {
	var request = sjaxPost('/admin/remove/source', { 'source': source });
	if(request.status != 200)
		alert('Error removing source: ' + request.responseText);
}

function updateSource(source) {
	var request = sjaxPost('/admin/update/source', { 'source': source });
	if(request.status != 200)
		alert('Error updating source: ' + request.responseText);
}

function updateSources() {
	var request = sjaxGet('/admin/update/sources');
	if(request.status != 200)
		alert('Error updating sources: ' + request.responseText);
}

function getUsers() {
	var request = sjaxGet('/admin/get/users', 'ajax');
	if(request.status == 200)
		return request.response;
	else
		return '';
}

function getServers() {
	var request = sjaxGet('/admin/get/servers', 'ajax');
	if(request.status == 200)
		return request.response;
	else
		return '';
}

function getSources() {
	var request = sjaxGet('/admin/get/sources', 'ajax');
	if(request.status == 200)
		return request.response;
	else
		return '';
}

function getConfig() {
	var request = sjaxGet('/admin/get/config', 'ajax');
	if(request.status == 200)
		return request.response;
	else
		return '';
}

function updateConfig() {
	var request = sjaxPost('/admin/update/config', { 'config': config.getValue() });
	if(request.status != 200 || request.responseText != 'success')
		alert('Error updating config: ' + request.responseText);
}


