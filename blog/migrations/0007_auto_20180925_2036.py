# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-25 12:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20180921_2230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='thumbnail_name',
        ),
        migrations.AddField(
            model_name='blog',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to='thumbnail/%Y/%m/%d/'),
        ),
    ]
