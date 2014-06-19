function submit() {
	login(document.getElementById('user'), document.getElementById('password'), function() {
		location.assign('/');
	});
}
