from django.db import models
from django.contrib.auth.models import User

class Battle(models.Model):
    subscriber = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    players = models.ManyToManyField(User, through='PlayersInBattles')
    status = models.CharField(max_length=1, choices=[("O", "OK"), ("E", "Error"), ("T", "Time Limit"), ("N", "Not started")], default="N")  # by the rules or by errors
    total_time = models.TimeField()
    logs = models.FileField()

    def __init__(self, game, players, subscriber):
        self.game = game
        self.players = players
        self.subscriber = subscriber

    def start(self):
        # starts a battle, simultaneously records the progress of the battle in a log file
        pass
