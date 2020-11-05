# Generated by Django 3.0.10 on 2020-11-05 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friendships', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relationshipstatus',
            name='from_slug',
            field=models.CharField(help_text="Denote the relationship from the user, i.e. 'requesting'", max_length=100, verbose_name='from slug'),
        ),
        migrations.AlterField(
            model_name='relationshipstatus',
            name='to_slug',
            field=models.CharField(help_text="Denote the relationship to the user, i.e. 'requested'", max_length=100, verbose_name='to slug'),
        ),
    ]
