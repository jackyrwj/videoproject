$(function () {

    // 写入csrf
    $.getScript("/static/js/csrftoken.js");

    // 点赞
    $("#like").click(function(){
      var video_id = $("#like").attr("video-id");
      $.ajax({
            url: '/video/like/',
            data: {
                video_id: video_id,
                'csrf_token': csrftoken
            },
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                var code = data.code
                if(code == 0){
                    var likes = data.likes
                    var user_liked = data.user_liked
                    var get_coupon = data.coupon_get
                    $('#like-count').text(likes)
                    if(user_liked == 0){
                        $('#like').removeClass("grey").addClass("red")
                        var t = document.getElementById('coupon');
                        if(likes >= 20){
                            t.style.display = 'inline';
                            if(get_coupon == false){
                                t.style.color = 'red';
                            } else{
                                t.style.color = 'grey';
                            }
                        } else{
                            t.style.display = 'none';
                        }
                    }else{
                        $('#like').removeClass("red").addClass("grey")
                    }

                }else{
                    var msg = data.msg
                    alert(msg)
                }

            },
            error: function(data){
              alert("点赞失败")
            }
        });
    });


    // 领券
    $("#coupon").click(function(){
      var video_id = $("#ticket").attr("video-id");
      $.ajax({
            url: '/video/coupon/',
            data: {
                video_id: video_id,
                'csrf_token': csrftoken
            },
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                var code = data.code
                if(code == 0){
                    var is_get = data.is_get
                    var t = document.getElementById('content');
                    if(is_get == false){
                        $('#ticket').removeClass("grey").addClass("red")
                        t.textContent = "点击领取"
                    }else{
                        $('#ticket').removeClass("red").addClass("grey")
                        t.textContent = "已领取"
                    }
                }else{
                    var msg = data.msg
                    alert(msg)
                }

            },
            error: function(data){
              alert("领取失败")
            }
        });
    });

     // 收藏
    $("#star").click(function(){
      var video_id = $("#star").attr("video-id");
      $.ajax({
            url: '/video/collect/',
            data: {
                video_id: video_id,
                'csrf_token': csrftoken
            },
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                var code = data.code
                if(code == 0){
                    var collects = data.collects
                    var user_collected = data.user_collected
                    $('#collect-count').text(collects)
                    if(user_collected == 0){
                        $('#star').removeClass("grey").addClass("red")
                    }else{
                        $('#star').removeClass("red").addClass("grey")
                        alert("领取成功")
                    }
                }else{
                    var msg = data.msg
                    alert(msg)
                }

            },
            error: function(data){
              alert("收藏失败")
            }
        });
    });


    // 提交评论
    var frm = $('#comment_form')
    frm.submit(function () {
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            dataType:'json',
            data: frm.serialize(),
            success: function (data) {
                var code = data.code
                var msg = data.msg
                if(code == 0){
                    $('#id_content').val("")
                    $('.comment-list').prepend(data.html);
                    $('#comment-result').text("评论成功")
                    $('.info').show().delay(2000).fadeOut(800)
                }else{
                    $('#comment-result').text(msg)
                    $('.info').show().delay(2000).fadeOut(800);
                }
            },
            error: function(data) {
            }
        });
        return false;
    });

})





