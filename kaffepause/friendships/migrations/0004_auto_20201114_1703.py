# Generated by Django 3.0.10 on 2020-11-14 16:03

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('friendships', '0003_auto_20201110_2059'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='friendshipstatus',
            options={'verbose_name': 'Friendship status', 'verbose_name_plural': 'Friendship statuses'},
        ),
        migrations.AddField(
            model_name='friendshipstatus',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='friendshipstatus',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='friendshipstatus',
            name='slug',
            field=models.CharField(max_length=100, verbose_name='slug'),
        ),
    ]