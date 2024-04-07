from unittest.mock import Mock, patch

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files import File

from ..classes.tests_utils import compile_and_upload_to_file_field
from ..classes.jury import GameState
from ..models.jury_report import JuryReport
from . import Battle, Game, PlayersInBattle
from invoker.utils import Singleton


class BattleTest(TestCase):
    def test_create(self):
        battle = Battle()
        battle.save()
        self.assertEqual(Battle.objects.get(jury_report=battle.jury_report), battle)

    @patch('invoker.invoker_multi_request_priority_queue.InvokerMultiRequestPriorityQueue.add')
    def test_create_invoker_requests(self, mock_queue_add: Mock):
        user1 = User.objects.create_user(username='user1')
        user2 = User.objects.create_user(username='user2')

        game = Game.objects.create(pk=1)
        compile_and_upload_to_file_field(game.play, 'app/models/play.py', 'py')

        battle = Battle.objects.create(game=game)

        player_in_battle1 = PlayersInBattle.objects.create(player=user1, battle=battle)
        compile_and_upload_to_file_field(player_in_battle1.file_solution, 'app/models/solution.py', 'py')

        battle.create_invoker_requests()

        mock_queue_add.assert_called()
        invoker_requests = mock_queue_add.call_args.args[0].invoker_requests
        self.assertEqual(battle.numbers, {1: user1})

    @patch('app.models.battle.Battle.create_invoker_requests')
    def test_run(self, mock_create_invoker_requests: Mock):
        mock_jury = Mock()
        battle = Battle.objects.create(pk=0)
        battle.jury = mock_jury

        battle.game_state = GameState.END
        mock_jury.game_state = GameState.END
        Battle.jury_report = JuryReport()
        Battle.jury_report.points = {1:1}
        Battle.jury_report.status = 1
        Battle.jury_report.story_of_game = []
        Battle.jury_report.save()
        battle.run()

        self.assertEquals(battle.status, 1)
        self.assertEquals(battle.moves, [])

    def tearDown(self) -> None:
        Singleton._instances = {}
