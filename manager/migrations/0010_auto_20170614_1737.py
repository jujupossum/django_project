# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-14 17:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0009_auto_20170614_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
