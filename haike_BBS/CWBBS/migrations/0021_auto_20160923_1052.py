# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-23 02:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CWBBS', '0020_auto_20160923_1050'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment_statue',
            old_name='is_useful',
            new_name='statue',
        ),
    ]