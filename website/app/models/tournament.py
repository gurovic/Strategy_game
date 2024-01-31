from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timezone

from .tournament_system_round_robin import TournamentSystemRoundRobin
from .battle import Battle
from .game import Game


class Tournament(models.Model):
    class Status(models.IntegerChoices):
        NOT_STARTED = 0
        WAITING_SOLUTIONS = 1
        IN_PROGRESS = 2
        FINISHED = 3

    class System(models.IntegerChoices):
        ROUND_ROBIN = 0

    name = models.CharField(max_length=255, default='tournament', verbose_name='Name')
    game = models.ForeignKey(Game, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Game')
    players = models.ManyToManyField(User, through='PlayerInTournament', null=True, blank=True, verbose_name='Players')
    system = models.IntegerField(choices=System.choices, default=System.ROUND_ROBIN, verbose_name='Tournament System')
    start_time = models.DateTimeField(blank=True, null=True, verbose_name='Start Time')
    end_time = models.DateTimeField(null=True, verbose_name='Finish time')
    status = models.IntegerField(choices=Status.choices, default=Status.NOT_STARTED, verbose_name='Status')
    battles = models.ManyToManyField(Battle, blank=True, verbose_name='Battle')
    max_of_players = models.IntegerField(default=2, verbose_name='Maximum number of players')

    def start(self):
        self.status = self.Status.WAITING_SOLUTIONS

    def notify(self):
        self.status = self.Status.FINISHED

    def end(self):
        self.status = self.Status.IN_PROGRESS
        tournament_system = None
        if self.system == self.System.ROUND_ROBIN:
            tournament_system = TournamentSystemRoundRobin(self)
        tournament_system.run_tournament()

