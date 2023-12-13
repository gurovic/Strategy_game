from django.test import TestCase
from unittest.mock import Mock, patch
from datetime import datetime
from django.utils import timezone

from .tournament import Tournament


class TestTournament(TestCase):
    def setUp(self):
        Tournament.objects.create(name="test1", max_of_players=3)
        Tournament.objects.create(name="test2", max_of_players=5)

    def test_auto_time_add(self):
        test_tournament = Tournament.objects.create(name="test3", max_of_players=3)
        self.assertEqual(test_tournament.start_time.was_published_recently(), True)

    def test_start_tournament(self):
        pass

    @patch('app.models.tournament.Tournament.system')
    def test_end_tournament(self, mock_system):
        pass

    def test_notify(self):
        pass
