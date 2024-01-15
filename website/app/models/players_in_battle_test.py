from django.db import IntegrityError
from django.test import TestCase
from app.models.players_in_battle import PlayersInBattle


class PlayersInBattleTest(TestCase):
    def setUp(self):
        PlayersInBattle.objects.create(player=None, number=1)
        PlayersInBattle.objects.create(player=None, number=2)
        PlayersInBattle.objects.create(player=None, number=3)

    def test_number(self):
        player = PlayersInBattle.objects.create(player=None, number=4)
        self.assertEqual(player.number, 4)

    def test_unique_api_id_is_enforced(self):
        """ Test that two movies with same api_id are not allowed."""
        with self.assertRaises(IntegrityError):
            PlayersInBattle.objects.create(player=None, number=2)
