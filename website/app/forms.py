from django import forms
from django.forms import ModelForm, TextInput, DateTimeInput, NumberInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models.tournament import Tournament
from .models.game import Game

class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'game', 'system', 'finish_registration_time','tournament_start_time','max_of_players']
        '''
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
            'start_registration_time': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Время начала регистрации игроков'
            }),
            'finish_registration_time': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Время конца регистрации игроков'
            }),
            'max_of_players': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Максимальное количество игроков в турнире'
            })
        }
        '''

        
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
