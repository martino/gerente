# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0004_auto_20150122_2122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentpart',
            name='document',
        ),
        migrations.DeleteModel(
            name='DocumentPart',
        ),
    ]
