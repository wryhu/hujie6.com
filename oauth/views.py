# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.conf import settings

from oauth_client import OAuth_QQ, OAuth_GITHUB
from oauth.models import OAuthEx

import time


# http://hujie6.com/oauth/qq_login
def qq_login(request):
    oauth_qq = OAuth_QQ(settings.QQ_APP_ID, settings.QQ_KEY, settings.QQ_RECALL_URL)

    # 获取 得到Authorization Code的地址
    url = oauth_qq.get_auth_url()
    # 重定向到授权页面
    return HttpResponseRedirect(url)


# http://hujie6.com/oauth/qq_check
def qq_check(request):
    """登录之后，会跳转到这里。需要判断code和state"""
    request_code = request.GET.get('code')
    oauth_qq = OAuth_QQ(settings.QQ_APP_ID, settings.QQ_KEY, settings.QQ_RECALL_URL)

    # 获取access_token
    access_token = oauth_qq.get_access_token(request_code)  # OAuth_QQ类内部会在这一步添加access_token属性值
    time.sleep(0.05)  # 稍微休息一下，避免发送urlopen的10060错误
    # 通过access_token获取openid
    open_id = oauth_qq.get_open_id()

    # 检查open_id是否存在
    qqs = OAuthEx.objects.filter(open_id=open_id)
    if qqs:
        # 存在则获取对应的用户，并登录
        user = qqs[0].user

        # 设置backend，绕开authenticate验证。绕开的原因是这里已经可以确定用户使用过qq登录过网站。
        # authenticate方法得到的user对象和普通的user对象多了一个backend参数。手动设置一下这个参数，则可以顺利使用login方法登录该用户。
        setattr(user, 'backend', 'django.contrib.auth.backends.ModelBackend')

        login(request, user)
        return HttpResponseRedirect('/index')
    else:
        # 不存在，则跳转到绑定邮箱页面
        info = oauth_qq.get_qq_info()  # 通过openid获取用户信息
        url = '%s?open_id=%s&nickname=%s' % (reverse('bind_email'), open_id, info['nickname'])
        return HttpResponseRedirect(url)


# http://hujie6.com/oauth/github_login
def github_login(request):
    oauth_github = OAuth_GITHUB(settings.GITHUB_APP_ID, settings.GITHUB_KEY, settings.GITHUB_RECALL_URL)

    # 获取 得到Authorization Code的地址
    url = oauth_github.get_auth_url()
    # 重定向到授权页面
    return HttpResponseRedirect(url)


# http://hujie6.com/oauth/github_check
def github_check(request):
    """登录之后，会跳转到这里。需要判断code和state"""
    request_code = request.GET.get('code')
    oauth_github = OAuth_GITHUB(settings.GITHUB_APP_ID, settings.GITHUB_KEY, settings.GITHUB_RECALL_URL)

    # 获取access_token
    access_token = oauth_github.get_access_token(request_code)
    time.sleep(0.05)  # 稍微休息一下，避免发送urlopen的10060错误
    # 通过access_token获取openid
    result, open_id = oauth_github.get_github_info()

    # 检查open_id是否存在
    gits = OAuthEx.objects.filter(open_id=open_id)
    if gits:
        # 存在则获取对应的用户，并登录
        user = gits[0].user

        setattr(user, 'backend', 'django.contrib.auth.backends.ModelBackend')

        login(request, user)
        return HttpResponseRedirect('/index')
    else:
        # 不存在，则跳转到绑定邮箱页面
        info = result
        url = '%s?open_id=%s&nickname=%s' % (reverse('bind_email'), open_id, info['login'])
        return HttpResponseRedirect(url)


def bind_email(request):
    open_id = request.GET.get('open_id')
    nickname = request.GET.get('nickname')
    context = {}
    context['nickname'] = nickname

    if request.method == 'POST':
        email = request.POST.get('email')
        pwd = request.POST.get('password')

        users = User.objects.filter(email=email)
        if users:
            # 用户存在,进一步判断
            user = users[0]
            user_auth = authenticate(username=user.username, password=pwd)
            if user_auth is not None:
                user.username = nickname  # 更新昵称
                user.save()
            else:
                context['warning'] = '密码错误'
                context['email'] = email
                return render(request, 'bind_email.html', context)
        else:
            # 用户不存在，则注册
            user = User.objects.create_user(username=nickname, email=email, password=pwd)
            user.save()

        # 绑定用户并
        oauth_ex = OAuthEx(user=user, open_id=open_id)
        oauth_ex.save()

        # 登录用户
        user = authenticate(username=nickname, password=pwd)
        if user is not None:
            login(request, user)

        # 页面提示
        context['email'] = email
        context['goto_url'] = '/index'
        context['goto_page'] = True

        return render(request, 'message.html', context)

    return render(request, 'bind_email.html', context)