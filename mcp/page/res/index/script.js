var load = function(ev) {
	document.getElementById('server_button').addEventListener('click', function(evt) {
		goto('/server');

		evt.preventDefault();
	}, false);

	document.getElementById('user_button').addEventListener('click', function(evt) {
		goto('/user');

		evt.preventDefault();
	}, false);

	document.getElementById('admin_button').addEventListener('click', function(evt) {
		goto('/admin');

		evt.preventDefault();
	}, false);

	document.getElementById('logout_button').addEventListener('click', function(evt) {
		unsetCookie();
		goto('/');

		evt.preventDefault();
	}, false);

	document.getElementById('login_button').addEventListener('click', function(evt) {
		goto('/login');

		evt.preventDefault();
	}, false);

	check(function(logged, admin) {
		if (logged) {
			document.getElementById('server_button').className = '';
			document.getElementById('user_button').className = '';
			document.getElementById('logout_button').className = '';

			if (admin)
				document.getElementById('admin_button').className = '';
		}
		else {
			document.getElementById('login_button').className = '';
		}
	});
};

window.addEventListener('load', load, false);
