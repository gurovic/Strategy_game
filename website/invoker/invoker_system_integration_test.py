from unittest.mock import patch, Mock
from django.test import TestCase

from .invoker import Invoker
from .invoker_request import InvokerRequest
from .models import InvokerReport
from .invoker_multi_request import InvokerMultiRequest, Priority
from .invoker_multi_request_priority_queue import InvokerMultiRequestPriorityQueue


class TestInvokerSystem(TestCase):
    @patch('invoker.invoker_multi_request.InvokerMultiRequest.notify')
    @patch('website.settings.MAX_INVOKERS_COUNT')
    def test(self, mock_max_invoker_count: Mock, mock_i_m_r_notify: Mock):
        mock_max_invoker_count.return_value(1)
        mock_i_m_r_notify.return_value = InvokerMultiRequest.notify

        i_m_r_p_queue = InvokerMultiRequestPriorityQueue()

        command = 'python'
        file = './test_solutions/solution1.py'
        invoker_request1 = InvokerRequest(command=command, files=[file])
        invoker_multi_request = InvokerMultiRequest([invoker_request1], Priority.RED)
        i_m_r_p_queue.invoker_multi_request_queue.put(invoker_multi_request)

        i_m_r_p_queue.run()

        mock_i_m_r_notify.assert_called()

        print(mock_i_m_r_notify.call_args)

