# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialfeed', '0004_auto_20140722_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='title',
            field=models.CharField(default='Please set a title for this entry', max_length=100, verbose_name='title'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='provider',
            field=models.CharField(max_length=100, verbose_name='provider', choices=[('socialfeed.providers.instagram.hashtag', 'instagram (hashtag)'), ('socialfeed.providers.facebook', b'facebook (user feed)')]),
        ),
    ]
