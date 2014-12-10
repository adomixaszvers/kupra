# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid_upload_path.storage


class Migration(migrations.Migration):

    dependencies = [
        ('kupra', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='img',
            field=models.ImageField(default=b'default.jpg', null=True, upload_to=uuid_upload_path.storage.upload_to),
            preserve_default=True,
        ),
    ]
