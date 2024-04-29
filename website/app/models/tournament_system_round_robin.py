import datetime

from .game import Game
from .battle import Battle
from .tournament_system import TournamentSystem
from .players_in_battle import PlayersInBattle


class TournamentSystemRoundRobin(TournamentSystem):
    tournament = None

    def __init__(self, tournament):
        super(TournamentSystemRoundRobin, self).__init__(tournament)
        self.battle_count = len(self.players_in_tournament) * (len(self.players_in_tournament) - 1) / 2
        for i in range(len(self.players_in_tournament)):
            for j in range(i + 1, len(self.players_in_tournament)):
                battle = Battle.objects.create(game=self.tournament.game)
                PlayersInBattle.objects.create(file_solution=self.players_in_tournament[i].file_solution, number=0,
                                               battle=battle, player=self.players_in_tournament[i].player)
                PlayersInBattle.objects.create(file_solution=self.players_in_tournament[j].file_solution, number=1,
                                               battle=battle, player=self.players_in_tournament[j].player)
                self.tournament.battles.add(battle)

    def run_tournament(self):
        for battle in self.tournament.battles.all():
            battle.run()
        self.write_battles_results()

    def calculate_places(self):
        last_place = 1
        for player in self.players_in_tournament.order_by("-number_of_points"):
            player.place = last_place
            player.save()
            last_place += 1

    def finish(self):
        self.tournament.finish_tournament()

    def write_battles_results(self):
        for battle in self.tournament.battles.all():
            players = battle.players.through.objects.filter(battle=battle)
            for player in players:
                for player_in_tournament in self.players_in_tournament:
                    if player_in_tournament.player == player.player:
                        player_in_tournament.number_of_points += player.number_of_points
                        player_in_tournament.save()
            self.tournament.save()
        self.calculate_places()
        self.finish()
