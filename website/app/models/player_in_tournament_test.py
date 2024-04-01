from django.db import IntegrityError
from django.test import TestCase

from app.models import PlayerInTournament


class PlayerInTournamentTest(TestCase):
    def setUp(self):
        self.player1 = PlayerInTournament(number_of_points=10, place=3)
        PlayerInTournament.objects.create(number_of_points=10, place=3)
        PlayerInTournament.objects.create(number_of_points=20, place=2)
        PlayerInTournament.objects.create(number_of_points=50, place=1)

    def test_unique_api_id_is_enforced(self):
        with self.assertRaises(IntegrityError):
            PlayerInTournament.objects.create(number_of_points=60, place=0, id=1)
            PlayerInTournament.objects.create(number_of_points=50, place=0, id=1)

    def test_set_0_by_default(self):
        player = PlayerInTournament.objects.create()
        self.assertEqual(player.number_of_points, 0)
        self.assertEqual(player.place, 0)

    def test_instance(self):
        self.assertEqual(self.player1.number_of_points, 10)
        self.assertEqual(self.player1.place, 3)
        self.assertEqual(self.player1.id, None)
