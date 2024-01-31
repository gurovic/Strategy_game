from django.test import TestCase
from .models import Game  # Adjust the import based on your project structure
from .game_upload_form import GameForm

class GameFormTest(TestCase):

    def test_game_form_valid(self):
        data = {'name': 'Test Game', 'number_of_players': 4}
        form = GameForm(data=data)
        self.assertTrue(form.is_valid())

    def test_game_form_invalid(self):
        data = {'name': '', 'number_of_players': 0}
        form = GameForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
