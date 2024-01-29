from ...invoker.invoker_multi_request import InvokerMultiRequest
from ...invoker.invoker_request import InvokerRequestType

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
