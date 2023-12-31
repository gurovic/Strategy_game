from django.test import TestCase
import unittest
from ..forms import TournamentForm


class TestTournamentViews(TestCase):

    def test_if_form_is_valid(self, request):
        if request.method == "POST":
            form = TournamentForm(request.POST)
            if (form.is_valid()):
                response = self.client.get('/app/tournament/create')
                self.assertEqual(response.status_code, 200)
            else:
                response = self.client.get('/app/tournament/create')
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'tournament_create.html')
        else:
            response = self.client.get('/app/tournament/create')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'tournament_create.html')



    def test_correct_template_1(self):
        response = self.client.get('/app/tournament/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tournament_page.html')



    def test_correct_template_2(self):
        response = self.client.get('/app/tournament/create')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tournament_create.html')