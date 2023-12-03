const currentUrl = window.location.href


function redirect(path) {
	window.location.href = currentUrl + path;
}
