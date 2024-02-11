import random
import unittest

from django.contrib.auth.models import User
from django.test import TestCase
from unittest.mock import patch, Mock

from app.models import PlayersInBattle, Tournament, PlayerInTournament
from .tournament_system_round_robin import TournamentSystemRoundRobin


class TestTournamentSystemRoundRobin(TestCase):
    @classmethod
    def setUp(self):
        self.tournament = Tournament.objects.create(name='test1')
        self.user1 = User.objects.create(username='user1', password='<PASSWORD>')
        self.player1 = PlayerInTournament(tournament=self.tournament, player=self.user1)
        self.tournament.players.add(self.user1)
        self.user2 = User.objects.create(username='user2', password='<PASSWORD>')
        self.player2 = PlayerInTournament(tournament=self.tournament, player=self.user2)
        self.tournament.players.add(self.user2)
        self.user3 = User.objects.create(username='user3', password='<PASSWORD>')
        self.player3 = PlayerInTournament(tournament=self.tournament, player=self.user3)
        self.tournament.players.add(self.user3)
        self.tournament.save()

    @patch("app.models.tournament")
    def test_init(self, mock_tournament):
        tournament_system_rr = TournamentSystemRoundRobin(mock_tournament)
        self.assertEqual(tournament_system_rr.battle_count, len(tournament_system_rr.tournament.players) * (
                len(tournament_system_rr.tournament.players) - 1) / 2)

    @patch("app.models.tournament")
    def test_battles(self, mock_tournament):
        tournament_system_rr = TournamentSystemRoundRobin(mock_tournament)
        tournament_system_rr.run_tournament()
        self.assertEqual(tournament_system_rr.battle_count, 0)

    def test_calculate_places(self):
        self.player1.number_of_points = 100
        self.player2.number_of_points = 1203
        self.player3.number_of_points = 594
        self.player1.save()
        self.player2.save()
        self.player3.save()
        tournament_system = TournamentSystemRoundRobin(self.tournament)
        tournament_system.calculate_places()

        self.assertEqual(tournament_system.players_in_tournament[0].place, 1)
        self.assertEqual(tournament_system.players_in_tournament[1].place, 2)
        self.assertEqual(tournament_system.players_in_tournament[2].place, 3)

    @patch('app.models.tournament_system_round_robin.TournamentSystemRoundRobin.tournament')
    def test_finish(self, mock_tournament):
        mock_tournament.return_value = Mock()

        tournament_system = TournamentSystemRoundRobin(mock_tournament)
        tournament_system.finish()

        self.assertEqual(mock_tournament.finish_finish_tournament.call_count, 0)

    # @patch('app.models.tournament_system_round_robin.TournamentSystemRoundRobin.write_battle_result')
    def test_write_battle_results(self):
        tournament_system = TournamentSystemRoundRobin(self.tournament)
        battles = tournament_system.tournament.battles.all()
        points = {'user1': 0, 'user2': 0, 'user3': 0}
        for battle in battles:
            players = battle.players.through.objects.filter(battle=battle)
            for player in players:
                points_count = random.randint(0, 1000)
                player.number_of_points = points_count
                points[player.player.username] += points_count
                player.save()
            battle.save()
        tournament_system.write_battle_result()

        for player in tournament_system.players_in_tournament:
            self.assertEqual(points[player.player.username], player.number_of_points)


if __name__ == '__main__':
    unittest.main()
