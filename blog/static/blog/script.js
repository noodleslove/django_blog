$(function() {
  // Hide an element
  $(".red-box").hide();

  // Show it again
  $(".red-box").show();

  // Just toggle visibility depending on whether element is shown or hidden
  $(".red-box").toggle();  // hides

  // Up until this point, you can't even see what happens in the browser
  // because it happens in a matter of milliseconds.

  // Use show/hide as animations (not very commonly used)
  $(".green-box").hide(1000);
  $(".green-box").show(1000);

  $('.blue-box').delay(1000).animate({
    'margin-left': '+=100px'
  }, 1500, () => {
    $('.red-box').toggle(1000);
  });

  var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
  
  $('.comment-form').on('submit', e => {
    e.preventDefault();
    const pk = e.target.dataset.indexNumber;
    postComment(pk);
  });

  const postComment = function(pk) {
    const text = $(`#comment-${pk}`).val();

    $.ajax({
      url: `post/${pk}/`,
      type: 'POST',
      data: {
        csrfmiddlewaretoken: csrfToken,
        commentText: text
      },
      success: json => {
        $(`#comment-${pk}`).val('');
        console.log(json);
        $("#talk").prepend(`<li><strong>${json.text}</strong> - <em>${json.author}</em></li>`);
      },
      error: (xhr, errmsg, err) => {
        console.log(errmsg);
      }
    });
  };



});