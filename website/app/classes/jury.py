import enum

from invoker.invoker_request import InvokerRequest, InvokerRequestType
from app.models.jury_report import JuryReport
from invoker.invoker_multi_request import InvokerMultiRequest



class GameState(enum.Enum):
    PLAY = enum.auto()
    END = enum.auto()


class Jury:

    process = None

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


    def notify_processes(self, processes):
        self.process = processes

    def get_invoker_requests(self):
        invoker_requests = self.invoker_multi_request.invoker_requests
        for invoker_request in invoker_requests:
            if invoker_request.type == InvokerRequestType.PLAY:
                self.play_invoker_request = invoker_request
            else:
                self.strategies_invoker_requests.append(invoker_request)

    def get_processes(self):
        invoker_requests = self.invoker_multi_request.invoker_requests
        for i in range(len(self.process)):
            invoker_request = invoker_requests[i]
            if invoker_request.type == InvokerRequestType.PLAY:
                self.play_process = self.process[i]
            else:
                self.strategies_process.append(self.process[i])

    def perform_play_command(self):
        try:
            play_command = self.play_process.stdout.read()
        except RuntimeError:
            self.jury_report.status = "ERROR"
            return self.jury_report
        if play_command["state"] == "play":
            player_array = play_command["players"]
            data_array = play_command["data"]
            for i in range(len(player_array)):
                try:
                    self.strategies_process[player_array[i]].stdin.write(data_array[i])
                except RuntimeError:
                    self.jury_report.status = "ERROR"
                    return self.jury_report
            for i in range(len(player_array)):
                try:
                    player_command = self.strategies_process[player_array[i]].stdout.read()
                except RuntimeError:
                    self.jury_report.status = "ERROR"
                    return self.jury_report
                try:
                    self.play_process.stdin.write(player_command)
                except RuntimeError:
                    self.jury_report.status = "ERROR"
                    return self.jury_report
        else:
            self.game_state = GameState.END
            self.jury_report.status = "OK"
            players_points = play_command["points"]
            players = play_command["players"]
            for i in range(len(players_points)):
                self.jury_report.points[players[i]] = players_points[i]
            self.jury_report.story_of_game = play_command["story_of_game"]
            return self.jury_report
