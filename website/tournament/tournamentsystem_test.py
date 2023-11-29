import unittest
from unittest.mock import Mock, patch
from tournamentsystem import TournamentSystem
from tournament import Tournament


class TestTournamentSystem(unittest.TestCase):
    def test_init(self):
        mock_tournament = Mock()
        tournament_system = TournamentSystem(mock_tournament)
        self.assertIs(tournament_system.tournament, mock_tournament)
        self.assertListEqual([], tournament_system.battles)

    def test_finish(self):
        mock_tournament = Mock()
        tournament_system = TournamentSystem(mock_tournament)
        tournament_system.finish()
        tournament_system.tournament.end.assert_called()


if __name__ == '__main__':
    unittest.main()
