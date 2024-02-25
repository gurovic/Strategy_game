from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from unittest.mock import Mock, patch

from ..models import Game, Tournament
from ..views.tournament_registration_view import register

class TestRegisterRequestViews(TestCase):

    def test_authorized_client(self):
        client = Client()
        client.force_login(self.user)
        response = client.post('/app/start_page/', {'type': 'participate in tournament'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'start_page_views.html')

