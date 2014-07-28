# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import __builtin__
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('source_id', models.CharField(max_length=100, verbose_name='source id')),
                ('data', jsonfield.fields.JSONField(default=__builtin__.dict, verbose_name=b'data')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('provider', models.CharField(max_length=100, verbose_name='provider')),
                ('config', jsonfield.fields.JSONField(default=__builtin__.dict, verbose_name=b'config', blank=True)),
            ],
            options={
                'verbose_name': 'subscription',
                'verbose_name_plural': 'subscriptions',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='subscription',
            field=models.ForeignKey(to='socialfeed.Subscription'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([(b'subscription', b'source_id')]),
        ),
    ]
