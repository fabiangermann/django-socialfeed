# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialfeed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='provider',
            field=models.CharField(max_length=100, verbose_name='provider', choices=[(b'socialfeed.providers.instagram.InstagramProvider', 'instagram')]),
        ),
    ]
