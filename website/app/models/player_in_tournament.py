from django.db import models
from django.contrib.auth.models import User

from app.models.tournament import Tournament


class PlayerInTournament(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='player')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True, blank=True, verbose_name='tournament')
    number_of_points = models.IntegerField(default=0, verbose_name='number of point')
    place = models.IntegerField(default=0, verbose_name='place')
    file_solution = models.FileField(upload_to='player_in_tournament_files', null=True, verbose_name='file')
