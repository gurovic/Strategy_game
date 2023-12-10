import unittest
from unittest.mock import Mock, patch
from model_tournament import Tournament, PlayerInTournament

from django.utils import timezone


class TestTournament(unittest.TestCase):
    def setUp(self):
        Tournament.objects.create(running_results_status=Tournament.Status.NOT_STARTED, name="Some tournament", start_time=timezone.now(), end_time=timezone.now())
        Tournament.objects.create(running_results_status=Tournament.Status.IN_PROCESSING, name="Some tournament", start_time=timezone.now(), end_time=timezone.now())
        Tournament.objects.create(running_results_status=Tournament.Status.FINISHED, name="Some tournament", start_time=timezone.now(), end_time=timezone.now())


if __name__ == '__main__':
    unittest.main()
