import enum
import typing

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
    def __init__(self):
        self.process = None
        self.play_process = None
        self.strategies_process = []

        self.game_state = GameState.PLAY
        self.jury_report = JuryReport()
        self.jury_report.status = ""
        self.jury_report.points = {}
        self.jury_report.story_of_game = ""

    def play_process_callback(self, process):
        self.play_process = process

    def strategy_process_callback(self, process):
        self.strategies_process.append(process)

    def perform_play_command(self):
        try:
            play_command = self.play_process.connect(None)
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
                if (i == len(player_index_end) - 1):
                    data_to_players.append(play_command[player_index_end[i] + 2:])
                else:
                    data_to_players.append(play_command[player_index_end[i] + 2: player_index_end[i + 1] - 8])
            data_from_players = []
            for i in range(len(data_to_players)):
                if (data_to_players[i] != "None"):
                    player_data = self.strategies_process[i].connect(data_to_players[i])
                    # self.strategies_process[i].stdin = data_to_players[i]   not as should be, needs a change
                else:
                    player_data = ""
                    # self.strategies_process[i].stdin = ""
                # player_data = self.strategies_process[i].stdout
                data_from_players.append(player_data)
            # self.play_process.stdin = "" #not as should be, needs a change
            for i in range(len(data_from_players)):
                blank_str = self.play_process.connect(data_from_players[i])
                # self.play_process.stdin += data_from_players[i] #not as should be, needs a change
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
                        self.jury_report.points[player] = int(data_from_play_command)
                        player = ""
                    data_from_play_command = ""
                else:
                    data_from_play_command += add_str
                index += 1
            index += 2
            self.jury_report.story_of_game = play_command[index:]
            self.jury_report.status = "OK"
            return self.jury_report
