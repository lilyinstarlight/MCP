function change(parent, child) {
	var element = document.getElementById(parent);
	for(var node in element.childNodes) {
		if(element.childNodes[node].nodeType == 1 && element.childNodes[node].tagName.toLowerCase() == 'div')
			element.childNodes[node].style.display = 'none';
	}
	document.getElementById(child).style.display = 'block';
}

function XHR(address, method, data, type, response_type, handler) {
	var request = new XMLHttpRequest();
	request.onload = function() {
		if(request.readyState == 4)
			handler(request);
	};
	request.responseType = response_type;
	request.open(method, address, true);
	if(data != null) {
		request.setRequestHeader('Content-type', getMIME(type));
		request.send(encode(data, type));
	}
	else {
		request.send();
	}
}

function getMIME(type) {
	switch(type) {
		case 'urlencoded':
			return 'application/x-www-form-urlencoded';
		case 'json':
			return 'application/json';
		default:
			return type;
	}
}
function encode(data, type) {
	switch(type) {
		case 'urlencoded':
			var request = [];
			for(var key in data)
				request.push(encodeURIComponent(key) + '=' + encodeURIComponent(data[key]));
			return request.join('&');
		case 'json':
			return JSON.stringify(data);
		default:
			return data;
	}
}

function textGet(address, handler) {
	XHR(address, 'GET', null, null, 'text', handler);
}

function textPost(address, data, handler) {
	XHR(address, 'POST', data, 'urlencoded', 'text', handler);
}

function jsonGet(address, handler) {
	XHR(address, 'GET', null, null, 'json', handler);
}

function jsonPost(address, data, handler) {
	XHR(address, 'POST', data, 'urlencoded', 'json', handler);
}
