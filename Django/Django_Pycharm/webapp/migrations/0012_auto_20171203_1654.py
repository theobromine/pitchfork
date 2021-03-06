# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-03 21:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0011_auto_20171203_1649'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('group_id', models.IntegerField(default=0)),
                ('user_id', models.IntegerField(default=0)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('paid_bit', models.BooleanField(default=False)),
                ('paypal_id', models.CharField(max_length=50)),
                ('paid_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payout',
            fields=[
                ('payout_id', models.AutoField(primary_key=True, serialize=False)),
                ('group_id', models.IntegerField(default=0)),
                ('user_id', models.IntegerField(default=0)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('paid_bit', models.BooleanField(default=False)),
                ('paypal_id', models.CharField(max_length=50)),
                ('paid_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Payments',
        ),
    ]
