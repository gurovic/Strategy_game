from django.db import models
class TournamentSystem(models.Model):
    def __init__(self, tournament, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)
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
