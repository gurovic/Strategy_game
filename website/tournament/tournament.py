from datetime import datetime

class Tournament:
    def __init__(self, name, game, players, system, start_time, end_time):
        self.name = name
        self.game = game
        self.players = players
        self.system = system
        self.start_time = start_time
        self.end_time = end_time
        self.running_results_status = False

    def start(self):
        self.start_time = datetime.now()
        self.system.calculate_places(self.system.run_tournament(self), self.players)
        self.running_results_status = True

    def end(self):
        self.end_time = datetime.now()
        self.running_results_status = False