# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0002_auto_20150110_1750'),
        ('pruebas', '0008_auto_20150110_1750'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrameAnnotation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('test_results', models.TextField()),
                ('raw_result', models.TextField(null=True, blank=True)),
                ('frame', models.ForeignKey(to='documentos.Frame', null=True)),
                ('test_running', models.ForeignKey(to='pruebas.BaseTestResult')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
    ]
