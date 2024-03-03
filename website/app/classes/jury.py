import enum

from invoker.invoker_request import InvokerRequest, InvokerRequestType
from app.models.jury_report import JuryReport
from invoker.invoker_multi_request import InvokerMultiRequest



class GameState(enum.Enum):
    PLAY = enum.auto()
    END = enum.auto()


class Jury:

    def __init__(self, invoker_multi_request: InvokerMultiRequest):
        self.invoker_multi_request = invoker_multi_request
        self.invoker_multi_request.subscribe(self)

        self.play_invoker_request = None
        self.strategies_invoker_requests = []
        self.get_invoker_requests()

        self.process = None
        self.play_process = None
        self.strategies_process = []

        self.game_state = GameState.PLAY
        self.jury_report = JuryReport()


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
                self.jury_report.status = "ERROR"
                return self.jury_report
            player_number += 1
        self.strategies_invoker_requests = invoker_request_sorted_array

    def get_processes(self):
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
                self.jury_report.status = "ERROR"
                return self.jury_report
            player_number += 1
        self.strategies_process = invoker_process_sorted_array

    def perform_play_command(self):
        try:
            play_command = self.play_process.stdout.readline()
        except RuntimeError:
            self.jury_report.status = "ERROR"
            return self.jury_report
        # play_command:
        # status: play data: player1: .... player2: ...
        # status: end points: player1: .... player2: ... story_of_game: ...
        if (len(play_command) < 12):
            self.jury_report.status = "ERROR"
            return self.jury_report
        if play_command[8:12] == "play":
            index = 19
            data_from_play_command = ""
            try:
                data_from_play_command = play_command[index]
            except RuntimeError:
                self.jury_report.status = "ERROR"
                return self.jury_report
            end_cycle = 0
            index += 1
            data_to_players = []
            player_index_end = []
            while (end_cycle == 0):
                try:
                    add_str = play_command[index]
                except RuntimeError:
                    self.jury_report.status = "ERROR"
                    return self.jury_report
                if (add_str == " "):
                    if (data_from_play_command[:6] == "player"):
                        player_index_end.append(index - 1)
                    data_from_play_command = ""
                else:
                    data_from_play_command += add_str
                index += 1
                if (len(player_index_end) == len(self.strategies_process)):
                    end_cycle = 1
            for i in range(len(player_index_end)):
                if (i != len(player_index_end) - 1):
                    data_to_players.append(play_command[player_index_end[i] + 2 :])
                else:
                    data_to_players.append(play_command[player_index_end[i] + 2 : player_index_end[i + 1] - 7])
            data_from_players = []
            for i in range(len(self.strategies_process)):
                player_data = self.strategies_process[i].connect(data_to_players[i])
                data_from_players.append(player_data)
            for i in range(len(data_from_players)):
                self.play_process.stdin.write(data_from_players[i] + '\n')
        else:
            self.game_state = GameState.END
            index = 20
            data_from_play_command = ""
            player = ""
            try:
                data_from_play_command = play_command[index]
            except RuntimeError:
                self.jury_report.status = "ERROR"
                return self.jury_report
            index += 1
            while (data_from_play_command != "story_of_game"):
                try:
                    add_str = play_command[index]
                except RuntimeError:
                    self.jury_report.status = "ERROR"
                    return self.jury_report
                if (add_str == " "):
                    if (data_from_play_command[:6] == "player"):
                        player = data_from_play_command[:len(data_from_play_command) - 1]
                    else:
                        self.jury_report.points[player] = data_from_play_command
                        player = ""
                    data_from_play_command = ""
                else:
                    data_from_play_command += add_str
                index += 1
            index += 2
            self.jury_report.story_of_game = play_command[index:]
            self.jury_report.status = "OK"
            return self.jury_report

    def notify_processes(self, processes):
        self.process = processes
        self.get_processes()
