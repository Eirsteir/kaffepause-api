# Generated by Django 3.0.10 on 2020-11-15 09:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breaks', '0006_auto_20201115_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='break',
            name='start_time',
            field=models.TimeField(default=datetime.datetime(2020, 11, 15, 10, 40, 17, 693752)),
        ),
        migrations.AlterField(
            model_name='breakinvitation',
            name='expiry',
            field=models.TimeField(default=datetime.datetime(2020, 11, 15, 13, 10, 17, 695542)),
        ),
    ]
