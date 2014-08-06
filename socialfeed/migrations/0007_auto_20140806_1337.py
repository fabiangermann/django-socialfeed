# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialfeed', '0006_auto_20140804_1503'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': [b'-created_at'], 'verbose_name': 'post', 'verbose_name_plural': 'posts'},
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(null=True, verbose_name='crated at'),
        ),
    ]
