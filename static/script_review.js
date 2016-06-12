$(document).ready( function () {
    $('#submit').on('click', function() {
        $.ajax({
            method: 'POST',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                text:$('#message-text').val(),
                type: 'comment'
            }),
            url: '/rates',
            success: function(data) {
                if(data.status == 'ok') {
                    $('.comment-wrap').remove()
                    $('.comments-wrapper').append(data.markup);
                    $('.comment-number').text(data.review_amounts+ ' reviews')
                    $('#message-text').val("")
                    $('.rt-notifications>*').remove()
                    if('notification' in data) {
                        $('.rt-notifications').append(data.notification)
                    }
                } else {
                    $('.rt-notifications>*').remove()
                    if('notification' in data) {
                        $('.rt-notifications').append(data.notification)
                    }
                }
            }
        })
    })

})


