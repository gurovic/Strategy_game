from django.test import TestCase
from unittest.mock import patch, Mock

from .jury import Jury
from ...invoker.invoker_multi_request import InvokerMultiRequest
from ...invoker.invoker_request import InvokerRequest
from ...invoker.invoker_process import InvokerProcess


class TestJury(TestCase):
    @patch("invoker.invoker_multi_request.InvokerMultiRequest.invoker_requests")
    def test_get_invoker_requests(self, mock_invoker_requests: Mock):
        play_invoker_request = InvokerRequest("command")
        play_invoker_request.type = InvokerRequestType.PLAY
        strategy_invoker_request = InvokerRequest("command")
        strategy_invoker_request.type = InvokerRequestType.STRATEGY

        mock_invoker_requests.return_value = [play_invoker_request, strategy_invoker_request]

        invoker_multi_request = InvokerMultiRequest([play_invoker_request, strategy_invoker_request])

        jury = Jury(invoker_multi_request)

        self.assertEqual(jury.play_invoker_request, play_invoker_request)
        self.assertEqual(jury.strategies_invoker_requests,[strategy_invoker_request])

    @patch("app.classes.jury.Jury.get_invoker_requests")
    @patch("app.classes.jury.Jury.play_invoker_request.process_callback")
    @patch("app.classes.jury.Jury.strategies_invoker_requests")
    def test_get_processes(self, mock_strategies_invoker_requests: Mock, mock_play_process: Mock, mock_get_invoker_requests: Mock):
        mock_play_process.return_value = InvokerProcess()
        strategy_process = InvokerProcess()

        strategy_invoker_request = InvokerRequest("command")
        strategy_invoker_request.process_callback = strategy_process
        mock_strategies_invoker_requests.return_value = [strategy_invoker_request]

        invoker_multi_request = InvokerMultiRequest([])

        jury = Jury(invoker_multi_request)

        self.assertEqual(jury.play_process, mock_play_process)
        self.assertEqual(jury.strategies_process, [strategy_process])

