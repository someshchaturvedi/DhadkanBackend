# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 23:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cvd_portal', '0004_auto_20170901_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.IntegerField(default=1),
        ),
    ]
