# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pruebas', '0012_auto_20150123_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='documenttestresult',
            name='scoring_result',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
