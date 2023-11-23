import time

from .battle import Battle
from app.models import PlayersInBattle


class Sandbox:
    def __init__(self, game, strategy):
        self.game = game
        self.strategy = strategy
        players = [PlayersInBattle(player=strategy, strategy_id=0)]
        for i in range(game.number_of_players - 1):
            players.append(PlayersInBattle(player=game.ideal_solution, strategy_id=i + 1))
        self.battle = Battle(game, players)

    def run_battle(self):
        self.battle.run()

    def notify(self, report):
        self.report = report

    def get_report(self):
        while True:
            if self.report is not None:
                return self.report
            else:
                time.sleep(1)
