# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from read_count.models import Present_read_num, ReadDetail


# 博客分类
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __unicode__(self):
        return self.type_name


# 博客主体
class Blog(models.Model, Present_read_num):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType)
    tag = models.CharField(max_length=15, null=True)
    # 文章缩略图名称 jump.jpg
    thumbnail = models.ImageField(upload_to='thumbnail/%Y/%m/%d/', null=True)
    content = RichTextField()
    author = models.ForeignKey(User)
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('blog_detail', args=[self.pk])

    def get_email(self):
        return self.author.email

    def __unicode__(self):
        return "<blogtitle: %s>" % self.title

    class Meta:
        ordering = ['-created_time']




