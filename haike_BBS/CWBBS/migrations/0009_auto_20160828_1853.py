# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-28 10:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CWBBS', '0008_auto_20160827_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CWBBS.BBS_user'),
        ),
    ]
