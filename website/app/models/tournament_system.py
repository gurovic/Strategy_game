from django.db import models
from app.classes.logger import class_log


@class_log
class TournamentSystem:
    def __init__(self, tournament):
        self.tournament = tournament
        self.players_in_tournament = self.tournament.players.through.objects.filter(tournament=self.tournament)

    def run_tournament(self):
        pass

    def calculate_places(self):
        pass

    def finish(self):
        self.tournament.finish_tournament()

    def write_battle_result(self, results, numbers):
        pass

    def notify(self, results, numbers):
        self.write_battle_result(results, numbers)
