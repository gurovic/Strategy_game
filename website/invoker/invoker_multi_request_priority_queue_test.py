from django.test import TestCase
from unittest.mock import patch, Mock

from threading import Thread

from invoker.invoker_multi_request_priority_queue import InvokerMultiRequestPriorityQueue
from invoker.invoker_multi_request import InvokerMultiRequest, Priority


class TestInvokerMultiRequestPriorityQueue(TestCase):

    @patch("invoker.invoker_multi_request_priority_queue.InvokerPool")
    def test_unique(self, mock_pool):
        first_queue = InvokerMultiRequestPriorityQueue()
        second_queue = InvokerMultiRequestPriorityQueue()
        self.assertEqual(id(first_queue), id(second_queue))

    @patch("invoker.invoker_multi_request_priority_queue.InvokerPool")
    def test_async_unique(self, mock_pool):
        queues = []

        def create():
            queues.append(InvokerMultiRequestPriorityQueue())

        creator1 = Thread(target=create, args=())
        creator2 = Thread(target=create, args=())
        creator1.start()
        creator2.start()
        creator1.join()
        creator2.join()
        self.assertEqual(queues[0], queues[1])

    @patch("invoker.invoker_multi_request_priority_queue.InvokerPool")
    @patch("invoker.invoker_multi_request_priority_queue.InvokerMultiRequestPriorityQueue.run")
    def test_addition(self, mock_run: Mock, mock_invoker_pool: Mock):
        class TempQueue(InvokerMultiRequestPriorityQueue):
            pass

        queue = TempQueue()
        queue.invoker_pool = mock_invoker_pool
        mock_invoker_multi_request = InvokerMultiRequest([], Priority.GREEN)
        queue.add(mock_invoker_multi_request)
        self.assertEqual(queue.invoker_multi_request_queue.qsize(), 1)
        self.assertTrue(mock_run.called)

    @patch("invoker.invoker_multi_request_priority_queue.InvokerPool")
    @patch("invoker.invoker_multi_request_priority_queue.InvokerMultiRequestPriorityQueue.run")
    def test_notify(self, mock_run: Mock, mock_invoker_pool: Mock):
        queue = InvokerMultiRequestPriorityQueue()
        queue.invoker_pool = mock_invoker_pool
        queue.notify()
        self.assertTrue(mock_run.called)

    @patch("invoker.invoker_multi_request_priority_queue.InvokerPool")
    @patch("invoker.invoker_multi_request.InvokerMultiRequest")
    def test_run_one_possible(self, mock_invoker_multi_request: Mock, mock_invoker_pool: Mock):
        class TempQueue(InvokerMultiRequestPriorityQueue):
            pass

        queue = TempQueue()
        mock_invoker_pool.free_invokers_count = 4
        mock_invoker_pool.get.return_value = [0, 1, 2, 3]
        queue.invoker_pool = mock_invoker_pool
        mock_invoker_multi_request.invoker_requests_count = 4
        mock_invoker_multi_request.priority = Priority.YELLOW
        queue.invoker_multi_request_queue.put(mock_invoker_multi_request)
        queue.run()
        self.assertEqual(queue.invoker_multi_request_queue.qsize(), 0)

    @patch("invoker.invoker_multi_request_priority_queue.InvokerPool")
    @patch("invoker.invoker_multi_request.InvokerMultiRequest.run")
    def test_run_mixed(self, mock_imr_run: Mock, mock_invoker_pool: Mock):
        class TempQueue(InvokerMultiRequestPriorityQueue):
            pass

        queue = TempQueue()
        queue.invoker_pool = mock_invoker_pool
        queue.invoker_pool.free_invokers_count = 4
        queue.invoker_pool.get.return_value = [0, 1, 2, 3]

        for i in range(3):
            mock_invoker_multi_request = InvokerMultiRequest([], i)
            mock_invoker_multi_request.run = mock_imr_run
            mock_invoker_multi_request.invoker_requests_count = 4
            queue.invoker_multi_request_queue.put(mock_invoker_multi_request)

        for i in range(3):
            mock_invoker_multi_request = InvokerMultiRequest([], i)
            mock_invoker_multi_request.run = mock_imr_run
            mock_invoker_multi_request.invoker_requests_count = 6
            queue.invoker_multi_request_queue.put(mock_invoker_multi_request)
        queue.run()
        self.assertEqual(queue.invoker_multi_request_queue.qsize(), 5)

    @patch("invoker.invoker_multi_request_priority_queue.InvokerPool")
    @patch("invoker.invoker_multi_request.InvokerMultiRequest.run")
    def test_add_then_run_overflow_request_count(self, mock_imr_run: Mock, mock_invoker_pool: Mock):
        class TempQueue(InvokerMultiRequestPriorityQueue):
            pass

        queue = TempQueue()
        queue.invoker_pool = mock_invoker_pool
        queue.invoker_pool.free_invokers_count = 4
        queue.invoker_pool.get.return_value = [0, 1, 2, 3]
        invoker_multi_request = InvokerMultiRequest([])
        invoker_multi_request.run = mock_imr_run
        invoker_multi_request.invoker_requests_count = 100
        invoker_multi_request.priority = Priority.RED
        queue.add(invoker_multi_request)
        self.assertEqual(queue.invoker_multi_request_queue.qsize(), 1)

    @patch("invoker.invoker_multi_request_priority_queue.InvokerPool")
    @patch("invoker.invoker_multi_request.InvokerMultiRequest.run")
    def test_add_then_run(self, mock_imr_run: Mock, mock_invoker_pool: Mock):
        class TempQueue(InvokerMultiRequestPriorityQueue):
            pass

        queue = TempQueue()
        queue.invoker_pool = mock_invoker_pool
        invoker_requests_count = [1, 2, 3, 4]
        for i in range(100):
            queue.invoker_pool.free_invokers_count = 6
            queue.invoker_pool.get.return_value = [0, ] * invoker_requests_count[i % 4]
            invoker_multi_request = InvokerMultiRequest([])
            invoker_multi_request.run = mock_imr_run
            invoker_multi_request.invoker_requests_count = invoker_requests_count[i % 4]
            invoker_multi_request.priority = Priority.GREEN
            queue.add(invoker_multi_request)
            self.assertEqual(queue.invoker_multi_request_queue.qsize(), 0)
            self.assertTrue(invoker_multi_request.run.called)

    @patch("invoker.invoker_multi_request_priority_queue.InvokerPool")
    @patch("invoker.invoker_multi_request.InvokerMultiRequest.run")
    def test_add_multiple_then_run(self, mock_imr_run: Mock, mock_invoker_pool: Mock):
        class TempQueue(InvokerMultiRequestPriorityQueue):
            pass

        queue = TempQueue()
        queue.invoker_pool = mock_invoker_pool
        invoker_requests_count = [1, 2, 3, 4]
        for i in range(100):
            queue.invoker_pool.free_invokers_count = 4
            queue.invoker_pool.get.return_value = [0, ] * invoker_requests_count[i % 4]
            invoker_multi_request = InvokerMultiRequest([])
            invoker_multi_request.run = mock_imr_run
            invoker_multi_request.invoker_requests_count = invoker_requests_count[i % 4]
            invoker_multi_request.priority = Priority.RED
            queue.invoker_multi_request_queue.put(invoker_multi_request)
        queue.run()
        self.assertEqual(queue.invoker_multi_request_queue.qsize(), 0)
