function ajaxGet(address, handler) {
	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4)
			handler(ajax)
	}
	ajax.open('GET', address, true);
	ajax.send();
}

function ajaxPost(address, data, handler) {
	var ajax = new XMLHttpRequest();
	ajax.onload = function() {
		if(ajax.readyState == 4)
			handler(ajax)
	}
	ajax.open('POST', address, true);
	ajax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	var request = [];
	for(var key in data)
		request.push(encodeURIComponent(key) + '=' + encodeURIComponent(data[key]))
	ajax.send(request.join('&'));
}
