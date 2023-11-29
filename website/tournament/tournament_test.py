import unittest
from unittest.mock import Mock
from datetime import datetime
from tournament import Tournament

class TestTournament(unittest.TestCase):
    def setUp(self):
        self.tournament_name = "TestTournament"
        self.game = "Chess"
        self.players = ["Player1", "Player2", "Player3"]
        self.system = Mock()
        self.start_time = datetime.now()
        self.end_time = datetime.now()
        self.tournament = Tournament(self.tournament_name, self.game, self.players, self.system, self.start_time, self.end_time)

    def test_tournament_initialization(self):
        self.assertEqual(self.tournament.name, self.tournament_name)
        self.assertEqual(self.tournament.game, self.game)
        self.assertEqual(self.tournament.players, self.players)
        self.assertEqual(self.tournament.system, self.system)
        self.assertEqual(self.tournament.start_time, self.start_time)
        self.assertEqual(self.tournament.end_time, self.end_time)
        self.assertFalse(self.tournament.running_results_status)

    def test_start_tournament(self):
        self.tournament.start()

        self.assertTrue(self.tournament.running_results_status)
        self.system.run_tournament.assert_called_once_with(self.tournament)
        self.system.calculate_places.assert_called_once_with(self.system.run_tournament.return_value, self.tournament.players)

    def test_end_tournament(self):
        self.tournament.running_results_status = True
        self.tournament.end()
        self.assertFalse(self.tournament.running_results_status)

