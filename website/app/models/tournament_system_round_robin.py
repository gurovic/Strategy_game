import datetime

from .tournamentsystem import TournamentSystem
from .players_in_battle import PlayersInBattle
from .battle import Battle


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
                battle = Battle.objects.create(game=self.tournament.game, start_time=datetime.date.today())
                players = [
                    PlayersInBattle.objects.create(file_solution=participants[i][1], number=0, battle=battle),
                    PlayersInBattle.objects.create(file_solution=participants[j][1], number=1, battle=battle),
                ]
                print(players)
                battle.players.set(players)
                battle.save()
                self.tournament.battles.add(battle)
                battle.start()

    def calculate_places(self):
        places = list(zip(self.tournament_players.keys(), self.tournament_players.values()))
        places = sorted(places, key=lambda x: x[1].number_of_points)
        number = 1
        for place in places:
            place[1].place = number
            number += 1

    def finish(self):
        self.tournament.finish_tournament()

    def write_battle_result(self, results, numbers):
        for result in results.keys():
            self.tournament.players[numbers[result].user].number_of_points += results[result]
            self.tournament.players[numbers[result].user].save()
        self.battle_count -= 1
        if self.battle_count == 0:
            self.calculate_places()
            self.finish()
