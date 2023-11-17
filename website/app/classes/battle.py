import datetime
import random

from ..models import PlayersInBattle
from invoker.invoker_request import InvokerRequest
from invoker.models import InvokerReport
from invoker.invoker_multi_request import InvokerMultiRequest, Priority


class Battle:
    PRIORITY = Priority.GREEN  # TODO change

    def __init__(self, game, players: [PlayersInBattle]):
        self.id = random.randint(1, 1000000000000000000)
        self.game = game
        self.players = players
        self.status = False
        self.time_start = datetime.datetime.now()
        self.time_finish = datetime.datetime.now()
        self.moves = []
        self.report = None

    @staticmethod
    def get_running_command(path):
        return f"start {path}"

    def run(self):
        self.invoker_requests = [InvokerRequest(self.get_running_command(self.game.play), self.game.play)]
        for player in self.players:
            self.invoker_requests.append(InvokerRequest(self.get_running_command(player.path), player.path))
        self.invoker_multi_request = InvokerMultiRequest(self.invoker_requests, self.PRIORITY)
        self.invoker_multi_request.subscribers.append(self)

    def notify(self, report: InvokerReport):
        self.report = report

    def get_report(self):
        while self.report == None:
            pass
        return self.report
