from .models.tournament import Tournament
from django.forms import ModelForm, TextInput, DateTimeInput, NumberInput


class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'game', 'system', 'start_time', 'end_time', 'max_of_players']

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название турнира'
            }),
            'game': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Игра (по которой проводится турнир)'
            }),
            'system': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Система проведения турнира'
            }),
            'start_time': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Время начала регистрации игроков'
            }),
            'end_time': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Время конца регистрации игроков'
            }),
            'max_of_players': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Максимальное количество игроков в турнире'
            })
        }