from Strategy_game.sandbox.models.sandbox import Sandbox

class Button:
    def __init__(self):
        self.game = get() #написать то, как получаем игру, которую запускаем
        self.strategy = get()
        sb = Sandbox(self.game, self.strategy)
        sb.run_battle()



