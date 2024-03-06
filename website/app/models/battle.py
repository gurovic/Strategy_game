from django.db import models
from django.contrib.auth.models import User
from .jury_report import JuryReport
from ..classes.jury import GameState
from ..models import PlayersInBattle

class Battle(models.Model):
    class GameStateChoices(models.TextChoices):
        NS = "NOT_STARTED"
        OK = "OK"
        ER = "ERROR"

    game = models.ForeignKey('Game', on_delete=models.CASCADE, null=True)
    time_start = models.DateTimeField(auto_now_add=True)
    time_finish = models.DateTimeField(auto_now_add=True)
    players = models.ManyToManyField(User, through='PlayersInBattle', blank=True)
    status = models.TextField(choices=GameStateChoices.choices, default=GameStateChoices.NS)
    logs = models.FileField(blank=True)
    jury_report = models.ForeignKey(JuryReport, blank=True, null=True, on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.moves = []
        self.results = {}
        self.numbers = {}

    def run(self, jury):
        while jury.game_state is not GameState.END:
            jury.get_processes()
            jury.perform_play_command()

        points = self.jury_report.points
        points = dict(points.items())

        for player in self.players.all():
            player.number_of_points = points[player.number]

        for order, player in enumerate(points, start=1):
            self.results[player] = order
        self.moves = self.jury_report.story_of_game
        self.status = self.jury_report.status
