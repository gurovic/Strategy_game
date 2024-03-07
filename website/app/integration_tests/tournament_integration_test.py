import os

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files import File

from app.models import Game, Tournament


class TestTournament(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.game = Game.objects.create(name="Some game", number_of_players=2, win_point=1, lose_point=0)

        path_to_play = os.path.abspath("app/integration_tests/tournament_integration_test/game_play.py")
        play_file = open(path_to_play)
        django_play_file = File(play_file)
        cls.game.play.save("game_play.py", django_play_file)
        play_file.close()

        cls.first_user = User.objects.create_user(username='user1', password='12345')
        cls.second_user = User.objects.create_user(username='user2', password='12345')

        print(cls.game.play.path)

    def test(self):
        tournament = Tournament(name="Some tournament", game=self.game)
        tournament.save()
