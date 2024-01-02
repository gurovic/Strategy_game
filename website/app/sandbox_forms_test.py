from .sandbox_forms import SandboxForm
from .models.game import Game

from django.test import TestCase


class SandboxFormTest(TestCase):
    def test_create(self):
        a = SandboxForm()
        allGames = []
        for x in Game.objects.all():
            self.CHOICES.append(x.name)
        self.asserequal(allGames, SandboxForm)


# Create your tests here.
