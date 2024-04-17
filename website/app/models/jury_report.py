from django.db import models


class JuryReport(models.Model):
    class Status(models.IntegerChoices):
        OK = 1
        ERROR = 0
    story_of_game = models.TextField(blank=True, null=True, verbose_name="Ход игры")
    points = models.JSONField(blank=True, null=True, verbose_name="Очки игроков")
    status = models.IntegerField(blank=True, null=True, verbose_name="Статус боя", choices=Status.choices)

    def __str__(self):
        if self.status == self.Status.OK:
            return f"{self.get_status_display()} - {self.points}"
        return self.get_status_display()
