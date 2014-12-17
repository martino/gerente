# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pruebas', '0004_auto_20141215_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentannotation',
            name='raw_result',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
