# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 23:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cvd_portal', '0005_auto_20170901_2318'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patientdata',
            old_name='bp',
            new_name='systolic',
        ),
        migrations.AddField(
            model_name='patientdata',
            name='diastolic',
            field=models.IntegerField(default=0),
        ),
    ]
