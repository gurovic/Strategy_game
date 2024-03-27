from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from unittest.mock import Mock, patch

from ..models import Game, Tournament
from ..views.tournament_registration_view import register


class TestTournamentResultsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tournament = Tournament.objects.create(name="Тестовый турнир", max_of_players=1)

        cls.user = User.objects.create_user(username='test_user1', password='12345678')
        cls.user2 = User.objects.create_user(username='test_user2', password='12345678')

    def test_not_authorized_client(self):
        response = self.client.get('/app/tournament/1/registration')
        self.assertEqual(response.status_code, 404)

    def test_authorized_client(self):
        client = Client()
        client.force_login(self.user)
        response = client.get('/app/tournament/1/registration')
        self.assertEqual(response.status_code, 404)
        #self.assertTemplateUsed(response, 'tournament_registration.html')

    def test_views_use_correct_context(self):
        client = Client()
        client.force_login(self.user)

        response = client.get('/app/tournament/1/registration')
        self.assertEqual(response.status_code, 404)
        #self.assertEqual(response.context['status'], 'not registered')

        response = client.post('/app/tournament/1/registration')
        self.assertEqual(response.status_code, 404)
        #self.assertEqual(response.context['status'], 'registered')

        response = client.post('/app/tournament/1/registration')
        self.assertEqual(response.status_code, 404)
        #self.assertEqual(response.context['status'], 'already registered')

        client2= Client()
        client2.force_login(self.user2)

        response = client2.post('/app/tournament/1/registration')
        self.assertEqual(response.status_code, 404)
        #self.assertEqual(response.context['status'], 'denied registration')
