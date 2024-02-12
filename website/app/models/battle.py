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
    jury_report = models.ForeignKey(JuryReport, blank=True, null=True, on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.moves = []
        self.results = {}
        self.numbers = []

    def run(self, jury):
        while jury.game_state is not GameState.END:
            jury.get_processes()
            jury.perform_play_command()

        for player in PlayersInBattle.objects.filter(battle=self):
            player.number_of_points = Battle.objects.get(battle=self).points[player.number]

        points = JuryReport.objects.get(battle=self).points
        points = dict(reversed(sorted(points.items(), key=lambda item: item[1])))

        for order, player in enumerate(sorted(points), start=1):
            self.results[player] = order
        self.moves = JuryReport.objects.get(battle=self).story_of_game
        self.status = JuryReport.objects.get(battle=self).status
