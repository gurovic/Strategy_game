import os.path
import typing

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from website.settings import MEDIA_ROOT
from .jury_report import JuryReport
from ..classes.jury import GameState, Jury
from ..compiler import Compiler
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
        global ok_sum
        ok_sum = 0

        class CompiledFile:
            ok_sum = 0

            def get_compiled_file(self, compiler_report):
                self.compiled_file = compiler_report.compiled_file
                global ok_sum
                ok_sum += 1

        file = os.path.join(MEDIA_ROOT, str(self.game.play.path))
        list_compiled_file = []
        if file.split(".")[-1][0] != 'e':
            play_compiled = CompiledFile()
            list_compiled_file.append(play_compiled)
            Compiler(file, file.split(".")[-1], play_compiled.get_compiled_file).compile()
            file = os.path.join(MEDIA_ROOT, str(play_compiled.compiled_file))

        players_in_battle = PlayersInBattle.objects.filter(battle=self)

        launcher = Launcher(os.path.abspath(str(file)), params=[players_in_battle.count()], label="play")
        requests.append(launcher)

        number = 0
        files_list = []
        for player_in_battle in players_in_battle:
            number += 1
            self.numbers[number] = player_in_battle.player
            file = player_in_battle.file_solution.path
            if file.split(".")[-1][0] != 'e':
                strategy_compiled = CompiledFile()
                Compiler(file, file.split(".")[-1], strategy_compiled.get_compiled_file).compile()
                list_compiled_file.append(strategy_compiled)
                file = os.path.join(MEDIA_ROOT, str(strategy_compiled.compiled_file))

            files_list.append(file)

        while ok_sum != len(list_compiled_file):
            continue

        number = 1
        for file in files_list:
            launcher = Launcher(file, label=f'player{number}')
            requests.append(launcher)
            number += 1

        multi_request = InvokerMultiRequest(requests, priority=Priority.RED)
        self.jury = Jury(multi_request)
        multi_request.subscribe(self.jury)
        multi_request.start()

    def run(self, callback: typing.Optional[typing.Callable[[JuryReport], None]] = None):
        self.create_invoker_requests()
        jury = self.jury

        jury.get_processes()
        jury.perform_play_command()

        self.jury_report = jury.jury_report

        points = self.jury_report.points

        for player in PlayersInBattle.objects.filter(battle=self):
            player.number_of_points = points.get(player.number, 0)

        for order, player in enumerate(points, start=1):
            self.results[player] = order
        self.moves = self.jury_report.story_of_game
        self.status = self.jury_report.status

        self.save()

        if callback:
            callback(self.jury_report)
