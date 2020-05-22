$(function() {

	const likesBtn = (pk) => {
	    $(`.fas.fa-heart.fa-2x[data-index-number="${pk}"]`).toggle();
	    $(`.far.fa-heart.fa-2x[data-index-number="${pk}"]`).toggle();
	};

	$('.likes-form').on('submit', e => {
	    e.preventDefault();
	    const pk = e.target.dataset.indexNumber;
	    toggleLike(pk);
	});

	const toggleLike = (pk) => {
	    const serializeData = $(`.likes-form[data-index-number="${pk}"]`).serialize();

	    $.ajax({
	        url: `post/${pk}/likes/`,
	        type: 'POST',
	        data: serializeData,
	        success: json => {
	        	likesBtn(pk);
	    	},
	      	error: (xhr, errmsg, err) => {
	        	console.log(errmsg);
	    	}
	  	});
	};

	window.addEventListener('load', () => {
	    $('.likes-form').each(function() {
	      	const pk = $(this).context.dataset.indexNumber;
	      	const serializeData = $(`.likes-form[data-index-number="${pk}"]`).serialize();

	      	$.ajax({
		        url: `post/${pk}/likes/`,
		        type: 'GET',
		        data: serializeData,
		        success: json => {
		          	if (json.current === 'blank') {
		            	$(`.fas.fa-heart.fa-2x[data-index-number="${pk}"]`).hide();
		            	$(`.far.fa-heart.fa-2x[data-index-number="${pk}"]`).show();
		          	} else if (json.current === 'liked') {
		            	$(`.fas.fa-heart.fa-2x[data-index-number="${pk}"]`).show();
		            	$(`.far.fa-heart.fa-2x[data-index-number="${pk}"]`).hide();
		          	}
		        },
		        error: (xhr, errmsg, err) => {
		          	console.log(errmsg);
		        }
	      	});
	    });
  	});

});