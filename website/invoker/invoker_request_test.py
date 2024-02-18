from django.test import TestCase
from unittest.mock import patch, Mock

from invoker.invoker_request import InvokerRequest
from invoker.invoker import Invoker


class TestInvokerRequest(TestCase):
    @patch("invoker.invoker.Invoker.run")
    def test_run(self, mock_invoker_run: Mock):
        invoker = Invoker()

        invoker_request = InvokerRequest("echo Hello World", files=["test.test"], preserve_files=["test.test"])
        invoker_request.run(invoker)

        mock_invoker_run.assert_called_with("echo Hello World", files=["test.test"], preserve_files=["test.test"],
                                            callback=invoker_request.notify)

    @patch("invoker.models.InvokerReport")
    def test_notify(self, mock_invoker_report: Mock):
        mock = Mock()
        invoker_request = InvokerRequest("echo Hello World")
        invoker_request.report_callback = mock
        invoker_request.notify(mock_invoker_report)
        mock.assert_called()
