var login = function(username, password, callback) {
	auth = 'Basic ' + btoa(username + ':' + password);

	post('/api/user/' + username, auth, {}, function(request) {
		if (request.status == 200) {
			user = JSON.parse(request.responseText);
			setCookie(username, user['token']);

			typeof callback == 'function' && callback();
		}
		else if (request.status == 401)
			alert('Incorrect username or password');
		else
			alert('Error logging in');
	});
};
