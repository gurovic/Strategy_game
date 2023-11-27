from datetime import datetime
from tournament_system import TournamentSystem


class Tournament:
    def __init__(self, name, game, players, system):
        self.name = name
        self.game = game
        self.players = players
        self.system = system
        self.start_time = None
        self.end_time = None
        self.running_results_status = False
        self.player_in_tournament_list = []

    def start(self):
        if not self.running_results_status:
            self.start_time = datetime.now()
            battles = self.system.generate_battles(self)
            self.system.calculate_points(battles, self.player_in_tournament_list)
            self.running_results_status = True

    def end(self):
        if self.running_results_status:
            self.end_time = datetime.now()
            self.running_results_status = False