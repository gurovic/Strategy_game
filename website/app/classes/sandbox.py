from .battle import Battle
from app.models import PlayersInBattle


class Sandbox:
    def __init__(self, game, strategy):
        self.game = game
        self.strategy = strategy
        players = [PlayersInBattle(player=strategy, strategy_id=0)]
        for i in range(self.game.number_of_players - 1):
            players.append(PlayersInBattle(player=self.game.ideal_solution, strategy_id=i+1))
        self.battle = Battle(self.game, players)

    def run_battle(self):
        self.battle.run()

    def get_report(self):
        self.report = self.battle.get_report()
        return self.report
