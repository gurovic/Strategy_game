# Generated by Django 4.2.10 on 2024-02-11 18:53

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournamentsystemroundrobin',
            name='tournamentsystem_ptr',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='start_time',
        ),
        migrations.AddField(
            model_name='tournament',
            name='finish_registration_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 2, 11, 18, 53, 50, 688472, tzinfo=datetime.timezone.utc), null=True, verbose_name='Finish Registration Time'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='tournament_start_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 2, 11, 18, 53, 50, 688472, tzinfo=datetime.timezone.utc), null=True, verbose_name='Tournament Start Time'),
        ),
        migrations.AlterField(
            model_name='battle',
            name='total_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2024, 2, 11, 18, 53, 50, 663938, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='players',
            field=models.ManyToManyField(blank=True, through='app.PlayerInTournament', to=settings.AUTH_USER_MODEL, verbose_name='Players'),
        ),
        migrations.DeleteModel(
            name='TournamentSystem',
        ),
        migrations.DeleteModel(
            name='TournamentSystemRoundRobin',
        ),
    ]