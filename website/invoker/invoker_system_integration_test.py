from unittest.mock import patch, Mock
from django.test import TestCase

from .invoker import Invoker
from .invoker_request import InvokerRequest
from .models import InvokerReport
from .invoker_multi_request import InvokerMultiRequest, Priority
from .invoker_multi_request_priority_queue import InvokerMultiRequestPriorityQueue


class TestInvokerSystem(TestCase):
    #@patch('invoker.invoker_request.InvokerRequest.notify')
    @patch('invoker.invoker.Invoker.run')
    def test(self, mock_inv_run: Mock): #mock_i_r_notify: Mock):
        i_m_r_p_queue = InvokerMultiRequestPriorityQueue()

        command = 'python'
        file = '/home/user/PycharmProjects/Strategy_game/website/invoker/test_solutions/solution1.py'
        invoker_request = InvokerRequest(command=command, files=[file])
        invoker_multi_request = InvokerMultiRequest([invoker_request], Priority.RED)
        i_m_r_p_queue.invoker_multi_request_queue.put(invoker_multi_request)

        i_m_r_p_queue.run()

        mock_inv_run.assert_called()

        print(mock_inv_run.call_args)

