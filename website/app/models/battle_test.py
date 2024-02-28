from unittest import TestCase
from unittest.mock import Mock

from ..classes.jury import GameState
from ..models.jury_report import JuryReport
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
        Battle.jury_report = JuryReport()
        Battle.jury_report.points = {1:1}
        Battle.jury_report.status = 1
        Battle.jury_report.story_of_game = []
        Battle.jury_report.save()
        battle.run(mock_jury)


        self.assertEquals(battle.status, 1)
        self.assertEquals(battle.moves, [])
