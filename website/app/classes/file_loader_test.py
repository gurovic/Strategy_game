import unittest
import datetime

from threading import Lock, Thread

from Strategy_game.website.app.classes.file_loader import FileLoader
from ..models import CompilerReport


class TestSingleton(unittest.TestCase):
    def test_creating(self):
        a = FileLoader('Strategy_game/test_solutions/draught.cpp')
        self.assertGreater(1000000000000000001, a.id)
        self.assertEqual(a.file_path, 'Strategy_game/test_solutions/draught.cpp')
        self.assertEqual(a.lang, '.cpp')
        self.assertEqual(a.compiler_report, None)

    def test_non_existing_file(self):
        a = FileLoader('Strategy_game/test_solutions/a.cpp')
        self.assertEqual(a.compiler_report.status, "ERROR")

    def test_notify(self):
        a = FileLoader('Strategy_game/test_solutions/draughts.cpp')
        report = CompilerReport(None, 0, datetime.datetime.now().strftime("%Y%m%d"), "ERROR",
                                "No such file found {}".format("Strategy_game/test_solutions/draughts.cpp"), None)
        a.notify(CompilerReport())
        self.assertEqual(a.compiler_report, report)


if __name__ == '__main__':
    unittest.main()
