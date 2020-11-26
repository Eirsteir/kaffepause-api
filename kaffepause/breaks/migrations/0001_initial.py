# Generated by Django 3.0.10 on 2020-11-26 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import kaffepause.common.utils
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Break',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('start_time', models.DateTimeField(default=kaffepause.common.utils.thirty_minutes_from_now)),
                ('participants', models.ManyToManyField(related_name='breaks', related_query_name='break', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BreakInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('message', models.CharField(blank=True, max_length=75, null=True)),
                ('is_seen', models.BooleanField(default=False)),
                ('reply', models.CharField(blank=True, choices=[('accepted', 'Accepted'), ('declined', 'Declined'), ('ignored', 'Ignored')], max_length=10, null=True)),
                ('expiry', models.DateTimeField(default=kaffepause.common.utils.three_hours_from_now)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='break_invites', related_query_name='break_invitation', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_invites', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='breaks.Break')),
            ],
            options={
                'verbose_name': 'Break invitation',
                'verbose_name_plural': 'Break invitations',
                'ordering': ('-created', 'is_seen'),
            },
        ),
        migrations.CreateModel(
            name='BreakHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='previous_breaks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Break history',
                'verbose_name_plural': 'Break histories',
            },
        ),
        migrations.AddConstraint(
            model_name='breakinvitation',
            constraint=models.UniqueConstraint(fields=('sender', 'recipient', 'subject'), name='unique-invitation'),
        ),
    ]
