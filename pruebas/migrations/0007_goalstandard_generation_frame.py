# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pruebas', '0006_auto_20150106_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='goalstandard',
            name='generation_frame',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
