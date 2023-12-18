from tournamentsystem import TournamentSystem
from app.models.battle import Battle

class TournamentSystemRoundRobin(TournamentSystem):
    def __init__(self, tournament):
        super().__init__(tournament)
        self.battle_count = len(self.tournament.players)*(len(self.tournament.players)-1)/2

    def run_tournament(self):
        participants = list(zip(self.tournament.players.keys(), self.tournament.players.values()))
        for i in range(len(participants)):
            for j in range(i+1, len(participants)):
                battle = Battle(self.tournament.game, list([participants[i][1], participants[j][1]]), self)
                self.tournament.battles.append(battle)
                battle.run()

    def calculate_places(self):
        places = list(zip(self.tournament.players.keys(), self.tournament.players.values()))
        places = sorted(places, key = lambda x: x[1].number_of_points)
        number = 1
        for place in places:
            place[1].place = number
            number += 1

    def finish(self):
        self.tournament.end()

    def write_battle_result(self, results, numbers):
        for result in results:
            self.tournament.players[numbers[result[0]].user].number_of_points += result[1]
            self.tournament.players[numbers[result[0]].user].save()
        self.battle_count -= 1
        if self.battle_count == 0:
            self.calculate_places()
            self.finish()


