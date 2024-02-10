from django.test import TestCase
from unittest.mock import patch, Mock

from .jury import Jury

from invoker.invoker_multi_request import InvokerMultiRequest
from invoker.invoker_request import InvokerRequest, InvokerRequestType
from invoker.invoker_process import InvokerProcess


class TestJury(TestCase):
    @patch("app.classes.jury.Jury.get_processes")
    def test_get_invoker_requests(self, mock_get_processes: Mock):
        play_invoker_request = InvokerRequest("command")
        play_invoker_request.type = InvokerRequestType.PLAY
        strategy_invoker_request = InvokerRequest("command")
        strategy_invoker_request.type = InvokerRequestType.STRATEGY

        invoker_multi_request = InvokerMultiRequest([play_invoker_request, strategy_invoker_request])

        jury = Jury(invoker_multi_request)

        self.assertEqual(jury.play_invoker_request, play_invoker_request)
        self.assertEqual(jury.strategies_invoker_requests, [strategy_invoker_request])

    def test_get_processes(self):
        play_process = InvokerProcess()
        play_invoker_request = InvokerRequest("command")
        play_invoker_request.type = InvokerRequestType.PLAY
        play_invoker_request.process_callback = play_process

        strategy_process = InvokerProcess()
        strategy_invoker_request = InvokerRequest("command")
        strategy_invoker_request.type = InvokerRequestType.STRATEGY
        strategy_invoker_request.process_callback = strategy_process

        invoker_multi_request = InvokerMultiRequest([strategy_invoker_request, play_invoker_request])

        jury = Jury(invoker_multi_request)

        self.assertEqual(jury.play_process, play_process)
        self.assertEqual(jury.strategies_process, [strategy_process])

    @patch("app.classes.jury.Jury.get_invoker_requests")
    @patch("app.classes.jury.Jury.get_processes")
    @patch("invoker.invoker_process.InvokerProcess.read")
    @patch("invoker.invoker_process.InvokerProcess.write")
    def test_perform_play_command(self, mock_write: Mock, mock_read: Mock, mock_get_processes: Mock, mock_get_invoker_requests: Mock):
        play_command = {"state": "play", "player": 1, "data": "some data to player"}
        mock_read.return_value = play_command

        invoker_multi_request = Mock()
        jury = Jury(invoker_multi_request)
        jury.play_process = InvokerProcess()
        jury.strategies_process = [InvokerProcess()]

        jury.perform_play_command()

        mock_write.assert_called_with("some data to player")
