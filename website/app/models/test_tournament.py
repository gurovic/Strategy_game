from unittest import TestCase
from tournament import *


class TestTournament(TestCase):
    def test_get_by_order(self):
        a = Tournament
        self.assertEqual(type(a), Tournament)
