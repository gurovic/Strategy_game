from django import forms
from .models.game import Game


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'number_of_players', 'win_point', 'lose_point', 'rules']
