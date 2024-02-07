import unittest
from unittest.mock import Mock
from .tournamentsystem import TournamentSystem


class TestTournamentSystem(unittest.TestCase):
    def test_init(self):
        class MockTournament:
            count = 0
            def finish_tournament(self):
                self.count += 1

        mock_tournament = MockTournament()
        tournament_system = TournamentSystem(mock_tournament)
        self.assertIs(tournament_system.tournament, mock_tournament)

    def test_finish(self):
        class MockTournament:
            count = 0
            def finish_tournament(self):
                self.count += 1

        mock_tournament = MockTournament()
        tournament_system = TournamentSystem(mock_tournament)
        tournament_system.finish()
        self.assertEqual(mock_tournament.count, 1)


if __name__ == '__main__':
    unittest.main()
