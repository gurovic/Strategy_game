import os

from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from django.core.files import File

from app.models import Game, Tournament, PlayerInTournament
from app.compiler import Compiler, CompilerReport


class TestTournament(TestCase):
    @classmethod
    def setUpTestData(cls):
        def compile_and_upload_file(objects_file_field: models.FileField, path_to_file: str):
            def get_compiler_callback(report: CompilerReport):
                path_to_compiled_file = report.compiled_file.path
                name = path_to_compiled_file.split("/")[-1]
                local_file = open(path_to_compiled_file)
                django_file = File(local_file)
                objects_file_field.save(name, django_file)
                local_file.close()
                os.remove(path_to_compiled_file)

            path_to_file = os.path.abspath(path_to_file)
            compiler = Compiler(path_to_file, 'py', get_compiler_callback)
            compiler.compile()

        cls.game = Game.objects.create(name="Some game", number_of_players=2, win_point=1, lose_point=0)
        compile_and_upload_file(cls.game.play, "app/integration_tests/tournament_integration_test/game_play.py")

        cls.user1 = User.objects.create_user(username='user1', password='12345')
        cls.user2 = User.objects.create_user(username='user2', password='12345')
        cls.user3 = User.objects.create_user(username='user3', password='12345')

        cls.tournament = Tournament.objects.create(name="Some tournament", game=cls.game)

        player_in_tournament1 = PlayerInTournament.objects.create(player=cls.user1, tournament=cls.tournament)
        compile_and_upload_file(player_in_tournament1.file_solution,
                                "app/integration_tests/tournament_integration_test/solution1.py")

        player_in_tournament2 = PlayerInTournament.objects.create(player=cls.user2, tournament=cls.tournament)
        compile_and_upload_file(player_in_tournament2.file_solution,
                                "app/integration_tests/tournament_integration_test/solution2.py")

        player_in_tournament3 = PlayerInTournament.objects.create(player=cls.user3, tournament=cls.tournament)
        compile_and_upload_file(player_in_tournament3.file_solution,
                                "app/integration_tests/tournament_integration_test/solution3.py")

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.game.play.path)
        for player_in_tournament in PlayerInTournament.objects.all():
            os.remove(player_in_tournament.file_solution.path)
        super().tearDownClass()

    def test(self):
        tournament = self.tournament
        tournament.end_registration()

        self.assertEqual(tournament.status, Tournament.Status.FINISHED)
