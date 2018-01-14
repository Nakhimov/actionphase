# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-13 08:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('houseoffun', '0009_gamesignup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesignup',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signups', to='houseoffun.Game'),
        ),
        migrations.AlterUniqueTogether(
            name='gamesignup',
            unique_together=set([('game', 'user')]),
        ),
    ]
