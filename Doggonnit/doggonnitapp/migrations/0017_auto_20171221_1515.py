# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-21 23:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('doggonnitapp', '0016_auto_20171219_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='dogprofile',
            name='missing_since',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='missingdogreport',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
