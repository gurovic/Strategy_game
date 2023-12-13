from tournamentsystem import TournamentSystem
from app.models.battle import Battle

class TournamentSystemRoundRobin(TournamentSystem):
    def __init__(self, tournament):
        super().__init__(tournament)
        self.battle_count = len(self.tournament.players)*(len(self.tournament.players)-1)/2

    def run_tournament(self):
        for i in range(len(self.tournament.players)):
            for j in range(i+1, len(self.tournament.players)):
                Battle(self.tournament.game, list([self.tournament.players[i], self.tournament.players[j]]))

    def calculate_places(self):
        places = self.tournament.players
        places = sorted(places, key = lambda x: (x.number_of_wins, x.number_of_points))
        self.finish()
        return places

    def finish(self):
        self.tournament.end()

    def write_battle_result(self, battle):
        if battle.players[0].iswinner:
            battle.players[0].number_of_wins += 1
        elif battle.players[1].iswinner:
            battle.players[1].number_of_wins += 1

    def notify(self, battle):
        self.battle_count -= 1
        self.battles.append(battle)
        self.write_battle_result(battle)
