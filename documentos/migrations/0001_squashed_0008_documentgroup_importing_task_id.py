# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    replaces = [(b'documentos', '0001_initial'), (b'documentos', '0002_auto_20150110_1750'), (b'documentos', '0003_auto_20150121_2059'), (b'documentos', '0004_auto_20150122_2122'), (b'documentos', '0005_auto_20150123_2107'), (b'documentos', '0006_documentgroup_testing_task_id'), (b'documentos', '0007_auto_20150126_2140'), (b'documentos', '0008_documentgroup_importing_task_id')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('file_name', models.TextField()),
                ('original_text', models.TextField()),
                ('goal_standard', models.TextField()),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('text', models.TextField()),
                ('annotations', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('name', models.TextField()),
                ('alternative_names', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='frame',
            name='node',
            field=models.ForeignKey(to='documentos.Node'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='GoalStandard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('name', models.TextField()),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SuperNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('name', models.TextField()),
                ('verbose_name', models.TextField(null=True, blank=True)),
                ('goal_standard', models.ManyToManyField(to=b'documentos.GoalStandard')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='node',
            name='super_node',
            field=models.ManyToManyField(to=b'documentos.SuperNode', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='DocumentGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('name', models.TextField()),
                ('testing_task_id', models.TextField(null=True, blank=True)),
                ('importing_task_id', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='basedocument',
            name='group',
            field=models.ForeignKey(blank=True, to='documentos.DocumentGroup', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basedocument',
            name='goal_standard',
            field=django_extensions.db.fields.json.JSONField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='frame',
            name='annotations',
            field=django_extensions.db.fields.json.JSONField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
