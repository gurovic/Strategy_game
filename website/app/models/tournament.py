from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    pass


class Battle(models.Model):
    pass


class Tournament(models.Model):
    name = models.CharField(max_length=255, default='tournament')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    players = models.ManyToManyField(User, through='PlayersInTournament')
    system = models.CharField(max_length=1, choices=[("R", "Round-robin system"), ("O", "Olympic system")], default="O")
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    answers_sending_status = models.CharField(max_length=1,
                                              choices=[("N", "Not started"), ("I", "In processing"), ("F", "Finished")],
                                              default="N")
    counting_results = models.CharField(max_length=1,
                                        choices=[("N", "Not started"), ("I", "In processing"), ("F", "Finished")],
                                        default="N")

    def start(self):
        participants = PlayersInTournament.objects.get(tournament=self)
        for i in range(len(participants)):
            for j in range(len(participants)):
                if j <= i:
                    continue
                Battle(participants[i], participants[j]).save()

    def count_points(self):
        battles = Battle.objects.get(tournament=self)
        for battle in battles:
            for player in battle.players.all():
                player.points = PlayersInTournament.objects.get(tournament=self, player=player).number_of_points
                player.points += PlayersInBattles.objects.get(battle=battle, player=player).points


class PlayersInTournament(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    strategy = models.FilePathField(null=True)
    place = models.PositiveIntegerField()
    number_of_wins = models.PositiveIntegerField(default=0)
    number_of_points = models.PositiveIntegerField(default=0)


class PlayersInBattles(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE)
    strategy = models.FilePathField(null=True)
    is_win = models.BooleanField(default=False)
    points = models.IntegerField()  # 1, 1/2, 0 like win/draw/lose, or points at the end of battle
    number = models.PositiveIntegerField()
