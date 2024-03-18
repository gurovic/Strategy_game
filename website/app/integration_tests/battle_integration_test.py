from django.test import TestCase

from ..classes.jury import Jury
from ..models import Battle
from ...invoker.invoker_multi_request import InvokerMultiRequest
from ...invoker.invoker_request import InvokerRequest


class BattleTest(TestCase):
    def BattleRunTest(self):
        battle = Battle()
        first_strategy_invoker_request = InvokerRequest("")
        second_strategy_invoker_request = InvokerRequest("")
        play_inventory_request = InvokerRequest("")
        invoker_multi_request = InvokerMultiRequest(
            [first_strategy_invoker_request, second_strategy_invoker_request, play_inventory_request])
        jury = Jury(invoker_multi_request)
        self.assertEqual(battle.status, battle.GameStateChoices.NS)
        battle.run(jury)
        self.assertEqual(battle.status, battle.GameStateChoices.OK)