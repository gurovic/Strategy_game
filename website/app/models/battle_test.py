from unittest import TestCase
from unittest.mock import Mock

from Strategy_game.website.app.models.battle import Battle


class BattleTest(TestCase):
    def create_test(self):
        mock_jury = Mock()
        mock_jury_report = Mock()
        battle = Battle(mock_jury, mock_jury_report)
        battle.save()
        self.assertEqual(Battle.objects.filter(jury=mock_jury).jury_report, mock_jury_report)



