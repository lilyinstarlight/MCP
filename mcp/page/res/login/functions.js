var login = function(username, password, callback) {
	auth = 'Basic ' + btoa(username + ':' + password);

	post('/users/' + username, {}, auth, function(request) {
		if (request.status == 200) {
			user = JSON.parse(request.responseText);
			set_cookie(username, user.username + ':' + user.token);

			typeof callback == 'function' && callback();
		}
		else if (request.status == 401)
			alert('Incorrect username or password');
		else
			alert('Error logging in');
	});
}

var logout = function(callback) {
	unset_cookie();

	typeof callback == 'function' && callback();
}
