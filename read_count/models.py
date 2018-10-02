# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


# 这个比较特殊, 提供处理阅读数量的一个独立的应用, 独立出来的原因是可以让其他应用也能直接调用
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    # 这里括号里可以省略不写
    content_object = GenericForeignKey('content_type', 'object_id')


# 应用在admin页面显示不出阅读数的具体数值时,调用下面代码即可
class Present_read_num(object):
    def get_read_num(self):
        try:
            # 因为是独立出来的应用,所以其他应用(比如博客)刚创建出来后没有readnum属性,所以判断有的话返回其阅读数,没有设为0
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0


# 建立单个文章每天的阅读量的模型
class ReadDetail(models.Model):
    date = models.DateField(default=timezone.now)
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    # 这里括号里可以省略不写
    content_object = GenericForeignKey('content_type', 'object_id')
