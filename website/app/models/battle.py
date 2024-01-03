from django.db import models
from django.contrib.auth.models import User
from .game import Game


class Battle(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    players = models.ManyToManyField(User, through='PlayersInBattle')
    status = models.CharField(max_length=1, choices=[("O", "OK"), ("E", "Error"), ("T", "Time Limit"), ("N", "Not started")], default="N")  # by the rules or by errors
    total_time = models.TimeField()
    logs = models.FileField()

    def start(self):
        # starts a battle, simultaneously records the progress of the battle in a log file
        pass

    