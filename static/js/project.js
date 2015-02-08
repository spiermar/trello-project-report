$(function() {
	$.getJSON( "api/v1/backlog", function( data ) {
		var backlog = data.backlog;
		$.each(backlog, function(index, card) {
			$("#backlog").append($('<div></div>').addClass("card").append($('<h2></h2>').addClass("card-heading simple").html(card.name)).append($('<div></div>').addClass('card-body').append($('<p></p>').html(card.description))));
		});
		$('#backlog .fa-spin').hide();
	});
	$.getJSON( "api/v1/release", function( data ) {
		var release = data.release;
		$.each(release, function(index, card) {
			$("#release").append($('<div></div>').addClass("card").append($('<h2></h2>').addClass("card-heading simple").html(card.name)).append($('<div></div>').addClass('card-body').append($('<p></p>').html(card.description))));
		});
		$('#release .fa-spin').hide();
	});
	$.getJSON( "api/v1/ready", function( data ) {
		var ready = data.ready;
		$.each(ready, function(index, card) {
			$("#ready").append($('<div></div>').addClass("card").append($('<h2></h2>').addClass("card-heading simple").html(card.name)).append($('<div></div>').addClass('card-body').append($('<p></p>').html(card.description))));
		});
		$('#ready .fa-spin').hide();
	});
});