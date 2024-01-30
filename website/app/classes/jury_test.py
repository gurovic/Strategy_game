from django.test import TestCase
from unittest.mock import patch, Mock

from .jury import Jury

from invoker.invoker_process import InvokerProcess
from invoker.invoker_multi_request import InvokerMultiRequest
from invoker.invoker_request import InvokerRequest, InvokerRequestType


class TestJury(TestCase):
    @patch('app.classes.jury.Jury.get_processes')
    def test_get_invoker_requests(self, mock_get_processes: Mock):
        pass

    def test_get_processes(self):
        pass

    def test_perform_play_command(self):
        pass
