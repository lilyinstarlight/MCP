var goto = function(uri, open) {
    if (open)
	window.open(uri, '_blank');
    else
	window.location.href = uri;
};

var change = function(element, child) {
    if (typeof child === 'undefined') {
	var root = document.getElementById(element).parentNode;
	var child = element;
    }
    else {
	var root = document.getElementById(element);
    }

    for (var node in root.childNodes) {
	if (root.childNodes[node].nodeType === 1 && root.childNodes[node].tagName.toLowerCase() === 'section')
	    root.childNodes[node].style.display = 'none';
    }

    document.getElementById(child).style.display = 'block';
};

var isVisible = function(element) {
    if (element === document)
	return true;

    if (window.getComputedStyle(element, null).getPropertyValue('display') === 'none')
	return false;
    else
	return isVisible(element.parentNode);
};

var setCookie = function(username, token) {
    var date = new Date();
    date.setTime(date.getTime() + 4*3600*1000);

    document.cookie = 'username=' + username + '; expires=' + date.toUTCString();
    document.cookie = 'token=' + token + '; expires=' + date.toUTCString();
};

var unsetCookie = function() {
    document.cookie = 'username=; expires=' + new Date(0);
    document.cookie = 'token=; expires=' + new Date(0);
};

var splitCookie = function(name) {
    var cookies = document.cookie.split(';');

    for(var i = 0; i < cookies.length; i++) {
	var cookie = cookies[i];

	while (cookie.charAt(0) === ' ')
	    cookie = cookie.substring(1);

	if (cookie.indexOf(name + '=') === 0)
	    return cookie.substring(name.length + 1, cookie.length);
    }

    return '';
};

var getCookie = function() {
    return {'username': splitCookie('username'), 'token': splitCookie('token')};
};

var count = 0;
var XHR = function(address, method, auth, data, type, redirect, handler) {
    var completed = false;

    var request = new XMLHttpRequest();

    request.onreadystatechange = function() {
	if (request.readyState === 4) {
	    if ((request.status === 401 || request.status === 403) && redirect) {
		goto('/login');
		return;
	    }

	    if (handler !== null)
		handler(request);

	    completed = true;

	    count--;
	    working = document.getElementById('working');
	    if (count === 0 && working !== null)
		working.style.display = 'none';
	}
    };

    request.open(method, address, true);

    if (auth)
	request.setRequestHeader('Authorization', auth);

    if (data !== null) {
	request.setRequestHeader('Content-Type', type);

	if (type === 'application/json')
	    request.send(JSON.stringify(data));
	else
	    request.send(data);
    }
    else {
	request.send();
    }

    count++;
    setTimeout(function() {
	working = document.getElementById('working');
	if (!completed && working !== null)
	    working.style.display = 'inline-block';
    }, 500);
};

var get = function(address, auth, handler) {
    XHR(address, 'GET', auth, null, null, true, handler);
};

var post = function(address, auth, data, type, handler) {
    XHR(address, 'POST', auth, data, type, true, handler);
};

var put = function(address, auth, data, type, handler) {
    XHR(address, 'PUT', auth, data, type, true, handler);
};

var patch = function(address, auth, data, type, handler) {
    XHR(address, 'PATCH', auth, data, type, true, handler);
};

var del = function(address, auth, handler) {
    XHR(address, 'DELETE', auth, null, null, true, handler);
};
