import random
import time
from typing import Any
from unittest.mock import Mock, patch, PropertyMock
from django.test import TestCase

from app.classes.sandbox import Sandbox


class SandboxTest(TestCase):
    @patch("app.classes.sandbox.Battle")
    @patch("app.classes.sandbox.PlayersInBattle")
    def test_create(self, mock_battle: Mock, mock_players_in_battle: Mock):
        class GameMock(Mock):
            def __init__(self, **kwargs: Any):
                super().__init__(**kwargs)
                self.number_of_players = 2

        a = Sandbox(GameMock(), None, None)
        self.assertEqual(mock_battle.call_count, 2)
        self.assertEqual(mock_players_in_battle.call_count, 1)
        # self.assertEqual(mock_game.call_count, 3)
        self.assertEqual(a.strategy, None)

    @patch("app.classes.sandbox.Battle")
    @patch("app.classes.sandbox.PlayersInBattle")
    def test_running(self, mock_battle: Mock, mock_players_in_battle: Mock):
        class GameMock(Mock):
            def __init__(self, **kwargs: Any):
                super().__init__(**kwargs)
                self.number_of_players = 2

        class BattleMock(Mock):
            def __init__(self, **kwargs: Any):
                super().__init__(**kwargs)
                self.count_battle = 0

            def run(self):
                self.count_battle += 1

        a = Sandbox(GameMock(), None, None)
        a.battle = BattleMock()
        a.run_battle()
        self.assertEqual(a.battle.count_battle, 1)

    @patch("app.classes.sandbox.Battle")
    @patch("app.classes.sandbox.PlayersInBattle")
    def test_notify(self, mock_battle: Mock, mock_players_in_battle: Mock):
        class GameMock(Mock):
            def __init__(self, **kwargs: Any):
                super().__init__(**kwargs)
                self.number_of_players = 2

        def notify(report):
            self.assertEqual(report, 1234567890)

        a = Sandbox(GameMock(), None, notify)
        a.notify(1234567890)
        self.assertEqual(a.report, 1234567890)

    @patch("app.classes.sandbox.Battle")
    @patch("app.classes.sandbox.PlayersInBattle")
    def test_run_and_notify(self, mock_battle: Mock, mock_players_in_battle: Mock):
        random_number = random.randint(1, 1000000000)

        class GameMock(Mock):
            def __init__(self, **kwargs: Any):
                super().__init__(**kwargs)
                self.number_of_players = 2

        class BattleMock(Mock):
            def __init__(self, creator, **kwargs: Any):
                super().__init__(**kwargs)
                self.battle_count = 0
                self.creator = creator
                self.report = random_number

            def run(self):
                self.battle_count += 1
                return self.creator.notify(self.report)

        class ToNotify:
            def __init__(self):
                self.notify_count = 0
                self.report = None

            def notify(self, report):
                self.notify_count = 1
                self.report = report

        report_getter = ToNotify()
        a = Sandbox(GameMock(), None, report_getter.notify)
        a.battle = BattleMock(a)
        a.run_battle()
        self.assertEqual(a.battle.battle_count, 1)
        self.assertEqual(a.battle.creator, a)

        time_start = time.time()
        while report_getter.report is None:
            if (time.time() - time_start) > 1:
                break

        self.assertEqual(report_getter.notify_count, 1)
        self.assertEqual(report_getter.report, random_number)
