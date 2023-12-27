from models.tournament import Tournament
from django.forms import ModelForm


class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'game', 'start_time', 'end_time', 'max_of_players'] #add system after fix