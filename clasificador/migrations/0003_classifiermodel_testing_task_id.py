# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clasificador', '0002_remove_classifiermodel_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='classifiermodel',
            name='testing_task_id',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
