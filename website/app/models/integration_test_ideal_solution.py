from django.test import TestCase

from .players_in_battle import PlayersInBattle
from .file_loader import FileLoader
from .file import File
from .battle import Battle
from .game import Game


class IntegrationTest(TestCase):
    def test_upload(self):
        File.objects.create(file=FileDjango(open(__file__, "r"), name="test"), name="test")
        file = File.objects.get(name="test")
        report = FileLoader(file)
        self.assertEqual(report.compiler_report.status, "OK")

    def test_creating_battle(self):
        game = Game(id=1)
        players = []
        ideal_solution_path = "/path/"
        for i in range(game.number_of_players):
            new_player = PlayersInBattle(ideal_solution_path)
            players.append(new_player)
        battle = Battle(game, players)
        self.assertEqual(battle.game, game)
        self.assertEqual(battle.players, players)

    def test_run(self):
        game = Game()
        players = PlayersInBattle()
        battle = Battle(game, players)
        battle.run()
        self.assertEqual(battle.report, "OK")

    def test_create_response(self):
        pass

    def test_response_in_views(self):
        pass
