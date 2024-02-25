from django.db import models
from .battle import Battle


class JuryReport(models.Model):
    class Status(models.IntegerChoices):
        OK = 1
        ERROR = 0
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE, null=True)
    story_of_game = models.TextField(blank=True, null=True, verbose_name="Ход игры")
    points = models.JSONField(blank=True, null=True, verbose_name="Очки игроков")
    status = models.IntegerField(blank=True, null=True, verbose_name="Статус боя", choices=Status.choices)