from app.models import Battle, PlayersInBattle


class Sandbox:
    def __init__(self, game, strategy, callback):
        self.game = game
        self.strategy = strategy
        self.callback = callback
        self.battle = Battle.objects.create(game=self.game)
        player = PlayersInBattle.objects.create(file_solution=strategy, number=1, battle=self.battle)
        self.players = [player]
        for i in range(1, self.game.number_of_players):
            player = PlayersInBattle.objects.create(file_solution=self.game.ideal_solution, number=i + 1,
                                                    battle=self.battle)
            self.players.append(player)
        self.battle.save()

    def run_battle(self):
        self.battle.run(self.notify)

    def notify(self, report):
        self.callback(report)
