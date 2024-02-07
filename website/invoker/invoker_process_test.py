from abc import ABC

from django.test import TestCase
from unittest.mock import patch, Mock
from invoker.invoker import Invoker
from invoker.invoker import RunResult
from invoker.invoker_process import InvokerProcess
import typing


class TestInvokerProcess(TestCase):
    class InvokerProcessForTesting(InvokerProcess, ABC):
        def kill(self):
            pass

        def make_run_result(self) -> RunResult:
            pass

        def wait(self, timeout: typing.Optional[int] = None):
            pass

    @patch("invoker.invoker_process_test.TestInvokerProcess.InvokerProcessForTesting.kill")
    @patch("invoker.invoker_process_test.TestInvokerProcess.InvokerProcessForTesting.make_run_result")
    @patch("invoker.invoker_process_test.TestInvokerProcess.InvokerProcessForTesting.wait")
    def test_create(self, mock_kill: Mock, mock_make_run_result: Mock, mock_wait: Mock):
        invoker_process = self.InvokerProcessForTesting()

    @patch("invoker.invoker_process_test.TestInvokerProcess.InvokerProcessForTesting.kill")
    @patch("invoker.invoker_process_test.TestInvokerProcess.InvokerProcessForTesting.make_run_result")
    @patch("invoker.invoker_process_test.TestInvokerProcess.InvokerProcessForTesting.wait")
    def test_with_callback(self, mock_kill: Mock, mock_make_run_result: Mock, mock_wait: Mock):
        mock_callback = Mock()
        invoker_process = self.InvokerProcessForTesting(callback=mock_callback)
        mock_kill.assert_called()
        mock_make_run_result.assert_called()
