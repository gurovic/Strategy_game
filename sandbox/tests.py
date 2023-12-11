from django.test import TestCase
from sandbox.forms import SandboxForm
from Strategy_game.sandbox.models.game import Game
from unittest.mock import Mock

from django.test import TestCase


class SandboxFormTest(TestCase):
    def test_create(self):
        a = SandboxForm()
        allGames = []
        for x in Game.objects.all():
            self.CHOICES.append(x.name)
        self.asserequal(allGames, SandboxForm)

    def test_run_sandbox(self):
        pass

# Create your tests here.
