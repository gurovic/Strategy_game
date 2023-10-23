from django.db import models
from django.contrib.auth.models import User
from .model_game import Game
from .model_battle import Battle, PlayersInBattles


class TournamentSystem:
    def __init__(self, tournament):
        self.tournament = tournament

    def start(self):
        raise NotImplementedError("The start() method must be overridden in the child class")

    def count_places(self):
        raise NotImplementedError("The count_places() method must be overridden in the child class")

    def count_points(self):
        battles = Battle.objects.get(tournament=self)
        for battle in battles:
            for player in battle.players.all():
                player_points = PlayersInTournament.object.get(tournament=self, player=player).number_of_points
                player_points += PlayersInBattles.object.get(battle=battle, player=player).points

    def count_wins(self):
        battles = Battle.objects.get(tournament=self)
        for battle in battles:
            for player in battle.players.all():
                player_wins = PlayersInTournament.object.get(tournament=self, player=player).number_of_wins
                player_wins += PlayersInBattles.object.get(battle=battle, player=player).wins


class RoundRobinSystem(TournamentSystem):
    def start(self):
        pass


class OlympicSystem(TournamentSystem):
    def start_round(self, players_in_round):
        number_of_players_in_game = self.tournament.game.number_of_players
        winners_in_round = players_in_round
        while len(players_in_round) >= number_of_players_in_game:
            players_in_battle = players_in_round[:number_of_players_in_game]
            battle = Battle(game=self.tournament.game, players=players_in_battle)
            battle.start()
            for player in players_in_battle:
                players_in_round.exclude(player)
                if PlayersInBattles.objects.get(player=player, battle=battle).is_wim is False:
                    winners_in_round.exclude(player)
        return winners_in_round

    def start(self):
        players = self.tournament.players
        while len(players) is not 1:
            players = self.start_round(players)


class TournamentSystemField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 104
        super().__init__(*args, **kwargs)


class Tournament(models.Model):
    name = models.CharField(max_length=255, default='tournament')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    players = models.ManyToManyField(User, through='PlayersInTournament')
    battles = models.ManyToManyField(Battle)
    system = models.TournamentSystemField()
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
        battles = Battle.objects.get(tournament=self)
        for battle in battles:
            for player in battle.players.all():
                player_wins = PlayersInTournament.object.get(tournament=self, player=player).number_of_wins
                player_wins += PlayersInBattles.object.get(battle=battle, player=player).wins

    def count_places(self):
        if self.system is "R":
            pass
        else:
            pass


class PlayersInTournament(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    strategy = models.FilePathField(null=True)
    place = models.PositiveIntegerField()
    number_of_wins = models.PositiveIntegerField(default=0)
    number_of_points = models.PositiveIntegerField(default=0)
