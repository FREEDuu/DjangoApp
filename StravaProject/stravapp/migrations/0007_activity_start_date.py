# Generated by Django 4.2.18 on 2025-01-15 17:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stravapp', '0006_alter_activity_elapsed_time_alter_activity_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 15, 17, 11, 51, 172556)),
        ),
    ]
