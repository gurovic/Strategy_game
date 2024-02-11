from datetime import datetime, timedelta
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.http import HttpRequest
from unittest.mock import Mock, patch

from ..models import Game, Tournament
from ..views.tournament_results_view import show


class TestTournamentResultsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.game = Game.objects.create(id=0)
        now = timezone.now()
        cls.tournament1 = Tournament.objects.create(name="Турнир 1", game=cls.game, start_time=now+timedelta(minutes=20), end_time=now+timedelta(minutes=50))
        cls.tournament2 = Tournament.objects.create(name="Турнир 2", game=cls.game, start_time=now-timedelta(days=5), end_time=now-timedelta(days=4))
        cls.tournament3 = Tournament.objects.create(name="Турнир 3", game=cls.game, start_time=now-timedelta(minutes=20), end_time=now+timedelta(minutes=40))
        cls.tournament4 = Tournament.objects.create(name="Турнир 4", game=cls.game, start_time=now+timedelta(days=2), end_time=now+timedelta(days=2, minutes=30))
        cls.tournament5 = Tournament.objects.create(name="Турнир 5", game=cls.game, start_time=now-timedelta(hours=3), end_time=now-timedelta(hours=2))
        cls.tournament6 = Tournament.objects.create(name="Турнир 6", game=cls.game, start_time=now-timedelta(days=10, hours=3), end_time=now-timedelta(days=10))

    def test_views_url_exists(self):
        response = self.client.get('/app/tournaments')
        self.assertEqual(response.status_code, 200)

    def test_views_use_correct_template(self):
        response = self.client.get('/app/tournaments')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tournaments.html')

    def test_upcoming_or_current_tournaments_context(self):
        response = self.client.get('/app/tournaments')
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["upcoming_or_current_tournaments"],
                                 [self.tournament3, self.tournament1, self.tournament4])

    def test_past_tournaments_contex(self):
        response = self.client.get('/app/tournaments')
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["past_tournaments"],
                                 [self.tournament5, self.tournament2, self.tournament6])

