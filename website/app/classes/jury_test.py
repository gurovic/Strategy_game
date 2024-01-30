from django.test import TestCase
from unittest.mock import patch, Mock

from .jury import Jury

from invoker.invoker_process import InvokerProcess
from invoker.invoker_multi_request import InvokerMultiRequest
from invoker.invoker_request import InvokerRequest, InvokerRequestType


class TestJury(TestCase):
    @patch('app.classes.jury.Jury.get_processes')
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
        pass

    def test_perform_play_command(self):
        pass
