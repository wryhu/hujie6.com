# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Comment
from .forms import CommentForm
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta
from django.urls import reverse


# 提交评论用ajax异步处理
def submit_comment(request):
    # 创建评论表单
    comment_form = CommentForm(request.POST, user=request.user)
    # 若验证成功
    data = {}

    if comment_form.is_valid():
        # 生成一条评论保存到数据库
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()

        # 返回给ajax数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        data['user_pk'] = comment.user.pk
        data['comment_time'] = (comment.comment_time + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.text
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)


def submit_reply(request):
    data = {}
    try:
        parent_reply_id = request.POST.get('parent_reply_id')
        root_comment_id = request.POST.get('root_comment_id')
        content_type = request.POST.get('content_type')
        model_class = ContentType.objects.get(model=content_type).model_class()
        object_id = int(request.POST.get('object_id'))

        comment = Comment()
        comment.user = request.user
        comment.text = request.POST.get('reply_text')
        comment.content_object = model_class.objects.get(id=object_id)
        comment.root = Comment.objects.get(id=root_comment_id)
        comment.parent = Comment.objects.get(id=parent_reply_id)
        comment.reply_to_user = comment.parent.user
        comment.save()

        # 返回给ajax数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username

        data['comment_time'] = (comment.comment_time + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
        data['reply_to_user'] = comment.reply_to_user.username
        data['text'] = comment.text
        data['reply_pk'] = comment.pk
        data['user_pk'] = comment.user.pk
    except Exception as e:
        print(e)
        data['status'] = 'ERROR'
        data['message'] = '回复失败'
    return JsonResponse(data)
