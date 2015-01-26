# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('pruebas', '0013_documenttestresult_scoring_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basetestresult',
            name='confusion_matrix',
            field=django_extensions.db.fields.json.JSONField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basetestresult',
            name='json_model',
            field=django_extensions.db.fields.json.JSONField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='documentannotation',
            name='raw_result',
            field=django_extensions.db.fields.json.JSONField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='documentannotation',
            name='test_results',
            field=django_extensions.db.fields.json.JSONField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='documenttestresult',
            name='json_model',
            field=django_extensions.db.fields.json.JSONField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='documenttestresult',
            name='scoring_result',
            field=django_extensions.db.fields.json.JSONField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='frameannotation',
            name='raw_result',
            field=django_extensions.db.fields.json.JSONField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='frameannotation',
            name='raw_scoring',
            field=django_extensions.db.fields.json.JSONField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='frameannotation',
            name='test_results',
            field=django_extensions.db.fields.json.JSONField(),
            preserve_default=True,
        ),
    ]
