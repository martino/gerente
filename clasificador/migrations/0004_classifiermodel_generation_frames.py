# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0002_auto_20150110_1750'),
        ('clasificador', '0003_classifiermodel_testing_task_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='classifiermodel',
            name='generation_frames',
            field=models.ManyToManyField(to='documentos.Frame'),
            preserve_default=True,
        ),
    ]
