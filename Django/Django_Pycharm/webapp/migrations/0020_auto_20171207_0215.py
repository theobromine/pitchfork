# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-07 07:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0019_auto_20171206_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='pitched',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
