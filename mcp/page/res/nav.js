if (document.getElementById('server_button'))
    document.getElementById('server_button').addEventListener('click', function(evt) {
	goto('/server');

	evt.preventDefault();
    }, false);

if (document.getElementById('user_button'))
    document.getElementById('user_button').addEventListener('click', function(evt) {
	goto('/user');

	evt.preventDefault();
    }, false);

if (document.getElementById('admin_button'))
    document.getElementById('admin_button').addEventListener('click', function(evt) {
	goto('/admin');

	evt.preventDefault();
    }, false);

if (document.getElementById('logout_button'))
    document.getElementById('logout_button').addEventListener('click', function(evt) {
	unsetCookie();
	goto('/');

	evt.preventDefault();
    }, false);
