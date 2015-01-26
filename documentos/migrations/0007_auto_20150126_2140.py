# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0006_documentgroup_testing_task_id'),
    ]

    operations = [
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
