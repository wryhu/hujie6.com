# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import OAuthEx
from django.contrib import admin


# 装饰器注册法,代码相比以前的方法更明朗
@admin.register(OAuthEx)
class OAuthExAdmin(admin.ModelAdmin):
    list_display = ['user', 'open_id']
