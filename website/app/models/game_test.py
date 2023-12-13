from app.models.game import Game

from django.test import TestCase
from django.db import IntegrityError


class GameTest(TestCase):
    def setUp(self):
        play = None
        ideal_solution = None
        Game.objects.create(name='test1', play=play, ideal_solution=ideal_solution, number_of_players=2)
        Game.objects.create(name='test2', play=play, ideal_solution=ideal_solution, number_of_players=3)
        Game.objects.create(name='test3', play=play, ideal_solution=ideal_solution, number_of_players=5)
        Game.objects.create(name='test4', play=play, ideal_solution=ideal_solution, number_of_players=10, win_point=10)
        Game.objects.create(name='test6', play=play, ideal_solution=ideal_solution, number_of_players=2, win_point=30,
                            lose_point=10)
        Game.objects.create(name='test7', play=play, ideal_solution=ideal_solution, number_of_players=5)
        Game.objects.create(name='test8', play=play, ideal_solution=ideal_solution, number_of_players=6)
        Game.objects.create(name='test9', play=play, ideal_solution=ideal_solution, number_of_players=2, win_point=10)

    def test_get_by_name(self):
        game = Game.objects.get(name='test1')
        self.assertEqual(game.name, 'test1')

    def test_get_by_id(self):
        game = Game.objects.get(pk=1)
        self.assertEqual(game.name, 'test1')
        self.assertEqual(game.number_of_players, 2)

        game = Game.objects.get(pk=5)
        self.assertEqual(game.name, 'test6')
        self.assertEqual(game.win_point, 30)
        self.assertEqual(game.lose_point, 10)
        self.assertEqual(game.number_of_players, 2)

    def test_unique_api_id_is_enforces(self):
        with self.assertRaises(IntegrityError):
            Game.objects.create(
                name='test5',
                play=None,
                ideal_solution=None,
                id=1
            )
