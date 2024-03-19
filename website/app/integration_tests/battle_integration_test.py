from django.test import TestCase

from ..classes.jury import Jury
from ..launcher import Launcher
from ..models import Battle
from ...invoker.invoker_multi_request import InvokerMultiRequest
from ...invoker.invoker_request import InvokerRequest


class BattleTest(TestCase):
    def BattleRunTest(self):
        battle = Battle()
        file_path1 = "battle_test_files/strategy1"
        file_path2 = "battle_test_files/strategy2"
        file_path3 = "battle_test_files/play"
        first_strategy_invoker_request = InvokerRequest(f'python {file_path1}')
        second_strategy_invoker_request = InvokerRequest(f'python {file_path2}')
        play_inventory_request = InvokerRequest(f'python {file_path3}')
        invoker_multi_request = InvokerMultiRequest(
            [first_strategy_invoker_request, second_strategy_invoker_request, play_inventory_request])
        jury = Jury(invoker_multi_request)
        self.assertEqual(battle.status, battle.GameStateChoices.NS)
        battle.run(jury)
        self.assertEqual(battle.status, battle.GameStateChoices.OK)
