var username = get_cookie().split(':')[1]
var user;

var submitModifyUser = function() {
	modifyUser(username, document.getElementById('user_modify_password').value, document.getElementById('user_modify_key').value);
}

var refresh = function(force) {
	if (typeof force !== 'boolean')
		force = false;

	getUser(username, function(response) {
		user = response;

		if (force) {
			document.getElementById('user_modify_name').value = user.username;
			document.getElementById('user_modify_password').value = '';
			document.getElementById('user_modify_key').value = user.key;
		}

		document.getElementById('user_modify_admin').value = user.key;
		document.getElementById('user_modify_active').value = user.key;

		var user_servers = users[selected[0]].servers;
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
}

var load = function() {
	refresh(true);
}

window.addEventListener('load', load, false);
