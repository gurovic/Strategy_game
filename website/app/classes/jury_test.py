from django.test import TestCase
from unittest.mock import patch, Mock

from .jury import Jury
from ...invoker.invoker import InvokerProcess
from ...invoker.invoker_multi_request import InvokerMultiRequest
from ...invoker.invoker_request import InvokerRequest


class TestJury(TestCase):
    @patch("invoker.invoker.InvokerProcess.rear")
    @patch("invoker.invoker.InvokerProcess.write")
    def test_perform_play_command(self, mock_read: Mock, mock_write: Mock):
        play_command = {"state": "play", "player": 1, "data": "some data to player"}

        mock_read.return_value = play_command

        invoker_multi_request = Mock()
        jury = Jury(invoker_multi_request)
        jury.play_process = InvokerProcess()
        jury.strategies_process = [InvokerProcess()]

        jury.perform_play_command()

        mock_write.assert_called_with("some data to player")
