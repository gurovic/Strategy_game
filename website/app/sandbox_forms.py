from django import forms
from .models.game import Game
from .models.sandbox import Sandbox


class SandboxForm(forms.Form):
    #num_game = forms.ChoiceField(label="Game", choices=Game.objects.all())
    user_strategy = forms.FileField(label="Your strategy")

    def run_sandbox(self):
        sandbox = Sandbox(self.num_game, self.user_strategy)  # создали sandbox по параметрам, которые получили
        sandbox.run_battle()
