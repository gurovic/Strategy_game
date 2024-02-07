from django.test import TestCase
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.utils import timezone
from unittest.mock import Mock, patch

from ..models import Game, Tournament, PlayerInTournament
from ..views.tournament_results_view import show


class TestTournamentResultsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.game = Game.objects.create(id=0)
        cls.user = User.objects.create_user(username='testuser', password='12345678')
        cls.tournament = Tournament.objects.create(
            name="Тестовый турнир",
            game=cls.game,
            status=3,
            end_time=timezone.now()
        )
        cls.player_in_tournament = PlayerInTournament.objects.create(
            player=cls.user,
            tournament=cls.tournament,
            place=1
        )

    def test_views_url_exists(self):
        response = self.client.get('/app/tournament1/results')
        self.assertEqual(response.status_code, 200)

    def test_views_use_correct_template(self):
        response = self.client.get('/app/tournament1/results')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tournament_results.html')

    def test_views_use_correct_context(self):
        response = self.client.get('/app/tournament1/results')
        self.assertEqual(response.status_code, 200)