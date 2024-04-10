import os.path

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

        def get_compiled_file(compiler_report=None):
            if compiler_report is None:
                play_compiled_file = os.path.join(MEDIA_ROOT, str(self.game.play.path))
            else:
                play_compiled_file = os.path.join(MEDIA_ROOT, str(compiler_report.compiled_file))
                self.game.play = compiler_report.compiled_file

            launcher = Launcher(os.path.abspath(str(play_compiled_file)), label="play")
            requests.append(launcher)
            players_in_battle = PlayersInBattle.objects.filter(battle=self)
            number = 0
            files_list = []

            for player_in_battle in players_in_battle:
                number += 1
                self.numbers[number] = player_in_battle.player
                player_solution_file = player_in_battle.file_solution.path
                if player_solution_file.split(".")[-1][0] != 'e':
                    strategy_compiled = CompiledFile()
                    Compiler(player_solution_file, player_solution_file.split(".")[-1],
                             strategy_compiled.get_compiled_file).compile()
                    list_compiled_file.append(strategy_compiled)
                    player_solution_file = os.path.join(MEDIA_ROOT, str(strategy_compiled.compiled_file))

                files_list.append(player_solution_file)

            while ok_sum != len(list_compiled_file):
                continue

            number = 1
            for compiled_file in files_list:
                launcher = Launcher(compiled_file, label=f'player{number}')
                requests.append(launcher)
                number += 1

            multi_request = InvokerMultiRequest(requests, priority=Priority.RED)
            self.jury = Jury(multi_request)
            multi_request.subscribe(self.jury)
            multi_request.start()

        # <--------- AFTER FUNCTION --------->
        if file.split(".")[-1][0] != 'e':
            Compiler(file, file.split(".")[-1], get_compiled_file).compile()
        else:
            get_compiled_file()

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
