# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-18 06:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cvd_portal', '0002_auto_20170818_0627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientdata',
            name='time_stamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 18, 6, 59, 28, 42305)),
        ),
    ]
