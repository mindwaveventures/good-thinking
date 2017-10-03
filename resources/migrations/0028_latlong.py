# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-02 13:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import resources.models.resources


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0027_auto_20170918_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='LatLong',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('latitude', resources.models.resources.LatitudeField(max_length=10)),
                ('longitude', resources.models.resources.LongitudeField(max_length=10)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='latlong', to='resources.ResourcePage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
