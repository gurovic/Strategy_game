from django.db import models
from django.contrib.auth.models import User
from .game import Game


class Battle(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    time_start = models.DateTimeField(auto_now_add=True)
    time_finish = models.DateTimeField(auto_now_add=True)
    players = models.ManyToManyField(User, through='PlayersInBattle', blank=True)
    status = models.CharField(max_length=1,
                              choices=[("O", "OK"), ("E", "Error"), ("T", "Time Limit Exceeded"), ("N", "Not started")],
                              default="N")  # by the rules or by errors
    logs = models.FileField(blank=True)

    def __init__(self, subscriber, jury, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscriber = subscriber
        self.moves = []
        self.results = {}
        self.jury = jury
        self.numbers = []

    def run(self):
        while self.jury.game_state == True:
            self.moves.append(self)
            self.jury.perform_play_command()

        # starts a battle, simultaneously records the progress of the battle in a log file
        pass
