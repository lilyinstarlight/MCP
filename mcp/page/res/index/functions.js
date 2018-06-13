var username = getCookie()['username'];
var auth_token = 'Token ' + getCookie()['token'];

var check = function(handler) {
	XHR('/api/user/' + username, 'GET', auth_token, null, false, function(request) {
		if (request.status === 200)
			handler(true, JSON.parse(request.responseText)['admin']);
		else
			handler(false, false);
	});
};
