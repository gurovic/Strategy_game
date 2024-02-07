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

    def test_start_tournament(self):
        test_tournament = Tournament.objects.create(max_of_players=3, name="test4")
        test_tournament.start()
        self.assertEqual(test_tournament.status, Tournament.Status.WAITING_SOLUTIONS)

    def test_end_tournament(self):

        test_tournament = Tournament.objects.create(max_of_players=3, name="test4")
        test_tournament.end()
        self.assertEqual(test_tournament.status, Tournament.Status.IN_PROGRESS)

    def test_notify(self):
        test_tournament = Tournament.objects.create(max_of_players=3, name="test4")
        test_tournament.notify()
        self.assertEqual(test_tournament.status, Tournament.Status.FINISHED)
