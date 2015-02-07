# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    replaces = [(b'pruebas', '0001_initial'), (b'pruebas', '0002_auto_20141208_2214'), (b'pruebas', '0003_auto_20141208_2218'), (b'pruebas', '0004_auto_20141215_2214'), (b'pruebas', '0005_documentannotation_raw_result'), (b'pruebas', '0006_auto_20150106_1747'), (b'pruebas', '0007_goalstandard_generation_frame'), (b'pruebas', '0008_auto_20150110_1750'), (b'pruebas', '0009_frameannotation'), (b'pruebas', '0010_frameannotation_raw_scoring'), (b'pruebas', '0011_basetestresult_confusion_matrix'), (b'pruebas', '0012_auto_20150123_2118'), (b'pruebas', '0013_documenttestresult_scoring_result'), (b'pruebas', '0014_auto_20150126_2112')]

    dependencies = [
        ('documentos', '0002_auto_20150110_1750'),
        ('clasificador', '0001_squashed_0007_auto_20150126_2140'),
        ('documentos', '0001_initial'),
        ('documentos', '0005_auto_20150123_2107'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('json_model', models.TextField()),
                ('micro_f1', models.FloatField(null=True, blank=True)),
                ('macro_f1', models.FloatField(null=True, blank=True)),
                ('micro_precision', models.FloatField(null=True, blank=True)),
                ('macro_precision', models.FloatField(null=True, blank=True)),
                ('micro_recall', models.FloatField(null=True, blank=True)),
                ('macro_recall', models.FloatField(null=True, blank=True)),
                ('model_version', models.ForeignKey(related_name='test', to='clasificador.ClassifierModel')),
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
                ('test_results', django_extensions.db.fields.json.JSONField()),
                ('test_running', models.ForeignKey(to='pruebas.DocumentTestResult')),
                ('document', models.ForeignKey(to='documentos.BaseDocument', null=True)),
                ('raw_result', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FrameAnnotation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('test_results', django_extensions.db.fields.json.JSONField()),
                ('raw_result', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
                ('frame', models.ForeignKey(to='documentos.Frame', null=True)),
                ('test_running', models.ForeignKey(to='pruebas.BaseTestResult')),
                ('raw_scoring', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='basetestresult',
            name='confusion_matrix',
            field=django_extensions.db.fields.json.JSONField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='DocumentTestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('json_model', django_extensions.db.fields.json.JSONField()),
                ('document_group', models.ForeignKey(to='documentos.DocumentGroup')),
                ('model_version', models.ForeignKey(related_name='doc_test', to='clasificador.ClassifierModel')),
                ('scoring_result', django_extensions.db.fields.json.JSONField(null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='basetestresult',
            name='json_model',
            field=django_extensions.db.fields.json.JSONField(),
            preserve_default=True,
        ),
    ]
