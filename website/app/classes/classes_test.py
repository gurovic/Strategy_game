import datetime

from django.test import TestCase


from .file_loader import FileLoader
from ..models import CompilerReport,PlayersInBattle,Game
from invoker.models import InvokerReport
from .battle import Battle


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
        pass

    def test_running(self):
        pass

    def test_botify(self):
        pass

    def test_get_report(self):
        game = Game.objects.get(pk=0)
        players = PlayersInBattle()
        a = Battle(game, players)
        report = a.get_report()
        a.notify(InvokerReport())
