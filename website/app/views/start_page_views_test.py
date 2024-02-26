from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from unittest.mock import Mock, patch

from ..models import Game, Tournament
from ..views.tournament_registration_view import register

class TestStartPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user1', password='12345678')
        cls.user2 = User.objects.create_user(username='test_user2', password='12345678')

    def test_authorized_client_participate_in_tournament(self):
        client = Client()
        client.force_login(self.user)
        response = client.post('/app/start_page/', {'type': 'participate in tournament'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'start_page_views.html')

    def test_not_authorized_client_participate_in_tournament(self):
        response = self.client.post('/app/start_page/', {'type': 'participate in tournament'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'start_page_views.html')
