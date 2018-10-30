# coding=utf-8
import datetime
import random
import re
import requests
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


# 百度图片爬虫
def img_crwaler():
    url = "https://image.baidu.com/search/flip?tn=baiduimage&word=%E9%A3%8E%E6%99%AF&pn=" + str(random.randint(0, 1780))\
          + "&width=1920&height=1080"
    res = requests.get(url)
    html = res.text
    q = r'http://[^"]+pg'
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


# 提供给下方函数调用
def reading_trend(read_nums):
    # 前七天的阅读量变化: 人生的路总像这样曲曲折折~~~
    num = 0
    if [0 for i in range(7)] == read_nums:
        print(read_nums)
        # 前七天的阅读量变化: 一篇都没人看?这也太真实了吧!
        num = 1
    # 前七天的阅读量变化: 近几日上升回温,我的春天要来了吗?
    if read_nums[4] < read_nums[5] < read_nums[6]:
        num = 4
    # 前七天的阅读量变化: 连续多天的上升状态,最高にhighってやつだ!
    if read_nums[2] < read_nums[3] < read_nums[4] < read_nums[5] < read_nums[6]:
        num = 5
    # 前七天的阅读量变化: 近几日下降明显,好吧我已经习惯了~
    if read_nums[4] > read_nums[5] > read_nums[6]:
        num = 6
    # 前七天的阅读量变化: 连续多天的下降状态,这破站吃枣药丸啊!
    if read_nums[2] > read_nums[3] > read_nums[4] > read_nums[5] > read_nums[6]:
        num = 7
    n = 0
    for i in range(6):
        if read_nums[i] < read_nums[i + 1]:
            n += 1
        if read_nums[i] > read_nums[i + 1]:
            n -= 1
    # 前七天的阅读量变化: 一路飙升,我这是要上天啊!
    if 6 == n:
        num = 2
    # 前七天的阅读量变化: 一路下降,holy shit!
    if -6 == n:
        num = 3
    return num


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    # 给一些数据设置数据库缓存,我设置保存一天
    sevendays_cache = cache.get('seven_cache')
    if sevendays_cache is None:
        sevendays_cache = get_7_days_hot_blog()
        cache.set('seven_cache', sevendays_cache, 43200)
    num_cache = reading_trend(read_nums)
    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['num'] = num_cache
    context['get_today_hot_data'] = get_today_hot_data(blog_content_type)
    context['get_yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['get_7_days_hot_blog'] = sevendays_cache
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


def page_not_found(request):
    context = {}
    user_name = request.user.username
    if user_name == '':
        context['user_name'] = '亲爱的游客'
    else:
        context['user_name'] = request.user.username
    return render(request, '404.html', context)


def frame(request):
    return render(request, 'frame.html')


def music(request):
    return render(request, 'music.html')


def jojo(request):
    return render(request, 'jojo.html')


def main(request):
    return render(request, 'main.html')


def privacy_policy(request):
    return render(request, 'privacy_policy.html')