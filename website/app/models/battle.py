from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from .jury_report import JuryReport
from ..classes.jury import GameState, Jury
from ..launcher import Launcher
from ..models import PlayersInBattle
from invoker.invoker_multi_request import Priority, InvokerMultiRequest
from invoker.invoker_request import InvokerRequest
from invoker.invoker_multi_request_priority_queue import InvokerMultiRequestPriorityQueue


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

    def create_invoker_requests(self):
        requests = []

        file = self.game.play.path
        launcher = Launcher(file)
        request = InvokerRequest(launcher.command(), files=[file], timelimit=settings.LAUNCHER_RUN_TL[launcher.extension], label="play")
        requests.append(request)

        players_in_battle = PlayersInBattle.objects.filter(battle=self)
        number = 0
        for player_in_battle in players_in_battle:
            number += 1
            self.numbers[number] = player_in_battle.player
            file = player_in_battle.file_solution.path
            launcher= Launcher(file)
            request = InvokerRequest(launcher.command(), files=[file], timelimit=settings.LAUNCHER_RUN_TL[launcher.extension], label=f"player{number}")
            requests.append(request)

        multi_request = InvokerMultiRequest(requests, priority=Priority.RED)
        queue = InvokerMultiRequestPriorityQueue()
        queue.add(multi_request)

        self.jury = Jury(multi_request)

    def run(self):
        self.create_invoker_requests()
        jury = self.jury

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
