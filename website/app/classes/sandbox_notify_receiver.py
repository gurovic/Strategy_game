from .sandbox import Sandbox


class SandboxNotifyReceiver:
    def __init__(self, game, strategy):
        self.report = None
        self.game = game
        self.strategy = strategy
        self.sandbox = Sandbox(game, strategy, self.notify)

    def run(self):
        self.sandbox.run_battle()

    def notify(self, report):
        self.report = report
