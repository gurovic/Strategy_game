from unittest import TestCase
from unittest.mock import Mock

from ..classes.jury import GameState
from . import Battle


class BattleTest(TestCase):
    def test_create(self):
        battle = Battle()
        battle.save()
        self.assertEqual(Battle.objects.get(jury_report=battle.jury_report), battle)

    def test_run(self):
        mock_jury = Mock()
        battle = Battle()
        battle.save()

        battle.game_state = GameState.END
        mock_jury.game_state = GameState.END
        battle.run(mock_jury)

        self.assertEquals(battle.status, "OK")
        self.assertEquals(battle.moves, [])
