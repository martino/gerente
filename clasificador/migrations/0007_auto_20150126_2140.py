# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('clasificador', '0006_auto_20150121_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classifiermodel',
            name='json_model',
            field=django_extensions.db.fields.json.JSONField(),
            preserve_default=True,
        ),
    ]
