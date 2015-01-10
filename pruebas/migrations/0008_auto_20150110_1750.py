# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pruebas', '0007_goalstandard_generation_frame'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goalstandard',
            name='class_obj',
        ),
        migrations.DeleteModel(
            name='GoalStandard',
        ),
        migrations.DeleteModel(
            name='ModelClass',
        ),
    ]
