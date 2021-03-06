# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-30 16:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('searchkeyws', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilteredUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='WSFilteredUrlsRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_proyecto', models.IntegerField()),
                ('nombre_directorio', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='filteredurl',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urls', to='searchkeyws.WSFilteredUrlsRequest'),
        ),
    ]
