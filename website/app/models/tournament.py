from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from .model_battle import Battle
from .game import Game
#from .model_tournament_system import TournamentSystem


class Tournament(models.Model):
    class Status(models.IntegerChoices):
        NOT_STARTED = 0
        WAITING_SOLUTIONS = 1
        IN_PROGRESS = 2
        FINISHED = 3

    name = models.CharField(max_length=255, default='tournament', verbose_name='Name')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Game')
    players = models.ManyToManyField(User, through='PlayerInTournament', null=True, blank=True, verbose_name='Players')
    #system = models.ForeignKey(TournamentSystem, on_delete=models.CASCADE, null=False, blank=False, verbose_name='Tournament System')
    start_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Start Time')
    end_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Finish time')
    status = models.IntegerField(choices=Status.choices, default=Status.NOT_STARTED, verbose_name='Status')
    battles = models.ManyToManyField(Battle, blank=True, verbose_name='Battle')
    max_of_players = models.IntegerField(default=2, verbose_name='Maximum number of players')

    def start(self):
        self.status = self.Status.WAITING_SOLUTIONS

    def notify(self):
        self.status = self.Status.FINISHED

    def end(self):
        self.status = self.Status.IN_PROGRESS
        self.system.run_tournament()
