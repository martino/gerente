# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clasificador', '0005_classifiermodel_goal_standard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classifiermodel',
            name='goal_standard',
            field=models.ForeignKey(to='documentos.GoalStandard'),
            preserve_default=True,
        ),
    ]
