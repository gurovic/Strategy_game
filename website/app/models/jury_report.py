from django.db import models


class JuryReport(models.Model):
    story_of_game = models.Field(editable=False, blank=True, null=True, verbose_name="Ход игры")
    points = models.JSONField(editable=False, blank=True, null=True, verbose_name="Очки игроков")
    status = models.IntegerField(editable=False, blank=True, null=True, verbose_name="Статус боя")