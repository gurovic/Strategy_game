from tournament_system import TournamentSystem
from app/models/battle import Battle
class TournamentSystemRoundRobin(TournamentSystem):
    def __init__(self, tournament, battles):
        super().__init__(tournament,battles)

    def run_tournament(self):
        for i in range(len(self.tournament.players)):
            for j in range(len(self.tournament.players)):
                if i==j:
                    continue
                battle = Battle(self.tournament.game, list([self.tournament.players[i],self.tournament.players[j]]))

    def calculate_places(self):
        pass

    def write_battle_result(self, battle):
        pass

    def finish(self):
        pass
