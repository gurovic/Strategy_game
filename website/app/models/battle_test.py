from unittest import TestCase
from unittest.mock import Mock

from ..classes.jury import GameState
from . import Battle


class BattleTest(TestCase):
    def test_create(self):
        mock_jury = Mock()
        battle = Battle(mock_jury)
        battle.save()
        self.assertEqual(Battle.objects.get(jury_report=battle.jury_report).jury, mock_jury)

    def test_run(self):
        mock_jury = Mock()
        battle = Battle(mock_jury)
        battle.save()

        battle.jury.game_state = GameState.END
        battle.run()

        self.assertEquals(battle.status, "OK")
        self.assertEquals(battle.moves, [])
