# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-14 08:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0024_auto_20170912_1224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resourcepage',
            name='video_url',
        ),
    ]