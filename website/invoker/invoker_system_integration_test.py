from unittest.mock import patch, Mock
from django.test import TestCase

from .invoker_request import InvokerRequest, InvokerRequestType
from .invoker_multi_request import InvokerMultiRequest, Priority
from .invoker_multi_request_priority_queue import InvokerMultiRequestPriorityQueue


class TestInvokerSystem(TestCase):
    @patch('invoker.invoker_multi_request.InvokerMultiRequest.run')
    @patch('website.settings.MAX_INVOKERS_COUNT')
    def test(self, mock_max_invoker_count: Mock, mock_imr_run: Mock):
        mock_max_invoker_count.return_value(1)

        i_m_r_p_queue = InvokerMultiRequestPriorityQueue()

        invoker_request1 = InvokerRequest('python ../libgame/examples/bolshe_menshe_data/bolshe_menshe_solution1.py')
        invoker_multi_request1 = InvokerMultiRequest([invoker_request1], Priority.RED)

        invoker_request2 = InvokerRequest('python ../libgame/examples/bolshe_menshe_data/bolshe_menshe_solution2.py')
        invoker_multi_request2 = InvokerMultiRequest([invoker_request2], Priority.YELLOW)

        i_m_r_p_queue.invoker_multi_request_queue.put(invoker_multi_request1)
        i_m_r_p_queue.invoker_multi_request_queue.put(invoker_multi_request2)

        i_m_r_p_queue.run()

        mock_imr_run.assert_called()
