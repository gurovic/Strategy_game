from unittest import TestCase
from unittest.mock import Mock

from Strategy_game.website.app.classes.jury import GameState
from Strategy_game.website.app.models.battle import Battle


class BattleTest(TestCase):
    def test_create(self):
        mock_jury = Mock()
        mock_jury_report = Mock()
        battle = Battle(mock_jury, mock_jury_report)
        battle.save()
        self.assertEqual(Battle.objects.get(jury=mock_jury).jury_report, mock_jury_report)

    def test_run(self):
        class JuryReportMock(self):
            def __init__(self):
                self.story_of_game = []
                self.points = []
                self.status = "OK"

        mock_jury = Mock()
        mock_jury_report = JuryReportMock()
        battle = Battle(mock_jury, mock_jury_report)
        battle.save()

        battle.jury.game_state = GameState.END
        battle.run()

        self.assertEquals(battle.status, "OK")
        self.assertEquals(battle.moves, [])
