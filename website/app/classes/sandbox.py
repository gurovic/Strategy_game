from app.models.model_battle import Battle, PlayersInBattles


class Sandbox:
    def __init__(self, game, strategy, creator):
        self.game = game
        self.strategy = strategy
        self.creator = creator
        players = [PlayersInBattles(player=strategy, strategy_id=0)]
        for i in range(self.game.number_of_players - 1):
            players.append(PlayersInBattles(player=self.game.ideal_solution, strategy_id=i+1))
        self.battle = Battle(self.game, players)
        self.report = None

    def run_battle(self):
        self.battle.run()

    def notify(self, report):
        self.report = report
        self.creator(report)
