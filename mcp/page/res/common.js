var goto = function(uri) {
	location.href = uri;
}

var change = function(element, child) {
	var root = document.getElementById(element);

	for (var node in root.childNodes) {
		if (root.childNodes[node].nodeType == 1 && root.childNodes[node].tagName.toLowerCase() == 'section')
			root.childNodes[node].style.display = 'none';
	}

	document.getElementById(child).style.display = 'block';
}

var is_visible = function(element) {
	if (element == document)
		return true;

	if (element.style.display == 'none')
		return false;
	else
		return is_visible(element.parentNode);
}

var set_cookie = function(username, key) {
	document.cookie = JSON.stringify({'username': username, 'key': key});
}

var unset_cookie = function() {
	document.cookie = '';
}

var get_cookie = function() {
	return JSON.parse(document.cookie);
}

var count = 0;
var XHR = function(address, method, auth, data, handler) {
	var completed = false;

	var request = new XMLHttpRequest();

	request.onreadystatechange = function() {
		if (request.readyState == 4) {
			if (request.status == 401)
				window.location.href = '/login';

			if (handler != null)
				handler(request);

			completed = true;

			count--;
			working = document.getElementById('working');
			if (count == 0 && working != null)
				working.style.display = 'none';
		}
	};

	request.open(method, address, true);

	request.setRequestHeader('Authorization', auth);

	if (data != null) {
		json = JSON.stringify(data);
		request.setRequestHeader('Content-Type', 'application/json');
		request.setRequestHeader('Content-Length', json.length);

		request.send(json);
	}
	else {
		request.send();
	}

	count++;
	setTimeout(function() {
		working = document.getElementById('working');
		if (!completed && working != null)
			working.style.display = 'inline-block';
	}, 500);
}

var get = function(address, auth, handler) {
	XHR(address, 'GET', auth, null, handler);
}

var post = function(address, auth, data, handler) {
	XHR(address, 'POST', auth, data, handler);
}

var put = function(address, auth, data, handler) {
	XHR(address, 'PUT', auth, data, handler);
}

var patch = function(address, auth, data, handler) {
	XHR(address, 'PATCH', auth, data, handler);
}

var delete = function(address, auth, handler) {
	XHR(address, 'DELETE', auth, null, handler);
}
