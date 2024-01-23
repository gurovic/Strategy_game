from ..invoker.invoker_multi_request import InvokerMultiRequest

import enum


class GameState(enum.Enum):
    PLAY = enum.auto()
    END = enum.auto()


class Jury:
    def __init__(self, invoker_multi_request: InvokerMultiRequest):
        self.invoker_multi_request = invoker_multi_request
        self.play_invoker_request = 0
        self.strategies_invoker_requests = []
        self.play_process = 0
        self.strategies_process = []
        self.game_state = GameState.PLAY

    def get_invoker_requests(self):
        for invoker_request in self.invoker_multi_request.invoker_requests:
            if invoker_request.type == InvokerRequestType.PLAY:
                self.play_invoker_request = invoker_request
            else:
                self.strategies_invoker_requests.append(invoker_request)

    def get_processes(self):
        self.play_process = self.play_invoker_request.process_callback
        for invoker_request in self.strategies_invoker_requests:
            self.strategies_process.append(invoker_request.process_callback)

    def perform_play_command(self):
        play_command = self.play_process.read()
        if play_command.state == "play":
            player = play_command.player
            data = play_command.data
            self.strategies_process[player].write(data)
        else:
            self.game_state = GameState.END
            players_points = play_command.points
            # return points to invoker_reports using invoker_request.report_callback
