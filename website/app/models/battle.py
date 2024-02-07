from ..classes.jury import GameState
from ..models import PlayersInBattle
from django.db import models
from django.contrib.auth.models import User
from .game import Game


class Battle(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    time_start = models.DateTimeField(auto_now_add=True)
    time_finish = models.DateTimeField(auto_now_add=True)
    players = models.ManyToManyField(User, through='PlayersInBattle', blank=True)
    status = models.CharField(max_length=1,
                              choices=[("O", "OK"), ("E", "Error"), ("T", "Time Limit Exceeded"), ("N", "Not started")],
                              default="N")  # by the rules or by errors
    logs = models.FileField(blank=True)

    def __init__(self, jury, jury_report, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.moves = []
        self.results = {}
        self.jury = jury
        self.jury_report = jury_report
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
