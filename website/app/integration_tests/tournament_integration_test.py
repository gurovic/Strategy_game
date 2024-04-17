import os

from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from django.core.files import File

from .. import compiler, launcher
from ..classes.tests_utils import compile_and_upload_to_file_field
from app.models import Game, Tournament, PlayerInTournament
from app.compiler import Compiler, CompilerReport


class TestTournament(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.game = Game.objects.create(pk=1, play=os.path.abspath(
            'app/integration_tests/tournament_integration_test/game_play.py'))

        cls.user1 = User.objects.create_user(username='user1', password='12345')
        cls.user2 = User.objects.create_user(username='user2', password='12345')
        cls.user3 = User.objects.create_user(username='user3', password='12345')

        cls.tournament = Tournament.objects.create(name="Some tournament", game=cls.game)

        PlayerInTournament.objects.create(player=cls.user1, tournament=cls.tournament,
                                          file_solution='app/integration_tests/tournament_integration_test/game_play.py')

        PlayerInTournament.objects.create(player=cls.user2, tournament=cls.tournament,
                                          file_solution='app/integration_tests/tournament_integration_test/game_play.py')

        PlayerInTournament.objects.create(player=cls.user3, tournament=cls.tournament,
                                          file_solution='app/integration_tests/tournament_integration_test/game_play.py')

    @classmethod
    def tearDownClass(cls):
        cls.game.play.delete()
        for player_in_tournament in PlayerInTournament.objects.all():
            player_in_tournament.file_solution.delete()
        super().tearDownClass()

    def test(self):
        tournament = self.tournament
        tournament.end_registration()

        self.assertEqual(tournament.status, Tournament.Status.FINISHED)
