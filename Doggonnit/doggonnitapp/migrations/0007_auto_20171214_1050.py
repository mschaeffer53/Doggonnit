# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-14 18:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doggonnitapp', '0006_auto_20171212_1611'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=25)),
                ('lat', models.FloatField()),
                ('long', models.FloatField()),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('weight', models.CharField(max_length=25)),
                ('age', models.CharField(max_length=25)),
                ('color', models.CharField(max_length=25)),
                ('breed', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='dogprofile',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='marker',
            name='dog',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='doggonnitapp.DogProfile'),
        ),
    ]
