# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-16 16:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='oauthex',
            old_name='qq_openid',
            new_name='open_id',
        ),
    ]