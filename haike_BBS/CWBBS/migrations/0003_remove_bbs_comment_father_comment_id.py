# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-22 03:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CWBBS', '0002_remove_category_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bbs_comment',
            name='father_comment_id',
        ),
    ]
