from django import forms
from .models.run_sandbox import Button
from database import Games #не знаю, где они хранятся


class ButtonForm(forms.ModelForm):
    class Meta:
        model = Button
    CHOICES = []
    for x in Games:
        CHOICES.append(x.name)
    num_game = forms.ChoiceField(label="Game", choices=CHOICES)
    user_strategy = forms.FileField(label="Your strategy")
