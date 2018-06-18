var login = function(username, password, callback) {
	auth = 'Login ' + btoa(username + ':' + password);

	XHR('/api/user/' + username, 'POST', auth, {}, false, function(request) {
		if (request.status === 200) {
			user = JSON.parse(request.responseText);
			setCookie(username, user['token']);

			typeof callback === 'function' && callback(request);
		}
		else
		    typeof callback === 'function' && callback(request);
	});
};
