import enum
import typing
import json

from invoker.invoker_request import InvokerRequest, InvokerRequestType
from app.models.jury_report import JuryReport
from invoker.invoker_multi_request import InvokerMultiRequest
from app.classes.logger import class_log


class GameState(enum.Enum):
    PLAY = enum.auto()
    END = enum.auto()


class StdIn(typing.Protocol):
    def write(self, data: str):
        ...


class StdOut(typing.Protocol):
    def read(self) -> str:
        ...

    def readline(self) -> str:
        ...


@class_log
class Jury:

    def __init__(self, invoker_multi_request: InvokerMultiRequest):
        self.invoker_multi_request = invoker_multi_request

        self.play_invoker_request = None
        self.strategies_invoker_requests = []

        self.process = None
        self.play_process = None
        self.strategies_process = []

        self.story_of_game = []

        self.game_state = GameState.PLAY
        self.jury_report = JuryReport()
        self.jury_report.status = ""
        self.jury_report.points = {}
        self.jury_report.story_of_game = ""

        self.get_invoker_requests()

    def get_invoker_requests(self):
        invoker_requests = self.invoker_multi_request.invoker_requests
        for invoker_request in invoker_requests:
            if invoker_request.label == "play":
                self.play_invoker_request = invoker_request
            else:
                self.strategies_invoker_requests.append(invoker_request)
        invoker_label = "player"
        player_number = 1
        invoker_request_sorted_array = []
        while (player_number <= len(self.strategies_invoker_requests)):
            invoker_label_now = invoker_label + str(player_number)
            index = 0
            end_cycle = 0
            found_player = 0
            while (end_cycle == 0):
                if (self.strategies_invoker_requests[index].label == invoker_label_now):
                    end_cycle = 1
                    invoker_request_sorted_array.append(self.strategies_invoker_requests[index])
                    found_player = 1
                index += 1
                if (index >= len(self.strategies_invoker_requests)):
                    end_cycle = 1
            if (found_player == 0):
                self.jury_report.status = JuryReport.Status.ERROR
                return self.jury_report
            player_number += 1
        self.strategies_invoker_requests = invoker_request_sorted_array

    def get_processes(self):
        if not self.process:
            self.invoker_multi_request.send_process()

        self.play_process = None
        self.strategies_process = []
        invoker_processes = self.process
        for invoker_process in invoker_processes:
            if invoker_process.label == "play":
                self.play_process = invoker_process
            else:
                self.strategies_process.append(invoker_process)
        process_label = "player"
        player_number = 1
        invoker_process_sorted_array = []
        while (player_number <= len(self.strategies_process)):
            process_label_now = process_label + str(player_number)
            index = 0
            end_cycle = 0
            found_player = 0
            while (end_cycle == 0):
                if (self.strategies_process[index].label == process_label_now):
                    end_cycle = 1
                    invoker_process_sorted_array.append(self.strategies_process[index])
                    found_player = 1
                index += 1
                if (index >= len(self.strategies_process)):
                    end_cycle = 1
            if (found_player == 0):
                self.jury_report.status = JuryReport.Status.ERROR
                return self.jury_report
            player_number += 1
        self.strategies_process = invoker_process_sorted_array

    def mark_error(self):
        self.game_state = GameState.END
        self.jury_report.status = JuryReport.Status.ERROR
        self.jury_report.save()
        return self.jury_report

    def perform_play_command(self):
        player_data = None

        while self.game_state == GameState.PLAY:
            try:
                play_command = self.play_process.connect(player_data)

                self.story_of_game.append(play_command)
                play_data = json.loads(play_command)
            except (RuntimeError, json.decoder.JSONDecodeError):
                return self.mark_error()
            
            match play_data["state"]:
                case "play":
                    player_command = self.strategies_process[play_data["player"]-1].connect(play_data["data"])
                    player_data = json.dumps({"player": play_data["player"], "data": player_command})
                    self.story_of_game.append(player_data)
                case "end":
                    self.game_state = GameState.END

                    self.jury_report.story_of_game = self.story_of_game
                    self.jury_report.status = JuryReport.Status.OK

                    points = {}
                    for player, point in enumerate(play_data["points"]):
                        points[player+1] = point

                    self.jury_report.points = points

                    self.jury_report.save()

                    return self.jury_report
                case _:
                    return self.mark_error()

    def notify_processes(self, processes):
        self.process = processes
        self.get_processes()

    def notify(self, report):
        pass
