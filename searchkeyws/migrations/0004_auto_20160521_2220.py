# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-21 22:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('searchkeyws', '0003_filteredurl_orden'),
    ]

    operations = [
        migrations.AddField(
            model_name='wsfilteredurlsrequest',
            name='id_request',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='searchkeyws.WSRequest'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wsresponse',
            name='id_request',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='searchkeyws.WSRequest'),
            preserve_default=False,
        ),
    ]
