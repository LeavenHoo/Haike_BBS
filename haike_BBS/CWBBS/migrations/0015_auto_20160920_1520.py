# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-20 07:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CWBBS', '0014_auto_20160913_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='praise_comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CWBBS.BBS_user'),
        ),
    ]
