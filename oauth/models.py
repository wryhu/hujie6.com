# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class OAuthEx(models.Model):
    user = models.ForeignKey(User)
    qq_openid = models.CharField(max_length=64)  # QQ的关联OpenID

    def __unicode__(self):
        return u'<%s>' % self.user
