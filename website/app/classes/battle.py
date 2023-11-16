import datetime

from ..models import PlayersInBattle
from Strategy_game.invokersstructure.invokerReport import InvokerReport
from Strategy_game.invokersstructure.invokerRequest import InvokerRequest
from Strategy_game.invokersstructure.invokerMultiRequest import InvokerMultiRequest


class Battle:
    PRIORITY = 10

    def __init__(self, game, players: [PlayersInBattle]):
        self.game = game
        self.players = players
        self.status = False
        self.time_start = datetime.datetime.now()
        self.time_finish = datetime.datetime.now()
        self.moves = []

    @staticmethod
    def get_running_command(path):
        return f"start {path}"

    def run(self):
        self.invoker_requests = [InvokerRequest(self.get_running_command(self.game.play), self.game.play)]
        for player in self.players:
            self.invoker_requests.append(InvokerRequest(self.get_running_command(player.path), player.path))
        self.invoker_multi_request = InvokerMultiRequest(self.invoker_requests, self, self.PRIORITY)

    def notify(self, reports: InvokerReport):
        # TODO предать этот информацию всех User который участвовали в этом Battle
        pass
