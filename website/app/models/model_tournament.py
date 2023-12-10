from datetime import datetime


class Tournament:

    def start(self):
        self.start_time = datetime.now()
        self.system.calculate_places(self.system.run_tournament(self), self.players)
        self.running_results_status = True

    def end(self):
        self.end_time = datetime.now()
        self.running_results_status = False