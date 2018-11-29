$(function(){
    var current_page = 1;
    var media_last = $("#ajax_blog").children(".media").last();
    var media_height = media_last.height() + 28; //此元素高度加上padding和border
    var media_height2 = media_last.offset().top - $(document).scrollTop();//此元素距离窗口顶部
    var final_height = $(window).height() - media_height - media_height2;//此元素距离窗口底部
    var media_height3 = media_height + 15; //每一次加载多出来的高度
    var initial_height = 100;
    var check_num = 1;
    $(window).scroll(function(){
        var media_height2 = media_last.offset().top - $(document).scrollTop();//此元素距离窗口顶部
        var final_height = $(window).height() - media_height - media_height2;//此元素距离窗口底部
        if(final_height>initial_height){
            current_page++;
            $.ajaxSetup({
                data:{csrfmiddlewaretoken:'{{ csrf_token }}'},
            });
            $.ajax({
                url: "{% url 'ajax_blog' %}",
                type: 'POST',
                data: {"start":current_page},
                dataType: 'text',
                cache: false,
                success: function(data){
                    if(data=="{}"){
                        if(check_num==1){
                            var media_html = '<h3 class="media2">已加载全部文章，感谢您的支持</h2>'
                            $("#ajax_blog").append(media_html);
                            $(".media2").slideDown("slow");
                            check_num = 2;
                        }
                        return false;
                    }else{
                        var data = JSON.parse(data)
                        var media_html = '<div class="media figcaption cp_'+current_page+'" style="display:none"><div class="row"><div class="col-md-3 media_img">\
                                        <div class="media-left media-middle"><a href="/blog/'+data['id']+'/">\
                                        <img src="/media/'+data['thumbnail']+'" height="150" width="150">\
                                        <figcaption></figcaption></a></div></div><div class="col-md-9"><div class="media-body">\
                                        <h3 class="media-heading"><a href="/blog/'+data['id']+'/">'+data['title']+'</a></h3>\
                                        <div id="content">'+data['content']+'</div><a id="tagset" href="#">\
                                        <button type="button" class="btn btn-default btn-xs"><span class="glyphicon glyphicon-grain"></span> 作者: jet\
                                        </button></a> <a href="/blog/type_'+data['type_id']+'"><button type="button" class="btn btn-default btn-xs">\
                                        <span class="glyphicon glyphicon-star-empty"></span> '+data['blog_type']+'</button></a>\
                                        <button type="button" class="btn btn-default btn-xs"><span class="glyphicon glyphicon-time"></span> '+data['created_time']
                                        +'</button> <button type="button" class="btn btn-default btn-xs">\
                                        <span class="glyphicon glyphicon-eye-open"></span> 阅读: '+data['read_num']
                                        +'</button> <button type="button" class="btn btn-default btn-xs">\
                                        <span class="glyphicon glyphicon-comment"></span> 评论: '+data['comment_num']
                                        +'</button></div></div></div></div>'
                        $("#ajax_blog").append(media_html)
                        var cp = ".cp_"+current_page;
                        $(cp).slideDown("slow",function(){
                            $(cp).removeClass("figcaption");
                        });
                    }
                }
            });
            initial_height+=media_height3;
        }
    });
});