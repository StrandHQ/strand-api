# Generated by Django 2.0.1 on 2018-01-11 01:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0002_auto_20180111_0108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='time_start',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 11, 1, 46, 43, 772158, tzinfo=utc)),
        ),
    ]
