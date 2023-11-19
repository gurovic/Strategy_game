import datetime
import asyncio

from django.test import TestCase

from .file_loader import FileLoader
from ..models import CompilerReport, PlayersInBattle, Game
from invoker.models import InvokerReport
from .battle import Battle
from .generate_battle import *


class TestFileLoader(TestCase):
    def test_creating(self):
        a = FileLoader('strategy_game/test_solutions/draughts.cpp')
        self.assertGreater(1000000000000000001, a.id)
        self.assertEqual(a.file_path, 'strategy_game/test_solutions/draughts.cpp')
        self.assertEqual(a.lang, 'cpp')
        self.assertEqual(a.compiler_report, None)

    def test_non_existing_file(self):
        a = FileLoader('strategy_game/test_solutions/a.cpp')
        self.assertEqual(a.compiler_report.status, 2)

    def test_notify(self):
        a = FileLoader('strategy_game/test_solutions/draughts.cpp')
        report = CompilerReport(
            compiled_file=None,
            time=0,
            status=2,
            error="No such file found {}".format('strategy_game/test_solutions/draughts.cpp'),
            invoker_report=None)
        a.notify(report)
        self.assertEqual(a.compiler_report, report)


class BattleTest(TestCase):
    def test_creating(self):
        game = Game()
        players = [PlayersInBattle()]
        a = Battle(game, players)
        self.assertEqual(a.game, game)
        self.assertEqual(a.players, players)
        self.assertEqual(a.status, False)
        self.assertEqual(a.moves, [])
        self.assertEqual(a.report, None)

    def test_running(self):
        game = Game()
        players = [PlayersInBattle()]
        a = Battle(game, players)
        a.run()
        new_invoker_report = InvokerReport(time=datetime.datetime.now(), status=1)
        a.notify(new_invoker_report)
        report = a.get_report()
        self.assertEqual(report, new_invoker_report)
        self.assertEqual(a.status, True)

    def test_get_report(self):
        game = Game()
        players = [PlayersInBattle()]
        a = Battle(game, players)
        new_invoker_report = InvokerReport(time=datetime.datetime.now(), status=1)
        a.notify(new_invoker_report)
        report = a.get_report()
        self.assertEqual(report, new_invoker_report)


class GenerateBattleTest(TestCase):
    def test_save_file(self):
        with open('strategy_game/test_solutions/draughts.cpp', 'r') as new_file:
            file = new_file.read()
        filename = save_file(file)
        self.assertEqual(type(filename), str)
        with open(filename, 'r') as file2:
            new_file = file2.read()
        self.assertEqual(new_file, file)

    def test_generate_filename(self):
        filename = generate_filename('cpp')
        self.assertEqual(type(filename), str)
        self.assertEqual(filename[:43], "strategy_game/test_solution/generated/file_")
        self.assertEqual(filename[-3:],'cpp')

    def test_generate_battle(self):
        pass