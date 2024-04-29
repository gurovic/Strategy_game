import datetime

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django_q.models import Schedule

from .tournament_system_round_robin import TournamentSystemRoundRobin
from .battle import Battle


def _end_registration_task(tournament_id: int):
    tournament = Tournament.objects.get(id=tournament_id)
    if tournament.status == Tournament.Status.WAITING_SOLUTIONS:
        tournament.end_registration()


def _start_tournament_task(tournament_id: int):
    tournament = Tournament.objects.get(id=tournament_id)
    if tournament.status == Tournament.Status.NOT_STARTED:
        tournament.start_tournament()


class Tournament(models.Model):
    class Status(models.IntegerChoices):
        NOT_STARTED = 0
        WAITING_SOLUTIONS = 1
        IN_PROGRESS = 2
        FINISHED = 3

    class System(models.IntegerChoices):
        ROUND_ROBIN = 0

    name = models.CharField(max_length=255, default='tournament', verbose_name='Name')
    game = models.ForeignKey('Game', blank=True, null=True, on_delete=models.CASCADE, verbose_name='Game')
    players = models.ManyToManyField(User, through='PlayerInTournament', blank=True, verbose_name='Players')
    system = models.IntegerField(choices=System.choices, default=System.ROUND_ROBIN, verbose_name='Tournament System')
    status = models.IntegerField(choices=Status.choices, default=Status.NOT_STARTED, verbose_name='Status')
    finish_registration_time = models.DateTimeField(default=timezone.now, null=True, blank=True, verbose_name='Finish Registration Time')
    tournament_start_time = models.DateTimeField(default=timezone.now, null=True, blank=True, verbose_name='Tournament Start Time')
    battles = models.ManyToManyField(Battle, blank=True, verbose_name='Battle')
    max_of_players = models.IntegerField(default=2, verbose_name='Maximum number of players')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.status == self.Status.WAITING_SOLUTIONS:
            Schedule.objects.update_or_create(name=f"End registration {self.id}", func="app.models.tournament._end_registration_task",
                                              repeats=1, args=str(self.id),
                                              defaults=dict(next_run=self.finish_registration_time))

        if self.status == self.Status.NOT_STARTED:
            Schedule.objects.update_or_create(name=f"Start tournament {self.id}", func='app.models.tournament._start_tournament_task',
                                              repeats=1, args=str(self.id),
                                              defaults=dict(next_run=self.tournament_start_time))

        return super().save(*args, **kwargs)

    def start_tournament(self):
        self.status = self.Status.WAITING_SOLUTIONS
        self.save()

    def end_registration(self):
        self.status = self.Status.IN_PROGRESS
        self.save()
        match self.system:
            case self.System.ROUND_ROBIN:
                tournament_system = TournamentSystemRoundRobin(self)
                tournament_system.run_tournament()
            case _:
                pass

    def finish_tournament(self):
        self.status = self.Status.FINISHED
        self.save()
