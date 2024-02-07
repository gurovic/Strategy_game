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

    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

