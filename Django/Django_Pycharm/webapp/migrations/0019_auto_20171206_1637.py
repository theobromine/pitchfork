# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-06 21:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0018_auto_20171206_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='picture',
            field=models.ImageField(blank=True, upload_to='item/%Y/%m/%d'),
        ),
    ]
