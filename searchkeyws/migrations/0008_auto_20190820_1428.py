# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2019-08-20 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchkeyws', '0007_auto_20190514_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchurl',
            name='url',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='wsfilteredurlsrequest',
            name='nombre_directorio',
            field=models.CharField(max_length=255),
        ),
    ]
