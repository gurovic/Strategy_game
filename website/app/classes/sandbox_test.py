from typing import Any
import random
import time

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

        sandbox = Sandbox(GameMock(), None, None)
        self.assertEqual(mock_battle.call_count, 0)
        self.assertEqual(mock_players_in_battle.call_count, 0)
        self.assertEqual(sandbox.strategy, None)

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

        sandbox = Sandbox(GameMock(), None, None)
        sandbox.battle = BattleMock()
        sandbox.run_battle()
        self.assertEqual(sandbox.battle.count_battle, 0)

    @patch("app.classes.sandbox.Battle")
    @patch("app.classes.sandbox.PlayersInBattle")
    def test_notify(self, mock_battle: Mock, mock_players_in_battle: Mock):
        class GameMock(Mock):
            def __init__(self, **kwargs: Any):
                super().__init__(**kwargs)
                self.number_of_players = 2

        class GetNotify:
            def __init__(self):
                self.report = None

            def notify(self, report):
                self.report = report

        get_notify = GetNotify()
        sandbox = Sandbox(GameMock(), None, get_notify.notify)
        sandbox.notify(1234567890)
        self.assertEqual(get_notify.report, 1234567890)

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

            def start(self):
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
