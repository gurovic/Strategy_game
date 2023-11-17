import unittest
import datetime

from django.test import TestCase

from threading import Lock, Thread

from strategy_game.website.app.classes.file_loader import FileLoader
from ..models import CompilerReport


class TestSingleton(TestCase):
    def test_creating(self):
        a = FileLoader('strategy_game/test_solutions/draught.cpp')
        self.assertGreater(1000000000000000001, a.id)
        self.assertEqual(a.file_path, 'strategy_game/test_solutions/draught.cpp')
        self.assertEqual(a.lang, '.cpp')
        self.assertEqual(a.compiler_report, None)

    def test_non_existing_file(self):
        a = FileLoader('strategy_game/test_solutions/a.cpp')
        self.assertEqual(a.compiler_report.status, "ERROR")

    def test_notify(self):
        a = FileLoader('strategy_game/test_solutions/draughts.cpp')
        report = CompilerReport(None, 0, datetime.datetime.now().strftime("%Y%m%d"), "ERROR",
                                "No such file found {}".format("strategy_game/test_solutions/draughts.cpp"), None)
        a.notify(CompilerReport())
        self.assertEqual(a.compiler_report, report)

