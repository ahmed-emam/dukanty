# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-08 20:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('rating', models.DecimalField(decimal_places=4, max_digits=5)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
            ],
        ),
    ]
