# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-09 15:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cvd_portal', '0008_auto_20170909_1509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='user_type',
        ),
    ]
