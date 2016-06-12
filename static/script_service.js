$(document).ready( function () {
    $('#submit').on('click', function() {
        var name = $(this).attr('service-name');
        $.ajax({
            method: 'POST',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                text:$('#message-text').val(),
                service: name,
                type: 'comment'
            }),
            url: '/services/'+name,
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
        var name = $('body').attr('service');

        $.ajax({
            method: 'POST',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                text:$('#message-text').val(),
                service: name,
                type: 'like'
            }),
            url: '/services/'+name,
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
        var translatorId = $(this).attr('translator-id');

        $('#translator-modal-'+translatorId).removeAttr('style')
    })

    $('.send-mail-button').on('click', function() {
        var translatorName = $(this).attr('translator');
        var translatorId = $(this).attr('translator-id');

        $('#translator-modal-'+translatorId).css({display:'none'})
        var slug = $('body').attr('service');

        $.ajax({
            method: 'POST',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                service: slug,
                translator: translatorName
            }),
            url: '/translator/mail',
            success: function(data) {
                $('.rt-notifications').append(data.notification)
            }

        })

    })

})

