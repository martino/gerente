# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pruebas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basetestresult',
            name='macro_f1',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basetestresult',
            name='macro_precision',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basetestresult',
            name='macro_recall',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basetestresult',
            name='micro_f1',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basetestresult',
            name='micro_precision',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basetestresult',
            name='micro_recall',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
