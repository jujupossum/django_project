# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-22 20:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0014_auto_20170618_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='total_classes',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]