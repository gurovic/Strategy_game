from django.db import models
from django.contrib.auth.models import User


class Tournament(models.Model):
    name = models.CharField(max_length=255, default='tournament')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    players = models.ManyToManyField(User, through='PlayersInTournament')
    system = models.CharField(max_length=1, choices=[("R", "Round-robin system"), ("O", "Olympic system")], default="O")
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    answers_sending_status = models.CharField(max_length=1, choices=[("N", "Not started"), ("I", "In processing"), ("F", "Finished")], default="N")
    counting_results = models.CharField(max_length=1, choices=[("N", "Not started"), ("I", "In processing"), ("F", "Finished")], default="N")

    def start(self):
        # starts battles
        pass

    def count_points(self):
        battles = Battle.objects.get(tournament=self)
        for battle in battles:
            for player in battle.players.all():
                player_points = PlayersInTournament.object.get(tournament=self, player=player).number_of_points
                player_points += PlayersInBattles.object.get(battle=battle, player=player).points

    def count_wins(self):
        pass


class PlayersInTournament(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    strategy = models.FilePathField(null=True)
    place = models.PositiveIntegerField()
    number_of_wins = models.PositiveIntegerField(default=0)
    number_of_points = models.PositiveIntegerField(default=0)
