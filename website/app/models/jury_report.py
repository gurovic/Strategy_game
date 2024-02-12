from django.db import models


class JuryReport(models.Model):
    class Status(models.IntegerChoices):
        OK = 1
        ERROR = 0
    story_of_game = models.TextField(editable=False, blank=True, null=True, verbose_name="Ход игры")
    points = models.JSONField(editable=False, blank=True, null=True, verbose_name="Очки игроков")
    status = models.IntegerField(editable=False, blank=True, null=True, verbose_name="Статус боя", choices=Status.choices)