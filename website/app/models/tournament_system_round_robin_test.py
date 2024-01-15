import unittest
from django.test import TestCase
from unittest.mock import patch, Mock
from .tournament_system_round_robin import TournamentSystemRoundRobin

class TestTournamentSystemRoundRobin(TestCase):
    @patch("app.models.tournament")
    def test_init(self, mock_tournament):
        tournament_system_rr = TournamentSystemRoundRobin(mock_tournament)
        self.assertEqual(tournament_system_rr.battle_count, len(tournament_system_rr.tournament.players)*(len(tournament_system_rr.tournament.players)-1)/2)

    @patch("app.models.tournament")
    def test_battles(self, mock_tournament):
        tournament_system_rr = TournamentSystemRoundRobin(mock_tournament)
        tournament_system_rr.run_tournament()
        self.assertEqual(tournament_system_rr.battle_count, 0)

if __name__ == '__main__':
    unittest.main()