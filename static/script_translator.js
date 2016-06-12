$(document).ready( function () {
    $('#submit').on('click', function() {
        var name = $(this).attr('translator-name');
        $.ajax({
            method: 'POST',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                text:$('#message-text').val(),
                translator: name,
                type: 'comment'
            }),
            url: '/interpreters/'+name,
            success: function(data) {
                if(data.status == 'ok') {
                    $('.comment-wrap').remove()
                    $('.comments-wrapper').append(data.markup);
                    $('.comment-number').text(data.comment_amount+ ' comments')
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
    $('#likes-amount-button').on('click',function() {
        var name = $('body').attr('translator');

        $.ajax({
            method: 'POST',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                text:$('#message-text').val(),
                translator: name,
                type: 'like'
            }),
            url: '/interpreters/'+name,
            success: function(data) {
                $('#likes-amount-field').text(data.likes_amount)
                if(data.refuse_like) {
                    $('#likes-amount-button').removeAttr('style')
                } else {
                    $('#likes-amount-button').css({color:'#128DB4'})
                }
                $('.rt-notifications>*').remove()
                if('notification' in data) {
                    $('.rt-notifications').append(data.notification)
                }
            }

        })
    })
    $('.modal-open-window').on('click', function() {
        var serviceId = $(this).attr('service-id');

        $('#service-modal-'+serviceId).removeAttr('style')
    })

    $('.send-mail-button').on('click', function() {
        var serviceName = $(this).attr('service');
        var serviceId = $(this).attr('service-id');

        $('#service-modal-'+serviceId).css({display:'none'})
        var slug = $('body').attr('translator');

        $.ajax({
            method: 'POST',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                translator: slug,
                service: serviceName
            }),
            url: '/service/mail',
            success: function(data) {
                $('.rt-notifications').append(data.notification)
            }

        })

    })
})

