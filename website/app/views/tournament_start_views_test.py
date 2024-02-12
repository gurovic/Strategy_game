from django.test import TestCase
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from unittest.mock import Mock, patch

from app.models import Tournament, Game
from app.models.tournament_system_round_robin import TournamentSystemRoundRobin
from app.views.tournament_start_view import start_tournament


class TestSandboxViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.game = Game.objects.create(id=0)
        cls.tournament = Tournament.objects.create(id=0, name="test1", game=cls.game)
        cls.tournament_system = TournamentSystemRoundRobin(cls.tournament)

    def test_views_url_exists(self):
        response = self.client.get('/app/tournament/start/0')
        self.assertEqual(response.status_code, 200)

    def test_views_use_correct_template(self):
        response = self.client.get('/app/tournament/start/0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tournament_start.html')

    def test_views_use_correct_context(self):
        response = self.client.get('/app/tournament/start/0')
        self.assertEqual(response.status_code, 200)

    @patch('app.views.tournament_start_view.Tournament')
    def test_post_compiler_request(self, tournament_mock):
        mock_compiler_instance = Mock()
        tournament_mock.return_value = mock_compiler_instance

        response = self.client.post('/app/tournament/start/0')

        # mock_compiler_instance.run.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['status'], 'getting report')

    @patch('app.views.tournament_start_view.Tournament')
    def test_get_request(self, tournament_mock):
        mock_compiler_instance = Mock()
        tournament_mock.return_value = mock_compiler_instance

        response = self.client.get('/app/tournament/start/0')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['status'], 'posting tournament')
