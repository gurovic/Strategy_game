from ..classes.jury import GameState
from ..models import PlayersInBattle
from django.db import models
from django.contrib.auth.models import User
from .game import Game
from .jury_report import JuryReport


class Battle(models.Model):
    class GameStateChoices(models.TextChoices):
        N = "NOT_STARTED"
        O = "OK"
        E = "ERROR"

    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    time_start = models.DateTimeField(auto_now_add=True)
    time_finish = models.DateTimeField(auto_now_add=True)
    players = models.ManyToManyField(User, through='PlayersInBattle', blank=True)
    status = models.TextField(choices=GameStateChoices.choices, default=GameStateChoices.N)
    logs = models.FileField(blank=True)
    jury_report = models.ForeignKey(JuryReport, on_delete=models.CASCADE)

    def __init__(self, jury, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.moves = []
        self.results = {}
        self.jury = jury
        self.numbers = []

    def run(self):
        while self.jury.game_state is not GameState.END:
            self.jury.get_processes()
            self.jury.perform_play_command()

        for player in PlayersInBattle.objects.filter(batlle=self):
            player.number_of_points = self.jury_report.points[player.number]

        self.jury_report.points = dict(reversed(sorted(self.jury_report.points.items(), key=lambda item: item[1])))

        for order, player in enumerate(sorted(self.jury_report.points.keys()), start=1):
            self.results[player] = order
        self.moves = self.jury_report.story_of_game
        self.status = self.jury_report.status
