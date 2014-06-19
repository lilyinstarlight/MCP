function login(username, password, callback) {
	auth = 'Basic ' + btoa(username + ':' + password);

	get('/users/' + username, auth, function(request) {
		if(request.status == 200) {
			user = JSON.parse(request.responseText);
			setLoginCookie(username, user.key);
			typeof callback == 'function' && callback();
		}
		else if(request.status == 401)
			alert('Incorrect username or password');
		else
			alert('Error logging in');
	});
}
