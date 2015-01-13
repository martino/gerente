# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pruebas', '0009_frameannotation'),
    ]

    operations = [
        migrations.AddField(
            model_name='frameannotation',
            name='raw_scoring',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
