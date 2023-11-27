import unittest
from unittest.mock import Mock, patch
from tournamentsystem import TournamentSystem
from tournament import Tournament


class TestTournamentSystem(unittest.TestCase):
    def test_init(self):
        b = Tournament
        a = TournamentSystem(b)
        self.assertIs(a.tournament, b)
        self.assertListEqual([], a.battles)

    def test_finish(self):
        mock = Mock()
        a = TournamentSystem(mock)
        a.finish()
        a.tournament.end.assert_called()


if __name__ == '__main__':
    unittest.main()
