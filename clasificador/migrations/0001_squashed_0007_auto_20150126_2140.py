# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    replaces = [(b'clasificador', '0001_initial'), (b'clasificador', '0002_remove_classifiermodel_description'), (b'clasificador', '0003_classifiermodel_testing_task_id'), (b'clasificador', '0004_classifiermodel_generation_frames'), (b'clasificador', '0005_classifiermodel_goal_standard'), (b'clasificador', '0006_auto_20150121_2129'), (b'clasificador', '0007_auto_20150126_2140')]

    dependencies = [
        ('documentos', '0002_auto_20150110_1750'),
        ('documentos', '0003_auto_20150121_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassifierModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('json_model', django_extensions.db.fields.json.JSONField()),
                ('name', models.TextField()),
                ('datatxt_id', models.TextField(null=True, blank=True)),
                ('testing_task_id', models.TextField(null=True, blank=True)),
                ('generation_frames', models.ManyToManyField(to=b'documentos.Frame')),
                ('goal_standard', models.ForeignKey(to='documentos.GoalStandard')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
    ]
