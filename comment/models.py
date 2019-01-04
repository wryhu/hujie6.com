# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import threading
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render


class SendMail(threading.Thread):
    def __init__(self, text, fail_silently=False):
        self.subject = '你的网站有人评论'
        self.text = text
        self.email = '736209298@qq.com'
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=self.fail_silently,
            html_message=self.text
)


# 建立评论模型
class Comment(models.Model):
    # 下面三行是评论的对象(就是哪个文章下的评论)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    # 这里括号里可以省略不写
    content_object = GenericForeignKey('content_type', 'object_id')

    # 评论内容
    text = models.TextField()
    # 评论时间
    comment_time = models.DateTimeField(auto_now_add=True)
    # 评论者,用的框架自带模型
    user = models.ForeignKey(User, related_name="comments")

    # 接下来创建回复功能,使用这个评论模型,因为回复和评论一样也需要有对象,内容,回复时间和回复人.不同的是
    # 回复的对象必须是回复或评论,不能是文章等对象,这是和评论的区别,所以要多创建几个如下字段.

    # 先创建回复的对象,因为回复可以回复回复,所以创建外键关联自身的类似上下级关系的字段parent,另外回复的对象必须是评论或回复,所以设置可为null,对象为null时就是顶级评论()
    parent = models.ForeignKey('self', related_name="child_replies_for_reply", null=True)
    # 为了查询方便,直接创建回复的对象的用户字段.同样,若是顶级评论时对应的回复对象不是评论而是文章,所以null设为True
    reply_to_user = models.ForeignKey(User, related_name="child_replies_for_user", null=True)
    # 创建顶级评论字段,方便查询当前顶级评论下的所有回复
    root = models.ForeignKey('self', related_name="child_replies_for_root", null=True)

    def send_mail(self, num):
        context = {}
        context['comment_text'] = self.text
        context['url'] = self.content_object.get_url()
        context['title'] = self.content_object.title
        # 回复
        if num == 2:
            context['name'] = '%s 回复给 @%s' % (self.user.first_name, self.reply_to_user.first_name)
        # 评论
        else:
            context['name'] = self.user.first_name
        text = render(None, 'comment/send_mail.html', context).content.decode('utf-8')
        send_mail = SendMail(text)
        send_mail.start()

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ['-comment_time']