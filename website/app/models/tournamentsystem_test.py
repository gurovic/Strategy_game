import unittest

from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.test import TestCase

from app.models import Tournament, PlayerInTournament
from .tournamentsystem import TournamentSystem


class TestTournamentSystem(TestCase):
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

    def test_init(self):
        class A(TournamentSystem):
            def __init__(self, tournament):
                super().__init__(tournament)

        a = A(self.tournament)
        self.assertEqual(a.tournament, self.tournament)

    def test_finish(self):
        class A(TournamentSystem):
            def __init__(self, tournament):
                super().__init__(tournament)

        a = A(self.tournament)
        a.finish()
        self.assertEqual(self.tournament.status, Tournament.Status.FINISHED)


if __name__ == '__main__':
    unittest.main()
