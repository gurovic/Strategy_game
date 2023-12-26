from Strategy_game.website.app.models.tournament import Tournament
from django.forms import ModelForm


class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'game', 'system', 'start_time', 'end_time', 'max_of_players']