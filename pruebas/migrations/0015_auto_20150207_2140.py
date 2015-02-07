# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pruebas', '0014_auto_20150126_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frameannotation',
            name='raw_scoring',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
