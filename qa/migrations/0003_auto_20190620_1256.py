# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-20 12:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0002_auto_20190619_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='date',
            field=models.DateField(default=datetime.date(2019, 6, 20)),
        ),
        migrations.AlterField(
            model_name='questions',
            name='date',
            field=models.DateField(default=datetime.date(2019, 6, 20)),
        ),
    ]
