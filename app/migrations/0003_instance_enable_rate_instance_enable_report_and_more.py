# Generated by Django 4.1.1 on 2022-10-13 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_instance_rp'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='enable_rate',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='instance',
            name='enable_report',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='instance',
            name='score',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='instance',
            name='score_computed',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='instance',
            name='socials',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='SafeVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta', models.JSONField(blank=True, null=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('db_status', models.IntegerField(choices=[(-1, 'Deleted'), (0, 'Pending'), (1, 'Active')], default=1)),
                ('is_safe', models.BooleanField(default=False)),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='safe_votes', to='app.instance')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='safe_votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('instance', 'user')},
            },
        ),
    ]