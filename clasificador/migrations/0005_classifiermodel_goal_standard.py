# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0003_auto_20150121_2059'),
        ('clasificador', '0004_classifiermodel_generation_frames'),
    ]

    operations = [
        migrations.AddField(
            model_name='classifiermodel',
            name='goal_standard',
            field=models.ForeignKey(to='documentos.GoalStandard', null=True),
            preserve_default=True,
        ),
    ]
