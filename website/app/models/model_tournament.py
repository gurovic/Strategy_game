from django.db import models
from django.contrib.auth.models import User
from .model_game import Game
from .model_tournament_system import TournamentSystem
from .model_battle import Battle, PlayersInBattles


class Tournament(models.Model):
    class Status(models.IntegerChoices):
        NOT_STARTED = 0
        IN_PROCESSING= 1
        FINISHED = 2

    name = models.CharField(max_length=255, default='tournament')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    players = models.ManyToManyField(User, through='PlayerInTournament', null=True)
    system = models.ForeignKey(TournamentSystem, on_delete=models.CASCADE, null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    running_results_status = models.IntegerField(choices=Status.choices, default=Status.NOT_STARTED)


class PlayerInTournament(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    strategy = models.FilePathField(null=True)
    place = models.PositiveIntegerField()
    number_of_wins = models.PositiveIntegerField(default=0)
    number_of_points = models.PositiveIntegerField(default=0)
