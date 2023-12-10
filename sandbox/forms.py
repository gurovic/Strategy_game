from django import forms
from Strategy_game.sandbox.forms import SandboxForm
from database import Games #не знаю, где они хранятся
from Strategy_game.sandbox.models.sandbox import Sandbox


class SandboxForm(forms.ModelForm):
    class Meta:
        model = SandboxForm
    CHOICES = []
    for x in Games:
        CHOICES.append(x.name)
    num_game = forms.ChoiceField(label="Game", choices=CHOICES)
    user_strategy = forms.FileField(label="Your strategy")
    sandbox = Sandbox(num_game, user_strategy)
    sandbox.run_battle()
