import datetime

from django.db import models
from django.contrib.auth.models import User
from django_q.models import Schedule
from django_q.tasks import schedule

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
    players = models.ManyToManyField(User, through='PlayerInTournament', blank=True, verbose_name='Players')
    system = models.IntegerField(choices=System.choices, default=System.ROUND_ROBIN, verbose_name='Tournament System')
    status = models.IntegerField(choices=Status.choices, default=Status.NOT_STARTED, verbose_name='Status')
    battles = models.ManyToManyField(Battle, blank=True, verbose_name='Battle')
    max_of_players = models.IntegerField(default=2, verbose_name='Maximum number of players')

    def start_tournament(self):
        print('!!!!!!!!! TOURNAMENT STARTED CORRECTLY !!!!!!!')
        self.status = self.Status.WAITING_SOLUTIONS
        self.save()

    def finish_tournament(self):
        self.status = self.Status.FINISHED
        self.save()

    def end_registration(self):
        print('!!!!!!!!! TOURNAMENT ENDING REGISTRATION 1 !!!!!!!!!')
        self.status = self.Status.IN_PROGRESS
        self.save()
        tournament_system = None
        if self.system == self.System.ROUND_ROBIN:
            tournament_system = TournamentSystemRoundRobin(self)
        tournament_system.run_tournament()
        print('!!!!!!!!! TOURNAMENT ENDING REGISTRATION 2 !!!!!!!!!')
