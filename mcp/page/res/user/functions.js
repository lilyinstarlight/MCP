var auth_token = 'Token ' + get_cookie().split(':')[0];

var getUser = function(user, password, key, handler) {
	get('/api/user/' + user, auth_token, function(request) {
		if (request.status === 200)
			handler(JSON.parse(request.responseText));
	});
}

var modifyUser = function(user, password, key, callback) {
	put('/api/user/' + user, auth_token, {'password': password, 'key': key}, function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error modifying user: ' + request.responseText);
	});
}
