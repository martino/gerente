# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0001_initial'),
        ('pruebas', '0002_auto_20141208_2214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentannotation',
            name='document_part',
        ),
        migrations.AddField(
            model_name='documentannotation',
            name='document',
            field=models.ForeignKey(to='documentos.BaseDocument', null=True),
            preserve_default=True,
        ),
    ]
