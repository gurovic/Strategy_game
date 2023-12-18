from django.db import models


class PlayersInBattle(models.Model):
    user = models.ForeignKey('app.User', on_delete=models.CASCADE, verbose_name='Игрок')
    number = models.IntegerField(default=0, unique=True, verbose_name='Номер в батле')
