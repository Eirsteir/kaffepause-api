# Generated by Django 3.0.10 on 2020-11-25 08:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('checkins', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkin',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='check_ins', to=settings.AUTH_USER_MODEL, verbose_name='check-ins'),
        ),
    ]
