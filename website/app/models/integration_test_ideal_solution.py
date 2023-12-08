from django.test import TestCase
from .file_loader import FileLoader
from .file import File
from .battle import Battle
from .game import Game
from .players_in_battle import PlayersInBattle


class IntegrationTest(TestCase):
    def test_upload(self):
        file = File()
        report = FileLoader(file)
        TestCase.assertEqual(report.compiler_report.status, "OK", "Failed upload")

    def test_creating_battle(self):
        game = Game()
        players = PlayersInBattle()
        battle = Battle(game, players)
        TestCase.assertEqual(battle.game, game, "Failed creating: different game types")
        TestCase.assertEqual(battle.players, players, "Failed: different players' lists")

    def test_run(self):
        game = Game()
        players = PlayersInBattle()
        battle = Battle(game, players)
        battle.run()
        TestCase.assertEqual(battle.report, "OK", "Failed running")

    def test_create_response(self):
        pass

    def test_response_in_views(self):
        pass
