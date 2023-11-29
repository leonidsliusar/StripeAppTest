console.log(`{{key}}`);
var stripe = Stripe('pk_test_51Mo3QcCf3ABPW4Y39UtVE2GfamiOpZOE9oEs5Qtk0tPG3hrbosYV68EP8xpAgGnSvUIuAbQmwC2HMntYScmC2ETM00Wtx0pRm7');



function session(obj_id) {
	fetch(`/buy/${obj_id}`, {method: 'GET'})
	.then(function(response) {
	  return response.json();
	})
	.then(function(session) {
	  return stripe.redirectToCheckout({ sessionId: session.id });
	})
	.then(function(result) {
	  if (result.error) {
		alert(result.error.message);
	  }
	});
}
