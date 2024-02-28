from django.test import TestCase
from .game_upload_form import GameForm


class GameFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'name': 'Test Game',
            'number_of_players': 4,
            'win_point': 10,
            'lose_point': 5,
            'rules': 'Some rules for the game.'
        }
        form = GameForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'number_of_players': 4,
            'win_point': 10,
            'lose_point': 5,
            'rules': 'Some rules for the game.'
        }
        form = GameForm(data=form_data)

        self.assertFalse(form.is_valid())
