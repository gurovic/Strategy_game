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
        cls.tournament = Tournament.objects.create(name="Тестовый турнир", game=cls.game, status=3, finish_registration_time=timezone.now())

        cls.user1 = User.objects.create_user(username='test_user1', password='12345678')
        cls.user2 = User.objects.create_user(username='test_user2', password='12345678')
        cls.user3 = User.objects.create_user(username='test_user3', password='12345678')

        cls.player1_in_tournament = PlayerInTournament.objects.create(player=cls.user1, tournament=cls.tournament, place=2)
        cls.player2_in_tournament = PlayerInTournament.objects.create(player=cls.user2, tournament=cls.tournament, place=3)
        cls.player3_in_tournament = PlayerInTournament.objects.create(player=cls.user3, tournament=cls.tournament, place=1)

    def test_views_url_exists(self):
        response = self.client.get('/app/tournament/1/results')
        self.assertEqual(response.status_code, 200)

    def test_views_use_correct_template(self):
        response = self.client.get('/app/tournament/1/results')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tournament_results.html')

    def test_views_use_correct_context(self):
        response = self.client.get('/app/tournament/1/results')
        self.assertEqual(response.status_code, 200)

    def test_players_in_tournament_order(self):
        response = self.client.get('/app/tournament/1/results')
        self.assertQuerySetEqual(response.context["players_in_tournament"],
                                 [self.player3_in_tournament, self.player1_in_tournament, self.player2_in_tournament])
