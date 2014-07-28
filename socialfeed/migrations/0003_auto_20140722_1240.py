# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialfeed', '0002_auto_20140718_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='provider_id',
            field=models.CharField(help_text='provider related identifier of subscription', max_length=100, null=True, verbose_name='provider id', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='is active'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='provider',
            field=models.CharField(max_length=100, verbose_name='provider', choices=[('socialfeed.providers.instagram.hashtag', 'instagram (hashtag)')]),
        ),
    ]
