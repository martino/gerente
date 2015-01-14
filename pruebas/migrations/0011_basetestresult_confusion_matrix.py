# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pruebas', '0010_frameannotation_raw_scoring'),
    ]

    operations = [
        migrations.AddField(
            model_name='basetestresult',
            name='confusion_matrix',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
