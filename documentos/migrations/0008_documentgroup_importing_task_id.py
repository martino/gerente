# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0007_auto_20150126_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentgroup',
            name='importing_task_id',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
