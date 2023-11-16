from django.db import models


class Game(models.Model):
    name = models.TextField(blank=True, null=True, verbose_name="Название game")
    play = models.TextField(blank=True, null=True, verbose_name="Путь к play")
    ideal_solution = models.TextField(blank=True, null=True, verbose_name="Путь к ideal_solution")
    number_of_players = models.IntegerField(default=0, null=True, verbose_name="Кол-во игроков")
