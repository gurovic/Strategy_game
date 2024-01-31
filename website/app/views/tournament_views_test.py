from django.test import TestCase
from unittest.mock import Mock, patch
from ..forms import TournamentForm
from ..models.game import Game



class TestTournamentViews(TestCase):

    def test_if_form_is_valid(self):
        mock_game = Mock()
        data = {'name':'example_tournament', 'game':None, 'system':0, 'start_time':'2006-10-25 14:30:59', 'end_time':'2006-10-26 14:30:59', 'max_of_players':10}
        #if request.method == "POST":
        form = TournamentForm(data)
        if (form.is_valid()):
           response = self.client.get('/app/tournament/create/')
           self.assertEqual(response.status_code, 200)
        else:
            self.fail()

        #else:
        #    response = self.client.get('/app/tournament/create/')
        #    self.assertEqual(response.status_code, 200)
        #    self.assertTemplateUsed(response, 'tournament_create.html')
        #else:
        #    response = self.client.get('/app/tournament/create')
        #    self.assertEqual(response.status_code, 200)
        #    self.assertTemplateUsed(response, 'tournament_create.html')



    def test_correct_template_1(self):
        response = self.client.get('/app/tournament/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tournament_page.html')



    def test_correct_template_2(self):
        response = self.client.get('/app/tournament/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tournament_create.html')