from typing import Any

from django.test import TestCase
from unittest.mock import Mock, patch
from datetime import datetime
from django.utils import timezone

from .tournament import Tournament


def validate_time(time):
    now = timezone.now()
    return now - timezone.timedelta(days=1) <= time <= now


class TestTournament(TestCase):
    def setUp(self):
        Tournament.objects.create(name="test1", max_of_players=3)
        Tournament.objects.create(name="test2", max_of_players=5)

    def test_auto_time_add(self):
        test_tournament = Tournament.objects.create(name="test3", max_of_players=3)
        self.assertEqual(validate_time(test_tournament.start_time), True)

    def test_start_tournament(self):
        test_tournament = Tournament.objects.create(max_of_players=3, name="test4")
        test_tournament.start()
        self.assertEqual(test_tournament.status, Tournament.Status.WAITING_SOLUTIONS)

    @patch('app.models.Tournament.system')
    def test_end_tournament(self, mock_tournament_system):
        mock_tournament_system.return_value = 6

        test_tournament = Tournament.objects.create(max_of_players=3, name="test4")
        test_tournament.system = mock_tournament_system
        test_tournament.end()
        self.assertEqual(test_tournament.status, Tournament.Status.IN_PROGRESS)

    def test_notify(self):
        test_tournament = Tournament.objects.create(max_of_players=3, name="test4")
        test_tournament.notify()
        self.assertEqual(test_tournament.status, Tournament.Status.FINISHED)
