from .models.tournament import Tournament
from django.forms import ModelForm, TextInput, DateTimeInput, NumberInput
from django import forms
from .models.game import Game
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'game', 'system', 'start_time', 'end_time', 'max_of_players']


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
