# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-06 21:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0017_auto_20171206_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercontribution',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
