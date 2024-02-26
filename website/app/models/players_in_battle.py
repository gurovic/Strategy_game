from django.contrib.auth.models import User
from django.db import models

from django.contrib.auth.models import User


class PlayersInBattle(models.Model):
    battle = models.ForeignKey("Battle", on_delete=models.CASCADE)
    player = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)
    number = models.IntegerField(default=0, verbose_name='Номер в батле')
    number_of_points = models.IntegerField(default=0, verbose_name='number of point')
    place = models.IntegerField(default=0, verbose_name='place')
    file_solution = models.FileField(upload_to='player_in_battle_files', null=True, verbose_name='file')
