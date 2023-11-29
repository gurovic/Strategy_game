from django.db import models
from django.contrib.auth.models import User
from .model_game import Game
from .model_battle import Battle, PlayersInBattles


class Tournament(models.Model):
    name = models.CharField(max_length=255, default='tournament')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    players = models.ManyToManyField(User, through='PlayersInTournament')
    system = models.CharField()
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    running_results_status = models.CharField(max_length=1, choices=[("N", "Not started"), ("I", "In processing"), ("F", "Finished")], default="N")


class PlayersInTournament(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    strategy = models.FilePathField(null=True)
    place = models.PositiveIntegerField()
    number_of_wins = models.PositiveIntegerField(default=0)
    number_of_points = models.PositiveIntegerField(default=0)
