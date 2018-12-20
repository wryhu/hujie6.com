$(function(){
    // 百度统计
    var _hmt = _hmt || [];
    (function() {
      var hm = document.createElement("script");
      hm.src = "https://hm.baidu.com/hm.js?4c1f8e68be72fa6ae0e0bbbda1cb56b8";
      var s = document.getElementsByTagName("script")[0];
      s.parentNode.insertBefore(hm, s);
    })();
    // 导航栏图标特效，引用jquery.easing函数。
    jQuery.extend( jQuery.easing,
    {
        easeOutBounce: function (x, t, b, c, d) {
            if ((t/=d) < (1/2.75)) {
                return c*(7.5625*t*t) + b;
            } else if (t < (2/2.75)) {
                return c*(7.5625*(t-=(1.5/2.75))*t + .75) + b;
            } else if (t < (2.5/2.75)) {
                return c*(7.5625*(t-=(2.25/2.75))*t + .9375) + b;
            } else {
                return c*(7.5625*(t-=(2.625/2.75))*t + .984375) + b;
            }
        },
    });
    var frame = $(parent.frames["hidden-player"].document)
    //logo切换
    var logo_num = frame.find(".logo_num").text();
    $(".pad").hover(function(){
        $(this).children("i").css("color",logo_num).animate({top:0},800,"easeOutBounce");
    },function(){
        $(this).children("i").css("color","rgba(0, 0, 0, 0.43)");
    });
    $("#exchange").click(function(){
        if(logo_num=="red"){
            $("#site_logo1").attr("src","/static/image/geassblue2.png");
            $("#site_logo2").attr("src","/static/image/geassblue1.png");
            frame.find(".logo_num").text("blue");
            logo_num="blue";
        }else if(logo_num=="blue"){
            $("#site_logo1").attr("src","/static/image/geassyellow2.png");
            $("#site_logo2").attr("src","/static/image/geassyellow1.png");
            frame.find(".logo_num").text("yellow");
            logo_num="yellow";
        }else if(logo_num=="yellow"){
            $("#site_logo1").attr("src","/static/image/geassred2.png");
            $("#site_logo2").attr("src","/static/image/geassred1.png");
            frame.find(".logo_num").text("red");
            logo_num="red";
        }
    });
    //网站logo变化
    function logo_change(){
        $("#site_logo1").fadeIn(2000,function(){
            $("#site_logo1").fadeOut(2000);
        });
        $("#site_logo2").fadeOut(2000,function(){
            $("#site_logo2").fadeIn(2000);
        });
    }
    logo_change();
    var timer = setInterval(logo_change,5000);
    $("#site_logo_a").mouseover(function(){
        clearInterval(timer);
        $("#site_logo1").stop().fadeOut(0);
        $("#site_logo2").stop().fadeIn(0);
    });
    $("#site_logo_a").mouseout(function(){
        $("#site_logo2").stop().fadeOut(0);
        $("#site_logo1").stop().fadeIn(0);
        logo_change();
        timer = setInterval(logo_change,5000);
    });
    var searchNum = 0;
    $("#search-click").click(function(){
        if(searchNum%2==0){
            $("#navbar-form").fadeIn();
            $("#search_box").focus().stop().animate({width:"200px"},500);
        }else{
            $("#search_box").stop().animate({width:"0"},500,function(){
                $("#navbar-form").fadeOut();
            });
        }
        searchNum++;
    });

    // 小火箭
    var navNum1 = 0;
    var navNum2 = 0;
    $(window).scroll(function(){
        var rockTop = $(document).scrollTop();
        if(rockTop==0){
            $('#navbar-base').css({top:0});
            $('#navbar-base').removeClass("navbar-scroll");
            navNum2 = 0;
        }
        if(rockTop>0&&navNum2==0){
            $('#navbar-base').addClass("navbar-scroll");
            navNum2 = 1;
        }
        if(rockTop>61&&navNum1==0){
            $("#navbar-shou").fadeIn(660);
            navNum1 = 1;
        }
        if(rockTop<61&&navNum1==1){
            $("#navbar-shou").fadeOut(660);
            navNum1 = 0;
        }
        if(rockTop>500){
            $('#totop').fadeIn();
        }
        else{
            $('#totop').fadeOut();
        }
    });
    // 鼠标绑定移入事件：循环上下
    function rock1(){
        $('#totop').stop().animate({marginBottom:"0px"},800,rock2);
    }
    function rock2(){
        $('#totop').stop().animate({marginBottom:"30px"},800,rock1);
    }
    $('#totop').mouseenter(function(){
        rock2();
    });
    // 鼠标绑定移出事件：停止并回到原位
    $('#totop').mouseleave(function(){
        $(this).stop().animate({marginBottom:"0px"},200);
    });
    // 点击火箭就跟着滚动条一起上升，然后取消绑定的鼠标移出和移入事件，不然上升时又回到原位了，然后火箭隐藏，火箭复位，火箭再次绑定鼠标移出事件。
    $('#totop').click(function(){
        var html_height = $(window).height()
        $('html,body').animate({'scrollTop':0},800);
        $(this).stop().unbind('mouseleave');
        $(this).unbind('mouseenter');
        $(this).css({opacity:1});
        $(this).stop().animate({marginBottom:html_height},800,function(){
            $(this).fadeOut(function(){
                $(this).css({opacity:0.5,marginBottom:0});
                $(this).bind('mouseleave', function(){
                    $(this).stop().animate({marginBottom:"0px"},200);
                });
                $(this).bind('mouseenter', function(){
                    rock2();
                });
            });
        });
    });
    // 播放器：从框架提取播放器html到网站页面，并加入定时器
    function real_time_music1(){
        var music_html = frame.find("#skPlayer").html();
        $(".skPlayer1").html(music_html);
        $(".skPlayer1 .skPlayer-play-btn").remove();
    }
    real_time_music1();
    // 二次提取设置透明合并到上面（其中播放按钮不透明，上层播放按钮直接删除）
    function real_time_music2(){
        var music_html = frame.find("#skPlayer").html();
        $(".skPlayer2").html(music_html);
        $(".skPlayer2 .skPlayer-control").css({top:"-100px","z-index":5,opacity:0});
        $(".skPlayer2 .skPlayer-cover").remove();
        $(".skPlayer-play-btn").css({outline:"none"});
    }
    real_time_music2();
    // 禁止播放器列表滚动冒泡,第一种方法，也是最简单的
    $('.skPlayer-list').mouseover(function(){
        $(this).css('overscroll-behavior','contain');
    });
    // 第二种方法
    function scrollFunc(e){
        var X = $('#music-bar').position().top;
        var mX = e.clientX
        var mY = e.clientY
        if((mX<100 && mY>X)){
            e.preventDefault();
        }
    }
    if(document.addEventListener){
        document.addEventListener('DOMMouseScroll',scrollFunc,false);
    }//火狐
    window.onmousewheel=document.onmousewheel=scrollFunc;//IE/Opera/Chrome
    $("#music-bar").mouseover(function(){
        $(this).stop().animate({marginLeft:"14px",marginBottom:"14px"},300);
        // 第一次打开时的提示
        if(frame.find('.prev_music').text()=='1'){
            $(this).attr('data-original-title','点我打开音乐播放器');
            $(this).tooltip('show');
            return false;
        }
        // 第二次到第n次打开时的提示
        if($("#music").css("margin-left")=="0px"){
            if($(".fa-chrome").attr("class")=="fa fa-chrome fa-spin"){
                $(this).attr('data-original-title','正在播放，如果你也有好听的歌可以联系主人推荐添加哦，联系方式在页面最下方（点我打开）');
            }else{
                $(this).attr('data-original-title','都是主人精心挑选的歌曲，跳转网页也不会中断播放哦（点我打开）');
            }
        }else{
            if($(".fa-chrome").attr("class")=="fa fa-chrome fa-spin"){
                $(this).attr('data-original-title','好听吧，不愧是主人的品味！下拉列表还有很多哦（点我收起）');
            }else{
                $(this).attr('data-original-title','歌曲尚未播放，主人每月会更新一次曲库，敬请期待哦（点我收起）');
            }
        }
        $(this).tooltip('show');
    });
    $("#music-bar").mouseout(function(){
        $(this).stop().animate({marginLeft:"0px",marginBottom:"0px"},300);
    });
    var i=0;
    $("#music-bar").click(function(){
        if(i%2==0){
            // 进行滑出动画
            $('#music').stop().animate({marginLeft:"388px"},800);
            window.time1 = setInterval(real_time_music1,300);
            i++;
        }else{
            // 收回播放器就停止定时器来停止加载播放器页面
            $('#music').stop().animate({marginLeft:"0px"},800);
            clearInterval(time1);
            i++;
        }
        frame.find('.prev_music').text("2");
    });
    // 接下来设置每个按钮的传递
    // 播放暂停，并使主页上的播放按钮显示正确状态
    $(document).on('click', ".skPlayer-play-btn", function(){
        if($(this).attr("class")=="skPlayer-play-btn skPlayer-pause"){
            frame.find(".skPlayer-right").click();
            $(this).attr("class","skPlayer-play-btn");
            $(".fa-chrome").attr("class","fa fa-chrome");
        }else{
            frame.find(".skPlayer-left").click();
            $(this).attr("class","skPlayer-play-btn skPlayer-pause");
            $(".fa-chrome").attr("class","fa fa-chrome fa-spin");
        }
    });
    // 音量开关
    $(".skPlayer-icon").click(function(){
        frame.find(".skPlayer-icon").click();
    });
    // 切换单曲循环
    $(".skPlayer-mode").click(function(){
        frame.find(".skPlayer-mode").click();
    });
    // 列表显示与否
    $(".skPlayer-list-switch").click(function(){
        $(".skPlayer-list").slideToggle();
    });
    // 点击列表內歌曲播放
    $(document).on('click', ".skPlayer-list li", function(){
        var num1 = $(this).attr("data-index");
        var text = ".skPlayer-list li[data-index="+num1+"]";
        frame.find(text).click();
        $(".skPlayer-list li").removeAttr("class");
        $(this).attr("class","skPlayer-curMusic");
        $(".skPlayer-play-btn").attr("class","skPlayer-play-btn skPlayer-pause");
        $(".fa-chrome").attr("class","fa fa-chrome fa-spin");
    });
    // 上一首,并且为播放状态
    $(document).on('click', ".fa-backward", function(){
        frame.find(".prev_music").click();
        var num2 = frame.find(".skPlayer-curMusic").attr("data-index");
        var text2 = ".skPlayer-list li[data-index="+num2+"]";
       $(".skPlayer-list li").removeAttr("class");
        $(text2).attr("class","skPlayer-curMusic");
        $(".skPlayer-play-btn").attr("class","skPlayer-play-btn skPlayer-pause");
        $(".fa-chrome").attr("class","fa fa-chrome fa-spin");
    });
    // 下一首,并且为播放状态
    $(document).on('click', ".fa-forward", function(){
        frame.find(".next_music").click();
        $(".skPlayer-play-btn").attr("class","skPlayer-play-btn skPlayer-pause");
        var num2 = frame.find(".skPlayer-curMusic").attr("data-index");
        var text2 = ".skPlayer-list li[data-index="+num2+"]";
        $(".skPlayer-list li").removeAttr("class");
        $(text2).attr("class","skPlayer-curMusic");
        $(".fa-chrome").attr("class","fa fa-chrome fa-spin");
    });
    var frame_play_btn = frame.find(".skPlayer-play-btn")
    function chrome_spin(){
        if(frame_play_btn.attr("class")=="skPlayer-play-btn skPlayer-pause"){
            $(".fa-chrome").attr("class","fa fa-chrome fa-spin");
        }else{
            $(".fa-chrome").attr("class","fa fa-chrome");
        }
    }
    chrome_spin();
    // 音量(鼠标模拟点击)
    $(document).on('click', "#skPlayer-voice", function(e){
        var vx = e.pageX;
        var target1 = parent.window.frames["hidden-player"].document.getElementById('skPlayer-voice');
        var eventObj = document.createEvent('MouseEvents');
        eventObj.initMouseEvent('click',true,true,window,0,vx,100,vx,150,false,false,true,false,0,null);
        target1.dispatchEvent(eventObj);
    });
    // 音乐进度(鼠标模拟点击)
    $(document).on('click', "#skPlayer-load", function(e){
        $(".skPlayer-play-btn").attr("class","skPlayer-play-btn skPlayer-pause");
        $(".fa-chrome").attr("class","fa fa-chrome fa-spin");
        var lx = e.pageX;
        var target2 = parent.window.frames["hidden-player"].document.getElementById('skPlayer-load');
        var eventObj = document.createEvent('MouseEvents');
        eventObj.initMouseEvent('click',true,true,window,0,lx,100,lx,150,false,false,false,false,0,null);
        target2.dispatchEvent(eventObj);
        console.log(lx)

    });
    //按下F5时，只刷新mainFrame，兼容IE、FF
    function mykeyDown(e){
        var ev = e ? e :event;
        if(window.addEventListener){
          if(ev.keyCode==116){//F5的键盘常用ASCII码为116
            parent.frames['main'].location.reload();
            ev.preventDefault();
            return false;
             }
         }else{
           if(ev.keyCode==116){
               ev.keyCode=0;
               ev.returnValue=false;
               parent.frames('main').location.reload();
               return false;
             }
         }
    }
    //给每个frame都绑定onkeydown事件
    window.onload =function(){
        document.onkeydown = mykeyDown;
        for(var i=0;i<frames.length;i++){
            if (typeof document.addEventListener != "undefined") {
                frames[i].document.addEventListener("keydown",mykeyDown,true);
            } else {
                frames[i].document.attachEvent("onkeydown", mykeyDown);
            }
        }
    };
    //footer和云
    var footNum = 0;
    var skyNum = 0;
    $(window).scroll(function(){
        var nowTop = $(document).scrollTop() + $(window).height();
        var rawTop = $(document).height();
        var skyTop = $("#footer_fluid").offset().top;
        if((nowTop>skyTop)&&(skyNum==0)){
            $("#footer_sky").show();
            skyNum=1;
        }
        if((nowTop<skyTop)&&(skyNum==1)){
            $("#footer_sky").hide();
            skyNum=0;
        }
        if(nowTop==rawTop){
            $("footer").stop().animate({bottom:0},700);
            footNum=1;
        }
        if(nowTop<rawTop&&footNum==1){
            $("footer").stop().animate({bottom:"-190px"},700);
            footNum=0;
        }
    });
    //导航栏收
    $("#navbar-shou").click(function(){
        $("#navbar-base").stop().animate({top:"-61px"},100,function(){
            $('#navbar-base').removeClass("navbar-scroll");
            $('#navbar-shou').hide();
            $("#search_box").stop().animate({width:"0"},500,function(){
                $("#navbar-form").fadeOut();
            });
            searchNum=0;
        });
    });
    if(/Android|webOS|iPhone|iPod|BlackBerry/i.test(navigator.userAgent)) {
        $("#bg1").remove();
        $("#friend_link").remove();
    }
});