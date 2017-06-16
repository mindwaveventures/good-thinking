# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-16 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20170615_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='hero_image_position',
            field=models.TextField(choices=[('center', 'center'), ('top', 'top'), ('right', 'right'), ('bottom', 'bottom'), ('left', 'left')], default='center', help_text='Background position the hero image'),
        ),
    ]