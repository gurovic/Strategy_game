from django.test import TestCase
from unittest.mock import patch, Mock

from invoker.invoker_multi_request import InvokerMultiRequest, Priority
from invoker.invoker_request import InvokerRequest
from invoker.models import InvokerReport
from invoker.invoker import Invoker, InvokerProcess


class TestInvokerMultiRequest(TestCase):
    @patch("invoker.invoker_multi_request.InvokerRequest")
    @patch("invoker.invoker_multi_request.InvokerMultiRequestPriorityQueue")
    def test_start(self, mock_queue: Mock, mock_request: Mock):
        invoker_multi_request = InvokerMultiRequest([mock_request])
        invoker_multi_request.start()
        mock_queue = mock_queue()
        mock_add = mock_queue.add
        mock_add.assert_called_with(invoker_multi_request)

    @patch("invoker.invoker.Invoker")
    @patch("invoker.invoker_multi_request.InvokerRequest")
    def test_run(self, mock_request: Mock, mock_invoker: Mock):
        invoker_requests = [mock_request() for _ in range(3)]
        invokers = [mock_invoker() for _ in range(3)]

        invoker_multi_request = InvokerMultiRequest(invoker_requests)
        invoker_multi_request.run(invokers)

        for (invoker, request) in zip(invokers, invoker_requests):
            request.run.assert_called_with(invoker)

    @patch("invoker.invoker_multi_request.InvokerRequest")
    def test_notify(self, mock_request: Mock):
        mock = Mock()

        invoker_report = InvokerReport()

        invoker_multi_request = InvokerMultiRequest([mock_request])
        invoker_multi_request.subscribers = [mock]

        invoker_multi_request.notify(invoker_report)
        mock.notify.assert_called()

    @patch("invoker.invoker_multi_request.InvokerRequest")
    def test_not_all_notify(self, mock_request: Mock):
        mock = Mock()

        invoker_requests = [mock_request for _ in range(2)]
        invoker_report = InvokerReport()

        invoker_multi_request = InvokerMultiRequest(invoker_requests)
        invoker_multi_request.subscribers = [mock]

        invoker_multi_request.notify(invoker_report)
        mock.notify.assert_not_called()

    @patch("invoker.invoker_multi_request.InvokerRequest")
    def test_all_notify(self, mock_request: Mock):
        mock = Mock()

        invoker_requests = [mock_request for _ in range(3)]
        invoker_reports = [InvokerReport() for _ in range(3)]

        invoker_multi_request = InvokerMultiRequest(invoker_requests)
        invoker_multi_request.subscribers = [mock]

        for invoker_report in invoker_reports:
            invoker_multi_request.notify(invoker_report)

        mock.notify.assert_called_with(invoker_reports)

    def test_send_processes(self):
        mock = Mock()

        invoker_requests = []
        for index in range(3):
            invoker_requests.append(Mock())
        invoker_process_callbacks = [Mock() for _ in range(3)]

        for index in range(3):
            invoker_requests[index].process = invoker_process_callbacks[index]

        invoker_multi_request = InvokerMultiRequest(invoker_requests)
        invoker_multi_request.subscribers = [mock]

        invoker_multi_request.send_process()

        mock.notify_processes.assert_called_with(invoker_process_callbacks)

    def test_subscribe(self):
        mock = Mock()
        invoker_multi_request = InvokerMultiRequest([])
        invoker_multi_request.subscribe(mock)
        self.assertEqual(invoker_multi_request.subscribers[0], mock)
