from django import forms
from run_sandbox import Button
from database import Games #не знаю, где они хранятся
from Strategy_game.sandbox.models.sandbox import Sandbox


class SandboxForm(forms.ModelForm):
    class Meta:
        model = Button
    CHOICES = []
    for x in Games:
        CHOICES.append(x.name)
    num_game = forms.ChoiceField(label="Game", choices=CHOICES)
    user_strategy = forms.FileField(label="Your strategy")
    sb = Sandbox(num_game, user_strategy)
    sb.run_battle()
