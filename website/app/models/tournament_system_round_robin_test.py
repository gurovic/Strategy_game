import unittest
from unittest.mock import Mock
from website.app.models.tournament_system_round_robin import TournamentSystemRoundRobin
class TestTournamentSystemRoundRobin(unittest.TestCase):
    def test_init(self):
        mock_tournament = Mock()
        self.tournament_system_rr = TournamentSystemRoundRobin(mock_tournament)
        self.assertEqual(self.tournament_system_rr.battle_count, len(self.tournament_system_rr.tournament.players)*(len(self.tournament_system_rr.tournament.players)-1)/2)

    def test_battles(self):
        self.assertEqual(len(self.tournament_system_rr.ongoing_battles),0);

if __name__ == '__main__':
    unittest.main()