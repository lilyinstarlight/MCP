var username = getCookie()['username'];
var auth_token = 'Token ' + getCookie()['token'];

var check = function(handler) {
	get('/api/user/' + username, auth_token, function(request) {
		handler(JSON.parse(request.responseText)['admin']);
	});
};

var getUser = function(user, handler) {
	get('/api/user/' + user, auth_token, function(request) {
		if (request.status === 200)
			handler(JSON.parse(request.responseText));
	});
};

var modifyUser = function(user, password, key, callback) {
	put('/api/user/' + user, auth_token, {'password': password, 'key': key}, 'application/json', function(request) {
		if (request.status === 200)
			typeof callback === 'function' && callback();
		else
			alert('Error modifying user: ' + request.responseText);
	});
};

var generateKey = function() {
	var chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';

	var key = '';
	for (var i = 0; i < 24; i++)
		key += chars[Math.floor(Math.random()*chars.length)];

	return key;
};
