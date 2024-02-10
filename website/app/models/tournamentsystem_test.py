import unittest
from unittest.mock import Mock, patch

from django.contrib.auth.models import User

from .tournamentsystem import TournamentSystem
from django.db import models


class TestTournamentSystem(unittest.TestCase):
    @patch('app.models.tournamentsystem.TournamentSystem')
    def test_init(self, mock_players_in_tournament):
        mock_players_in_tournament.return_value = Mock()

        class MockTournament(models.Model):
            count = 0

            def finish_tournament(self):
                self.count += 1

        mock_tournament = MockTournament()
        tournament_system = TournamentSystem(mock_tournament)
        self.assertIs(tournament_system.tournament, mock_tournament)

    def test_finish(self):
        class MockTournament:
            count = 0
            players = []

            def finish_tournament(self):
                self.count += 1

        mock_tournament = MockTournament()
        tournament_system = TournamentSystem(mock_tournament)
        tournament_system.finish()
        self.assertEqual(mock_tournament.count, 1)


if __name__ == '__main__':
    unittest.main()
