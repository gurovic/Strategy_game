from django.db import models
from django.contrib.auth.models import User
from app.models import Battle


class PlayersInBattle(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, verbose_name='Игрок')
    number = models.IntegerField(default=0, unique=True, verbose_name='Номер в батле')
    battle = models.ForeignKey(Battle, null=True, default=None, on_delete=models.CASCADE, verbose_name='Battle')
