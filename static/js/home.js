$(function(){
    // 请求统计数据
    $.ajax({
        url: "/tongJi",
        type: 'get',
        dataType: 'text',
        cache: false,
        success: function(data){
            data = JSON.parse(data);
            // 近几日
            $("#container2").highcharts({
                chart: { type: 'line' },
                title: { text: '<strong>近几日的网站访问数据</strong>', useHTML:true },
                xAxis: {
                    categories: data['dr'],   // x 轴分类
                    tickmarkPlacement: 'on',
                    title: '',
                },
                yAxis: {
                    title: { text: null },
                    labels:{ enabled: false },
                    gridLineDashStyle: 'Dash',
                },
                series: [{                              // 数据列
                    name: '访问量pv',                     // 数据列名
                    data: data['pv']               // 数据
                },
                {                              // 数据列
                    name: '访客数uv',                     // 数据列名
                    data: data['uv']               // 数据
                },
                {                              // 数据列
                    name: 'ip数',                     // 数据列名
                    data: data['ipc']               // 数据
                }],
                plotOptions: {
                    line: {
                        dataLabels: {
                            enabled: true
                        }
                    }
                },
                legend: {
                    itemStyle: {
                        font: '9pt Trebuchet MS, Verdana, sans-serif',
                        color: 'black'
                    },
                    itemHoverStyle:{
                        color: 'gray'
                    }
                },
                credits: { enabled: false },
            });
            // 地图
            var mydata = [
                {name: '北京',value: 0 },{name: '天津',value: 0 },
                {name: '上海',value: 0 },{name: '重庆',value: 0 },
                {name: '河北',value: 0 },{name: '河南',value: 0 },
                {name: '云南',value: 0 },{name: '辽宁',value: 0 },
                {name: '黑龙江',value: 0 },{name: '湖南',value: 0 },
                {name: '安徽',value: 0 },{name: '山东',value: 0 },
                {name: '新疆',value: 0 },{name: '江苏',value: 0 },
                {name: '浙江',value: 0 },{name: '江西',value: 0 },
                {name: '湖北',value: 0 },{name: '广西',value: 0 },
                {name: '甘肃',value: 0 },{name: '山西',value: 0 },
                {name: '内蒙古',value: 0 },{name: '陕西',value: 0 },
                {name: '吉林',value: 0 },{name: '福建',value: 0 },
                {name: '贵州',value: 0 },{name: '广东',value: 0 },
                {name: '青海',value: 0 },{name: '西藏',value: 0 },
                {name: '四川',value: 0 },{name: '宁夏',value: 0 },
                {name: '海南',value: 0 },{name: '台湾',value: 0 },
                {name: '香港',value: 0 },{name: '澳门',value: 0 },
                {name: '南海',value: 0 },
            ]
            var diyu = data['diyu']
            for(a in diyu){
                h = {name:diyu[a]['name'], value:diyu[a]['value']}
                mydata.push(h)
            }

            var optionMap = {
                backgroundColor: '#FFFFFF',
                title: {
                    text: '全国访客人数分布',
                    subtext: '数据来源于百度统计',
                    x:'center'
                },
                tooltip : {
                    trigger: 'item',
                    formatter: '{b}<br>{c}人访问'
                },

                legend: {
                    orient: 'vertical',
                    left: 'left'
                },
                visualMap: {
                    min: 0,
                    max: data['diyu_high'],
                    left: 'left',
                    top: 'bottom',
                    text: ['高', '低'],           // 文本，默认为数值文本
                    calculable: true,
                    inRange: {
                        color: ['white','red']
                    }
                },
                //配置属性
                series: [{
                    name: '数据',
                    type: 'map',
                    mapType: 'china',
                    roam: true,
                    label: {
                        normal: {
                            show: false  //省份名称
                        },
                        emphasis: {
                            show: true
                        }
                    },
                    data:mydata  //数据
                }]
            };
            //初始化echarts实例
            var myChart = echarts.init(document.getElementById('uv_map'));
            myChart.setOption(optionMap);
            // 今日访客
            var table = ""
            var latest = data['latest']
            for(var i=0,len=latest.length; i<len; i++){
                var n = i+1
                text = "<tr><th scope='row'>"+n+"</th><td>"+latest[i][0]+"</td><td>"+latest[i][1]+
                        "</td><td>"+latest[i][2]+"</td><td>"+latest[i][3]+"</td><td>"+latest[i][4]+
                        "</td><td>"+latest[i][5]+"</td></tr>"
                table += text;
            }
            if(table==""){
                $(".now_table").html("<tr><th scope='row'>1</th><td>暂无</td><td>暂无</td><td>暂无</td><td>暂无</td><td>暂无</td><td>暂无</td></tr>");
            }else{
                $(".now_table").html(table);
            }
            $(".fa-pulse").remove();
            $(".tong").slideDown("slow");
        }
    });

    // hyouka窗口大小等于浏览器大小
    var winTop = $(window).height();
    $("#bg1").height(winTop);
    (window.onresize = function () {
        var winTop = $(window).height();
        $("#bg1").height(winTop);
    })();
    // hyouka显示与隐藏
    var arrow_num = 0;
    arrow_one();
    function arrow_one(){
        $("#hyouka_arrow").one("click",function(){
            if(arrow_num%2==0){
                $(".hyouka_list:eq(0)").css({opacity:0.6});
                setTimeout(function(){
                    $(".hyouka_list:eq(1)").css({opacity:0.6});
                },300);
                setTimeout(function(){
                    $(".hyouka_list:eq(2)").css({opacity:0.6});
                },600);
                setTimeout(function(){
                    $(".hyouka_list:eq(3)").css({opacity:0.6});
                },900);
                setTimeout(function(){
                    $(".hyouka_list:eq(4)").css({opacity:0.6});
                },1200);
                setTimeout(function(){
                    $(".hyouka_list:eq(5)").css({opacity:0.6});
                },1500);
                setTimeout(function(){
                    $(".hyouka_list:eq(6)").css({opacity:0.6});
                    arrow_one();
                    arrow_num++;
                },1800);
                $(this).addClass("fa-rotate-180");
            }else{
                arrow_num++;
                $(".hyouka_list:eq(0)").css({opacity:0});
                setTimeout(function(){
                    $(".hyouka_list:eq(1)").css({opacity:0});
                },300);
                setTimeout(function(){
                    $(".hyouka_list:eq(2)").css({opacity:0});
                },600);
                setTimeout(function(){
                    $(".hyouka_list:eq(3)").css({opacity:0});
                },900);
                setTimeout(function(){
                    $(".hyouka_list:eq(4)").css({opacity:0});
                },1200);
                setTimeout(function(){
                    $(".hyouka_list:eq(5)").css({opacity:0});
                },1500);
                setTimeout(function(){
                    $(".hyouka_list:eq(6)").css({opacity:0});
                    arrow_one();
                },1800);
                $(this).removeClass("fa-rotate-180");
            }
        });
    }
    // 下雪动画,修改作者插件功能：增加暂停与继续功能，增加多种图片下落功能。
    $('#bg1').snowfall('stop');
    var snow_num = 0;
    //点击按钮控制动画运行，并且第一次点击显示hyouka介绍text。
    $("#snow_player").click(function(){
        if(snow_num==0){
            $('#bg1').snowfall({
                flakeCount: 25,
                flakeIndex: 1,
                maxSpeed: 6,
                minSpeed: 2,
                maxSize: 32,
                minSize: 4,
                image: '/static/image/sakura-'
            })
            $(this).attr("class","fa fa-pause");
            snow_num++;
            return false;
        }
        if(snow_num%2==1){
            $(this).attr("class","fa fa-play");
            $('#bg1').snowfall('stop');
        }else{
            $(this).attr("class","fa fa-pause");
            $('#bg1').snowfall('jixu');
        }
        if(snow_num==1){
            $('#topCatch-01').animate({width: 370}, {duration: 2500, easing: 'linear'});
            $('#topCatch-02').delay(3000).animate({width: 250}, {duration: 1700, easing: 'linear'});
            $('#topCatch-03').delay(5500).animate({width: 250}, {duration: 1700, easing: 'linear'});
            $('#topOnair-01').delay(8000).animate({width: 280}, {duration: 1000, easing: 'linear'});
        }
        snow_num++;
    });
    // 图片放大时显示在最前面，z-index应为最大，并虚化其他图片。
    var hyoukaimg_num = 2;
    $(".hyouka_list").mouseover(function(){
        if(arrow_num%2==1){
            $(this).css({"z-index":hyoukaimg_num,opacity:1});
            $(this).siblings().addClass("hyouka_blur");
            hyoukaimg_num+=2;
        }
    });
    $(".hyouka_list").mouseout(function(){
        if(arrow_num%2==1){
            $(this).css({"z-index":0,opacity:0.6});
            $(this).siblings().removeClass("hyouka_blur");
        }
    });
    // thumbnail鼠标进入特效
    $(".thumbnail").mouseover(function(){
        $(this).addClass("thumbnail_over");
    });
    $(".thumbnail").mouseout(function(){
        $(this).removeClass("thumbnail_over");
        $(this).addClass("thumbnail_out");
    });
    // 抓取图片
    function img_fun1(img_num){
        var img_div = "#img_urls div:eq(" + img_num + ")"
        var img_data = frame2.find(img_div).text();
        $('#bgz-1').fadeOut(1000,function(){
            $('#bgz-2').fadeIn(1000,function(){
                $("#change_img").one("click",function(){
                    img_num++;
                    img_fun2(img_num);
                    frame2.find("#img_urls").attr("title",img_num);
                });
            });
            $('#bgz-1').attr("src",img_data);
        });
    }
    function img_fun2(img_num){
        var img_div = "#img_urls div:eq(" + img_num + ")"
        var img_data = frame2.find(img_div).text();
        $('#bgz-2').fadeOut(1000,function(){
            $('#bgz-1').fadeIn(1000,function(){
                $("#change_img").one("click",function(){
                    img_num++;
                    img_fun1(img_num);
                    frame2.find("#img_urls").attr("title",img_num);
                });
            });
            $('#bgz-2').attr("src",img_data);
        });
    }
    // 访问此页就抓取前两张图片，显示第一张隐藏第二张
    var frame2 = $(parent.frames["hidden-player"].document);
    var img_num = frame2.find("#img_urls").attr("title")
    var img_num2 = img_num - 1
    var img_div1 = "#img_urls div:eq(" + img_num2 + ")";
    var img_div2 = "#img_urls div:eq(" + img_num + ")";
    var img_data1 = frame2.find(img_div1).text();
    var img_data2 = frame2.find(img_div2).text();
    $('#bgz-1').attr("src",img_data1);
    $('#bgz-2').attr("src",img_data2);
    // 点击抓取隐藏第一张显示第二张并在显示第二张的同时在第一张的位置加载第三张，此后再点击的话就循环此动作
    $("#change_img").one("click",function(){
        img_num++;
        img_fun1(img_num);
        frame2.find("#img_urls").attr("title",img_num);
    });
    //展示封面图片
    $(".main_bg").height(winTop/3);

//    $("rect").attr("fill","rgba(255, 255, 255, 0)");
    var sameHei = $(".same").height()*4;
    $(window).scroll(function(){
        var nowTop = $(document).scrollTop();
        $(".same").each(function(){
           var same_show = $(this).offset().top+sameHei;
            if((nowTop+winTop)>same_show){
                $(this).addClass("active");
                $('#chart_set').css({opacity:"1"});
            }
        });
    });
});