function session(obj_id) {
	var stripe = null;
	fetch(`/buy/${obj_id}`, {method: 'GET'})
	.then(function(response) {
	  return response.json();
	})
	.then(function(data) {
	key = data['key']
	session = data['session_id']
	stripe = Stripe(key);
	return stripe.redirectToCheckout({ sessionId: session });
	})
	.then(function(result) {
	  if (result.error) {
		alert(result.error.message);
	  }
	});
}
