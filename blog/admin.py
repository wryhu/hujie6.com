# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import BlogType, Blog
from django.contrib import admin


# 装饰器注册法,代码相比以前的方法更明朗
@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type_name']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'blog_type', 'author', 'get_read_num', 'thumbnail', 'tag', 'created_time', 'last_updated_time']


