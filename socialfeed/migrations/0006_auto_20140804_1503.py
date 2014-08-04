# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('socialfeed', '0005_auto_20140723_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='crated at'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='provider',
            field=models.CharField(max_length=100, verbose_name='provider', choices=[('socialfeed.providers.instagram_hashtag', 'instagram (hashtag)'), ('socialfeed.providers.facebook_userfeed', b'facebook (user feed)'), ('socialfeed.providers.youtube_channel', 'Youtube (channel)'), ('socialfeed.providers.twitter_stream', 'Twitter (stream)')]),
        ),
    ]
