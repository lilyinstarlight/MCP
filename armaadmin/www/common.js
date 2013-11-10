function ajaxGet(address, handler, response_type='') {
	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4)
			handler(ajax);
	};
	ajax.open('GET', address, true);
	ajax.responseType = response_type;
	ajax.send();
}

function ajaxPost(address, data, handler, type='urlencoded', response_type='') {
	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4)
			handler(ajax);
	};
	ajax.open('POST', address, true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	ajax.responseType = response_type;
	ajax.send(encode(data, type));
}

function sjaxGet(address, response_type='') {
	var sjax = new XMLHttpRequest();
	sjax.open('GET', address, false);
	sjax.responseType = response_type;
	sjax.send();

	return sjax;
}

function sjaxPost(address, data, type='urlencoded', response_type='') {
	var sjax = new XMLHttpRequest();
	sjax.open('POST', address, false);
	sjax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	sjax.responseType = response_type;
	sjax.send(encode(data, type));

	return sjax;
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
