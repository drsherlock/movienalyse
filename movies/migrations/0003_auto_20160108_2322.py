# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20160108_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='trailers',
            field=models.TextField(null=True, blank=True),
        ),
    ]
