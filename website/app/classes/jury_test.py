from unittest.mock import patch, Mock
import unittest

from invoker.invoker_multi_request import InvokerMultiRequest
from invoker.invoker_request import InvokerRequest
from invoker.invoker import NormalProcess
from app.classes.jury import Jury


class TestJury(unittest.TestCase):

    process = None

    def notify_processes(self, processes):
        self.process = processes

    @patch("app.classes.jury.Jury.get_processes")
    def test_get_invoker_requests(self, mock_get_processes: Mock):
        play_invoker_request = InvokerRequest("command")
        play_invoker_request.label = "play"

        strategy_invoker_request1 = InvokerRequest("command1")
        strategy_invoker_request1.label = "player1"
        strategy_invoker_request2 = InvokerRequest("command2")
        strategy_invoker_request2.label = "player2"

        invoker_multi_request = InvokerMultiRequest([play_invoker_request, strategy_invoker_request1, strategy_invoker_request2])

        jury = Jury(invoker_multi_request)

        self.assertEqual(jury.play_invoker_request, play_invoker_request)
        self.assertEqual(jury.strategies_invoker_requests, [strategy_invoker_request1, strategy_invoker_request2])

    def test_get_processes(self):

        play_mock_process = NormalProcess(Mock(), label="play")
        strategy_mock_process_1 = NormalProcess(Mock(), label="player1")
        strategy_mock_process_2 = NormalProcess(Mock(), label="player2")

        play_invoker_request = InvokerRequest("command", process_callback=play_mock_process)
        play_invoker_request.label = "play"
        play_process = play_invoker_request.process_callback

        strategy_invoker_request1 = InvokerRequest("command1", process_callback=strategy_mock_process_1)
        strategy_invoker_request1.label = "player1"
        strategy_invoker_request2 = InvokerRequest("command2", process_callback=strategy_mock_process_2)
        strategy_invoker_request2.label = "player2"
        strategy_processes = [strategy_invoker_request1.process_callback, strategy_invoker_request2.process_callback]

        invoker_multi_request = InvokerMultiRequest([play_invoker_request, strategy_invoker_request2, strategy_invoker_request1])

        jury = Jury(invoker_multi_request)

        invoker_multi_request.subscribe(jury)

        invoker_multi_request.send_process()

        self.assertEqual(jury.play_process, play_process)
        self.assertEqual(jury.strategies_process, strategy_processes)

    def test_perform_play_command_ended(self):

        play_command = "status: end points: player1: 5 player2: 4 story_of_game: smth"

        play_mock_process = NormalProcess(Mock(), label="play")
        play_mock_process.stdout = play_command
        strategy_mock_process_1 = NormalProcess(Mock(), label="player1")
        strategy_mock_process_2 = NormalProcess(Mock(), label="player2")

        play_invoker_request = InvokerRequest("command", process_callback=play_mock_process)
        play_invoker_request.label = "play"
        play_process = play_invoker_request.process_callback

        strategy_invoker_request1 = InvokerRequest("command1", process_callback=strategy_mock_process_1)
        strategy_invoker_request1.label = "player1"
        strategy_invoker_request2 = InvokerRequest("command2", process_callback=strategy_mock_process_2)
        strategy_invoker_request2.label = "player2"
        strategy_processes = [strategy_invoker_request1.process_callback, strategy_invoker_request2.process_callback]

        invoker_multi_request = InvokerMultiRequest([play_invoker_request, strategy_invoker_request2, strategy_invoker_request1])

        jury = Jury(invoker_multi_request)

        invoker_multi_request.subscribe(jury)
        invoker_multi_request.send_process()

        jury.perform_play_command()

        points_dict = {"player1": 5, "player2": 4}

        self.assertEqual(jury.jury_report.status, "OK")
        self.assertEqual(jury.jury_report.story_of_game, "smth")
        self.assertEqual(jury.jury_report.points, points_dict)

