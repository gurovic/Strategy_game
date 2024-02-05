import datetime

from .game import Game
from .battle import Battle
from .tournamentsystem import TournamentSystem
from .players_in_battle import PlayersInBattle


class TournamentSystemRoundRobin(TournamentSystem):
    def __init__(self, tournament):
        super(TournamentSystemRoundRobin, self).__init__(tournament)
        self.tournament = tournament
        self.tournament_players = dict()
        self.players_in_tournament = self.tournament.players.through.objects.filter(tournament=self.tournament)
        for player in self.players_in_tournament:
            self.tournament_players[player.player] = player
        self.battle_count = len(self.tournament_players) * (len(self.tournament_players) - 1) / 2

    def run_tournament(self):
        participants = list(zip(self.tournament_players.keys(), self.tournament_players.values()))
        for i in range(len(participants)):
            for j in range(i + 1, len(participants)):
                battle = Battle.objects.create(game=self.tournament.game)
                PlayersInBattle.objects.create(file_solution=participants[i][1].file_solution, number=0, battle=battle)
                PlayersInBattle.objects.create(file_solution=participants[j][1].file_solution, number=1, battle=battle)
                self.tournament.battles.add(battle)
                battle.start()
        self.write_battle_result()

    def calculate_places(self):
        # TODO
        places = list(zip(self.tournament_players.keys(), self.tournament_players.values()))
        places = sorted(places, key=lambda x: x[1].number_of_points)
        number = 1
        for place in places:
            place[1].place = number
            number += 1

    def finish(self):
        self.tournament.finish_tournament()

    def write_battle_result(self):
        #TODO
        points = {}
        for battle in self.tournament.battles:
            players = battle.players.through.objects.filter(battle=battle)
            for player in players:
                points[player.player] += player.number_of_points
        for user, point in points.items():
            tournament_player = self.tournament_players.get(player=user)
            tournament_player.number_of_point = point
            tournament_player.save()
        self.calculate_places()
        self.finish()
