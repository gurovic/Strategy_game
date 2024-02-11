from invoker.invoker_multi_request import InvokerMultiRequest
from invoker.invoker_request import InvokerRequestType
from invoker.invoker_request import InvokerRequest
from .jury_report import JuryReport

import enum


class GameState(enum.Enum):
    PLAY = enum.auto()
    END = enum.auto()


class Jury:
    def __init__(self, invoker_multi_request: InvokerMultiRequest):
        self.invoker_multi_request = invoker_multi_request

        self.play_invoker_request = None
        self.strategies_invoker_requests = []
        self.get_invoker_requests()

        self.play_process = None
        self.strategies_process = []
        self.get_processes()

        self.game_state = GameState.PLAY
        self.jury_report = JuryReport()

    def get_invoker_requests(self):
        invoker_requests = self.invoker_multi_request.invoker_requests
        for invoker_request in invoker_requests:
            if invoker_request.type == InvokerRequestType.PLAY:
                self.play_invoker_request = invoker_request
            else:
                self.strategies_invoker_requests.append(invoker_request)

    def get_processes(self):
        self.play_process = self.play_invoker_request.process_callback
        for invoker_request in self.strategies_invoker_requests:
            self.strategies_process.append(invoker_request.process_callback)

    def perform_play_command(self):
        try:
            play_command = self.play_process.read()
        except Exception:
            self.jury_report.error_occured()
            return self.jury_report
        if play_command["state"] == "play":
            player = play_command["player"] - 1
            data = play_command["data"]
            try:
                self.strategies_process[player].write(data)
            except Exception:
                self.jury_report.error_occured()
                return self.jury_report
            try:
                player_command = self.strategies_process[player].read()
            except Exception:
                self.jury_report.error_occured()
                return self.jury_report
            try:
                self.play_process.write(player_command)
            except Exception:
                self.jury_report.error_occured()
                return self.jury_report
        else:
            self.game_state = GameState.END
            players_points = play_command["points"]
            player = players_points["player"]
            points = players_points["points"]
            self.jury_report.add_points(player, points)
            return self.jury_report
