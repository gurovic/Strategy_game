from django.db import models


class PlayerInBattle(models.Model):
    path = models.TextField(editable=False, blank=True, null=True, verbose_name="Путь к файлу")
    strategy_id = models.IntegerField(default=0, verbose_name="id стратегии в Battle")
    is_winner = models.BooleanField(default=False, verbose_name="Победитель")
