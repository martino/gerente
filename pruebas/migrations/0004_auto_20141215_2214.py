# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pruebas', '0003_auto_20141208_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basetestresult',
            name='model_version',
            field=models.ForeignKey(related_name='test', to='clasificador.ClassifierModel'),
            preserve_default=True,
        ),
    ]
