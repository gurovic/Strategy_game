from django.test import TestCase
from sandbox.forms import SandboxForm
from database import Games #не знаю, где они хранятся
from unittest.mock import Mock

from django.test import TestCase


class SandboxFormTest(TestCase):
    def test_create(self):
        a = SandboxForm()
        allGames = []
        for x in Games:
            allGames.append(x.name)
        self.asserequal(allGames, SandboxForm)

    def test_run_sandbox(self):
        pass

# Create your tests here.
