from django.db import IntegrityError
from django.test import TestCase

from app.models import PlayersInBattle


class PlayersInBattleTest(TestCase):
    def setUp(self):
        PlayersInBattle.objects.create(player=None, number=1)
        PlayersInBattle.objects.create(player=None, number=2)
        PlayersInBattle.objects.create(player=None, number=3)

    def test_number(self):
        player = PlayersInBattle.objects.create(player=None, number=4)
        self.assertEqual(player.number, 4)

    def test_creating(self):
        player = PlayersInBattle.objects.create(number=4, number_of_points=100, place=1)
        self.assertEqual(player.number_of_points, 100)
        self.assertEqual(player.number, 4)
        self.assertEqual(player.place, 1)
        self.assertEqual(type(player), PlayersInBattle)
