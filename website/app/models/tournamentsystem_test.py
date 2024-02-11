import unittest

from django.contrib.auth.models import User
from django.db import models
from django.test import TestCase

from .tournamentsystem import TournamentSystem


class TestTournamentSystem(TestCase):
    def test_init(self):
        class A(TournamentSystem):
            def __init__(self):
                super().__init__()

        a = A()
        print(a)



if __name__ == '__main__':
    unittest.main()
