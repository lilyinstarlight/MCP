var username = getCookie()['username']
var user;

var submitModifyUser = function() {
	modifyUser(username, document.getElementById('user_modify_password').value, document.getElementById('user_modify_key').value);
};

var refresh = function(force) {
	if (typeof force !== 'boolean')
		force = false;

	getUser(username, function(response) {
		user = response;

		if (force) {
			document.getElementById('user_modify_username').value = user.username;
			document.getElementById('user_modify_password').value = '';
			document.getElementById('user_modify_key').value = '';
		}

		document.getElementById('user_modify_admin').checked = user.admin;
		document.getElementById('user_modify_active').checked = user.active;

		var user_servers = user.servers;
		var select = document.createElement('select');
		for (var server in user_servers) {
			var option = document.createElement('option');
			option.value = server;
			option.innerHTML = server;
			option.setAttribute('selected', 'selected');
			select.appendChild(option);
		}
		document.getElementById('user_modify_servers').innerHTML = select.innerHTML;
	});

	setTimeout(refresh, 500);
};

var load = function() {
	document.getElementById('logout_button').addEventListener('click', function(evt) {
		unsetCookie();
		goto('/');

		evt.preventDefault();
	}, false);

	document.getElementById('user_modify_generate').addEventListener('click', function(evt) {
		document.getElementById('user_modify_form').elements['key'].value = generateKey();

		evt.preventDefault();
	}, false);

	document.getElementById('user_modify_form').addEventListener('submit', function(evt) {
		modifyUser(document.getElementById('user_modify_form').elements['username'].value, document.getElementById('user_modify_form').elements['password'].value, document.getElementById('user_modify_form').elements['key'].value);

		evt.preventDefault();
	}, false);

	check(function(admin) {
		if (admin)
			document.getElementById('admin_button').className = '';
	});

	refresh(true);
};

window.addEventListener('load', load, false);
