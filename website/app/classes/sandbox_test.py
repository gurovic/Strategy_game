import random
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

        a = Sandbox(GameMock(), None)
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

        a = Sandbox(GameMock(), None)
        a.battle = BattleMock()
        a.run_battle()
        self.assertEqual(a.battle.count_battle, 1)

    @patch("app.classes.sandbox.Battle")
    @patch("app.classes.sandbox.PlayersInBattle")
    def test_get_result(self, mock_battle: Mock, mock_players_in_battle: Mock):
        global random_number
        random_number = random.randint(1, 1000000000)

        class GameMock(Mock):
            def __init__(self, **kwargs: Any):
                super().__init__(**kwargs)
                self.number_of_players = 2

        class BattleMock(Mock):
            def __init(self, **kwargs: Any):
                super().__init__(**kwargs)
                self.report = random_number

            def get_report(self):
                return self.report

        a = Sandbox(GameMock(), None)
        a.battle = BattleMock()
        report = a.get_report()
        self.assertEqual(report, random_number)
