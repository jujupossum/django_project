# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-28 19:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
