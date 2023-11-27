import unittest
from unittest.mock import Mock, patch
from tournamentsystem import TournamentSystem
from tournament.tournament import Tournament


class TestTournamentSystem(unittest.TestCase):
    @patch("tournament.tournament.Tournament")
    def test_init(self):
        b = Tournament
        a = TournamentSystem(b)
        self.assertIs(a.tournament, b)
        self.assertListEqual([], a.battles)

    def test_notify(self):
        mock = Mock()
        a = TournamentSystem(mock)
        a.notify()
        mock.assert_called()


if __name__ == '__main__':
    unittest.main()
