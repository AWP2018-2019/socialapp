# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-18 14:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20181211_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
    ]
