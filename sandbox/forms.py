from django import forms
from Strategy_game.sandbox.forms import SandboxForm
from database import Games #не знаю, где они хранятся
from Strategy_game.sandbox.models.sandbox import Sandbox


class SandboxForm(forms.ModelForm):
    class Meta:
        model = SandboxForm
    def __init__(self):
        self.CHOICES = []
        for x in Games:
            self.CHOICES.append(x.name)
        self.num_game = forms.ChoiceField(label="Game", choices=self.CHOICES)
        self.user_strategy = forms.FileField(label="Your strategy")
    def run_sandbox(self):
        sandbox = Sandbox(self.num_game, self.user_strategy) #создали sandbox по параметрам, которые получили
        sandbox.run_battle()
