from django.db import models

from app.models import Tournament


class TournamentSystem(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    def run_tournament(self):
        pass

    def calculate_places(self):
        pass

    def finish(self):
        self.tournament.notify()

    def write_battle_result(self, results, numbers):
        pass

    def notify(self, results, numbers):
        self.write_battle_result(results, numbers)
