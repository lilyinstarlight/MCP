var count = 0;

function change(element, child) {
	var root = document.getElementById(element);
	for(var node in root.childNodes) {
		if(root.childNodes[node].nodeType == 1 && root.childNodes[node].tagName.toLowerCase() == 'div')
			root.childNodes[node].style.display = 'none';
	}
	document.getElementById(child).style.display = 'block';
}

function isVisible(element) {
	if(element == document)
		return true;

	if(element.style.display == 'none')
		return false;
	else
		return isVisible(element.parentNode);
}

function XHR(address, method, auth, data, handler) {
	var completed = false;
	var request = new XMLHttpRequest();
	request.onreadystatechange = function() {
		if(request.readyState == 4) {
			handler(request);

			completed = true;

			count--;
			working = document.getElementById('working');
			if(count == 0 && element != null)
				element.style.display = 'none';
		}
	};
	request.open(method, address, true);
	request.setRequestHeader('Authorization', auth);
	if(data != null) {
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
		if(!completed && working != null)
			working.style.display = 'inline-block';
	}, 500);
}

function get(address, auth, handler) {
	XHR(address, 'GET', auth, null, handler);
}

function post(address, auth, data, handler) {
	XHR(address, 'POST', auth, data, handler);
}

function put(address, auth, data, handler) {
	XHR(address, 'PUT', auth, data, handler);
}

function patch(address, auth, data, handler) {
	XHR(address, 'PATCH', auth, data, handler);
}

function delete(address, auth, handler) {
	XHR(address, 'DELETE', auth, null, handler);
}

function setLoginCookie(username, key) {
	document.cookie = JSON.stringify({ 'username': username, 'key': key });
}

function unsetLoginCookie() {
	document.cookie = '';
}

function getLoginCookie() {
	return JSON.parse(document.cookie);
}
