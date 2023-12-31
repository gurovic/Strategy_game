class TournamentSystem:
    def __init__(self, tournament):
        self.tournament = tournament
        self.battles = []

    def run_tournament(self):
        pass

    def calculate_places(self):
        pass

    def finish(self):
        self.tournament.end()

    def write_battle_result(self, results, numbers):
        pass

    def notify(self, results, numbers):
        self.write_battle_result(results, numbers)
