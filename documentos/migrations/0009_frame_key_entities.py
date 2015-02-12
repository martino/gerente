# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0008_documentgroup_importing_task_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='frame',
            name='key_entities',
            field=django_extensions.db.fields.json.JSONField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
