from django.test import TestCase
from unittest.mock import patch, Mock

from invoker.invoker_multi_request import InvokerMultiRequest, Priority
from invoker.invoker_request import InvokerRequest
from invoker.models import InvokerReport
from invoker.invoker import Invoker


class TestInvokerMultiRequest(TestCase):
    @patch("invoker.invoker_multi_request_priority_queue.InvokerMultiRequestPriorityQueue.add")
    def test_start(self, mock_queue_add: Mock):
        invoker_request = InvokerRequest("Test")

        invoker_multi_request = InvokerMultiRequest([invoker_request])
        invoker_multi_request.start()

        mock_queue_add.assert_called_with(invoker_multi_request)

    @patch("invoker.invoker_request.InvokerRequest.run")
    def test_run(self, mock_request_run: Mock):
        invoker_requests = [InvokerRequest("Test") for _ in range(3)]
        invokers = [Invoker() for _ in range(3)]

        invoker_multi_request = InvokerMultiRequest(invoker_requests)
        invoker_multi_request.run(invokers)

        for invoker in invokers:
            mock_request_run.assert_any_call(invoker)

    def test_notify(self):
        mock = Mock()

        invoker_request = InvokerRequest("Test")
        invoker_report = InvokerReport()

        invoker_multi_request = InvokerMultiRequest([invoker_request])
        invoker_multi_request.subscribers = [mock]

        invoker_multi_request.notify(invoker_report)
        mock.notify.assert_called()

    def test_not_all_notify(self):
        mock = Mock()

        invoker_requests = [InvokerRequest("Test") for _ in range(2)]
        invoker_report = InvokerReport()

        invoker_multi_request = InvokerMultiRequest(invoker_requests)
        invoker_multi_request.subscribers = [mock]

        invoker_multi_request.notify(invoker_report)
        mock.notify.assert_not_called()

    def test_all_notify(self):
        mock = Mock()

        invoker_requests = [InvokerRequest("Test") for _ in range(3)]
        invoker_reports = [InvokerReport() for _ in range(3)]

        invoker_multi_request = InvokerMultiRequest(invoker_requests)
        invoker_multi_request.subscribers = [mock]

        for invoker_report in invoker_reports:
            invoker_multi_request.notify(invoker_report)

        mock.notify.assert_called_with(invoker_reports)

