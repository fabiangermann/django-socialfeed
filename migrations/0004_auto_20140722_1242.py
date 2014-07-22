# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialfeed', '0003_auto_20140722_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='subscription_id',
            field=models.CharField(help_text='provider related identifier of subscription', max_length=100, null=True, verbose_name='subscription id', blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='provider_id',
        ),
    ]
