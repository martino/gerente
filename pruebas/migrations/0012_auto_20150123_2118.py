# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0005_auto_20150123_2107'),
        ('clasificador', '0006_auto_20150121_2129'),
        ('pruebas', '0011_basetestresult_confusion_matrix'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentTestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('json_model', models.TextField()),
                ('document_group', models.ForeignKey(to='documentos.DocumentGroup')),
                ('model_version', models.ForeignKey(related_name='doc_test', to='clasificador.ClassifierModel')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='documentannotation',
            name='test_running',
            field=models.ForeignKey(to='pruebas.DocumentTestResult'),
            preserve_default=True,
        ),
    ]
