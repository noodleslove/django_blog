$(function() {
	const csrfToken = $('input[name=csrfmiddlewaretoken]').val();


	$(document).ready(function() {
	    $('.likes-form').each(function() {
	    	const url = $(this)[0].dataset.url;
	      	const pk = $(this)[0].dataset.indexNumber;
	      	const serializeData = $(`.likes-form[data-index-number="${pk}"]`).serialize();

	      	$.ajax({
		        url: url,
		        type: 'GET',
		        data: serializeData,
		        success: json => {
		          	if (json.current === 'blank') {
		            	$(`.likes-img[data-index-number="${pk}"]`).attr('src', '/static/blog/img/heart-outline.svg');
		          	} else if (json.current === 'liked') {
		            	$(`.likes-img[data-index-number="${pk}"]`).attr('src', '/static/blog/img/heart-solid-pink.svg');
		          	}
		        },
		        // console the error message
		        error: (xhr, errmsg, err) => {
		          	console.log(errmsg);
		        }
	      	});
	    });
  	});


	const toggleLike = pk => {
		const url = $(`.likes-form[data-index-number="${pk}"]`).data('url');
	    const serializeData = $(`.likes-form[data-index-number="${pk}"]`).serialize();

	    $.ajax({
	        url: url,
	        type: 'POST',
	        data: serializeData,
	        success: json => {
	        	if (json.status === 'removed') {
	        		$(`.likes-img[data-index-number="${pk}"]`).attr('src', '/static/blog/img/heart-outline.svg');
	        	} else if (json.status === 'added') {
	        		$(`.likes-img[data-index-number="${pk}"]`).attr('src', '/static/blog/img/heart-solid-pink.svg');
	        	}
	    	},
	    	// console the error message
	      	error: (xhr, errmsg, err) => {
	        	console.log(errmsg);
	    	}
	  	});
	};


	const postBtnState = (input, btn) => {
		if ($(input).val()) {
			$(btn).prop('disabled', false);
			$(btn).removeClass('disabled');
		} else {
			$(btn).prop('disabled', true);
			$(btn).addClass('disabled');
		}
	}


	$('.likes-btn').on('click', e => {
	    e.preventDefault();
	    const pk = e.target.dataset.indexNumber;
	    toggleLike(pk);
	});


	$('.comment-input').on('input', function(e) {
		const btn = $(this)[0].parentNode.lastElementChild;

		if ($(this).val()) {
			$(btn).prop('disabled', false);
			$(btn).removeClass('disabled');
		} else {
			$(btn).prop('disabled', true);
			$(btn).addClass('disabled');
		}
	});


	const newComment = (pk, value) => {
		const url = $(`.comment-form[data-index-number="${pk}"]`).data('url');

		$.ajax({
			url: url,
			type: 'POST',
			data: {
				csrfmiddlewaretoken: csrfToken,
				commentText: value
			},
			success: json => {
				const input = $(`#comment-${pk}`).val('');
				const btn = $(`#comment-${pk}`)[0].parentNode.lastElementChild;

				postBtnState(input, btn);

				const markup = `
					<li class="list-group-item px-3 py-1 border-0">
						<span class="text-muted mr-2 text-uppercase font-weight-bold">${json.author}</span>${json.text}
					</li>
				`;

				const markup2 = `
					<li class="list-group-item px-3 p-0 mb-3 border-0">
	                    <img src="${json.url}" alt="" class="rounded-circle article-img mr-2" draggable="false">
	                    <span class="text-muted mr-2 text-uppercase font-weight-bold">${json.author}</span>
	                    ${json.text}
	                </li>
				`;

				$(`ul[data-index-number="${pk}"]`).append(markup);
				$('.detail-ul').prepend(markup2);
			}
		});
	}


	$('.comment-form').on('submit', function(e) {
		e.preventDefault();
		const pk = e.target.dataset.indexNumber;
		const text = e.currentTarget[1].value;
		newComment(pk, text);
	});


	$('.bookmark-btn').on('click', e => {
		e.preventDefault();
		const pk = e.currentTarget.firstElementChild.dataset.indexNumber;
		const obj = $(e.currentTarget.firstElementChild).attr('src');

		if (obj === '/static/blog/img/bookmark-outline.svg') {
			$(`.bookmark-img[data-index-number="${pk}"]`).attr('src', '/static/blog/img/bookmark-solid-black.svg');
		} else {
			$(`.bookmark-img[data-index-number="${pk}"]`).attr('src', '/static/blog/img/bookmark-outline.svg');
		}
		
	});
});