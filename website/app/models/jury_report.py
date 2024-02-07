from django.db import models


class JuryReport(models.Model):
    story_of_game = models.TextField(editable=False, blank=True, null=True, verbose_name="Ход игры")
    points = models.TextField(editable=False, blank=True, null=True, verbose_name="Очки игроков")
    status = models.TextField(editable=False, blank=True, null=True, verbose_name="Статус боя")