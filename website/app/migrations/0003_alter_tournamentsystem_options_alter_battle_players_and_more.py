# Generated by Django 4.2.9 on 2024-01-03 15:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_alter_tournamentsystem_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tournamentsystem',
            options={},
        ),
        migrations.AlterField(
            model_name='battle',
            name='players',
            field=models.ManyToManyField(through='app.PlayersInBattle', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='PlayersInBattles',
        ),
    ]
