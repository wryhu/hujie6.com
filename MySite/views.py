# coding=utf-8
import datetime
import random
import re
import requests
import json
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum
from django.urls import reverse
from django.http import JsonResponse
from read_count.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from blog.models import Blog
from .forms import LoginForm, RegForm
from .youdao import Translate
from .tianqiapi import tianqi_api
from django.contrib.sessions.models import Session


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def online(request):
    ip = get_ip(request)
    request.session[ip] = "online_ip"
    return JsonResponse({"0": 0})


def show_online(request):
    online_sessions = Session.objects.filter(expire_date__gte=datetime.datetime.now())  # 获取未过期的sessions
    onlines = [os for os in online_sessions if "online_ip" in os.get_decoded().values()]
    return JsonResponse({"online": len(onlines)})


def tuling(ask_message):
    url = 'http://openapi.tuling123.com/openapi/api/v2'
    body = {
        "reqType":0,
        "perception": {
            "inputText": {
                "text": ask_message
            }
        },
        "userInfo": {
            "apiKey": "f05916358def466eab92e144251e6c7f",
            "userId": "364250"
        }
    }
    data = json.dumps(body)
    response = requests.post(url, data=data)
    retext = response.text
    return json.loads(retext)['results'][0]['values']['text']


def xiaoxin(request):
    xiao_text = request.POST.get("xiao_text", "")
    data = {}
    try:
        data['data'] = tuling(xiao_text)
    except Exception:
        data['data'] = ""
    return JsonResponse(data)


# 有道翻译
def translate(request):
    input_text = request.POST.get("input_text", "")
    lan1 = request.POST.get("lan1", "AUTO")
    lan2 = request.POST.get("lan2", "AUTO")
    t = Translate(input_text, lan1, lan2)
    data = {}
    try:
        data['data'] = t.youdao()
    except Exception:
        data['data'] = ""
    return JsonResponse(data)


# 图片爬虫
def img_crwaler():
    url = "https://pic.sogou.com/pics/channel/getAllRecomPicByTag.jsp?category=壁纸&tag=全部&start="\
          + str(random.randint(0, 1000)) + "&len=100&width=1920&height=1080"
    res = requests.get(url)
    html = res.text
    q = r'"thumbUrl":"([^"]+)'
    url_list = re.findall(q, html)
    return url_list


# ajax方式提取数据，不影响音乐播放器的正常加载
def ajax_img_crwaler(request):
    data = {}
    data['img_urls'] = img_crwaler()
    return JsonResponse(data)


def get_7_days_hot_blog():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    # read_details是Blog和ReadDetail建立关联的字段(Blog模型中有写)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gt=date)\
            .values('id', 'title')\
            .annotate(read_num_sum=Sum('read_details__read_num'))\
            .order_by('-read_num_sum')
    return blogs[:7]


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    # 给一些数据设置数据库缓存,我设置保存一天
    sevendays_cache = cache.get('seven_cache')
    if sevendays_cache is None:
        sevendays_cache = get_7_days_hot_blog()
        cache.set('seven_cache', sevendays_cache, 43200)
    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['get_today_hot_data'] = get_today_hot_data(blog_content_type)
    context['get_yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['get_7_days_hot_blog'] = sevendays_cache
    try:
        tianqi = tianqi_api(get_ip(request))
    except Exception as e:
        tianqi = "查询国内天气可以直接询问小新哦，他经常在线的嘿嘿"
    context['tianqi'] = tianqi
    return render(request, 'home.html', context)


# 登录处理
def login(request):
    if request.method == 'POST':
        # 建立含有post数据的登录表单实例
        login_form = LoginForm(request.POST)
        # 表单验证成功就让该用户变成登录状态并跳转到登录前页面
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            form = "=" + request.GET.get('form', reverse('home'))
            url = form.split('=')[-1]
            return redirect(url)
    else:
        # get页面请求就生成原始表单
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)


# 注册验证
def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        # 验证注册成功就创建用户实例到数据库保存
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.first_name = username
            user.save()
            # 用户登录并跳转回注册前页面
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            form = "=" + request.GET.get('form', reverse('home'))
            url = form.split('=')[-1]
            return redirect(url)
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('form', reverse('home')))


def music(request):
    return render(request, 'music.html')


def jojo(request):
    return render(request, 'jojo.html')


def main(request):
    return render(request, 'main.html')


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def move(request):
    return render(request, 'move.html')


def mobile(request):
    return render(request, 'mobile.html')


def frame(request):
    context = {}
    context["url_path"] = "/main"
    return render(request, 'frame.html', context)


def frames(request):
    url_path = request.path
    context = {}
    context["url_path"] = url_path.split("frames")[1]
    return render(request, 'frame.html', context)

