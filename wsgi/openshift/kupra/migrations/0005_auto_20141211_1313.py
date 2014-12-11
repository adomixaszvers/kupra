# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid_upload_path.storage


class Migration(migrations.Migration):

    dependencies = [
        ('kupra', '0004_auto_20141211_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='img',
            field=models.ImageField(default=b'default.jpg', upload_to=uuid_upload_path.storage.upload_to),
            preserve_default=True,
        ),
    ]
