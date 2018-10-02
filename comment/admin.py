# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Comment
from django.contrib import admin


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'text', 'comment_time', 'user']
