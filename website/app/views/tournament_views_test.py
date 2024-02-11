from django.test import TestCase
from unittest.mock import Mock, patch
from ..forms import TournamentForm
from ..models.game import Game



class TestTournamentViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.game = Game.objects.create(id=0)

    @patch('app.models.game')
    def test_if_form_is_valid(self, mock_game):
        data = {'name':'example_tournament', 'game':self.game, 'system':0, 'start_time':'2006-10-25 14:30:59', 'end_time':'2006-10-26 14:30:59', 'max_of_players':10}
        form = TournamentForm(data)
        if (form.is_valid()):
           response = self.client.get('/app/tournament/create/')
           self.assertEqual(response.status_code, 200)
        else:
            self.fail()

    def test_correct_template_1(self):
        response = self.client.get('/app/tournament/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tournament_page.html')



    def test_correct_template_2(self):
        response = self.client.get('/app/tournament/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tournament_create.html')