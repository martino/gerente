# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0001_initial'),
        ('clasificador', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('json_model', models.TextField()),
                ('micro_f1', models.FloatField()),
                ('macro_f1', models.FloatField()),
                ('micro_precision', models.FloatField()),
                ('macro_precision', models.FloatField()),
                ('micro_recall', models.FloatField()),
                ('macro_recall', models.FloatField()),
                ('model_version', models.ForeignKey(to='clasificador.ClassifierModel')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentAnnotation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('test_results', models.TextField()),
                ('document_part', models.ForeignKey(to='documentos.DocumentPart')),
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
