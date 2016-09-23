# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-31 08:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CWBBS', '0009_auto_20160828_1853'),
    ]

    operations = [
        migrations.CreateModel(
            name='Praise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_post_id', models.IntegerField(default=0)),
                ('p_comment_id', models.IntegerField(default=0)),
                ('p_user_id', models.IntegerField(default=0)),
                ('is_up', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
