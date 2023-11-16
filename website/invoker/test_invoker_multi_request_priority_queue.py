from django.test import TestCase
from unittest.mock import patch

from threading import Thread

from invoker.invoker_multi_request_priority_queue import InvokerMultiRequestPriorityQueue
from invoker.invoker_multi_request import InvokerMultiRequest, Priority


class TestInvokerMultiRequestPriorityQueue(TestCase):
    def test_unique(self):
        first_queue = InvokerMultiRequestPriorityQueue()
        second_queue = InvokerMultiRequestPriorityQueue()
        self.assertEqual(id(first_queue), id(second_queue))

    def test_async_unique(self):
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

    @patch("invoker.invoker_multi_request_priority_queue.InvokerMultiRequestPriorityQueue.run")
    @patch("invoker.invoker_multi_request_priority_queue.InvokerMultiRequest")
    def test_addition(self, mock_invoker_multi_request, mock_run):
        class TempQueue(InvokerMultiRequestPriorityQueue):
            pass

        queue = TempQueue()
        queue.add(mock_invoker_multi_request, 0)
        self.assertEqual(queue.invoker_multi_request_queue.qsize(), 1)
        self.assertTrue(mock_run.called)

    @patch("invoker.invoker_multi_request_priority_queue.InvokerMultiRequestPriorityQueue.run")
    def test_notify(self, mock_run):
        queue = InvokerMultiRequestPriorityQueue()
        queue.notify()
        self.assertTrue(mock_run.called)

    @patch("invoker.invoker_multi_request_priority_queue.InvokerMultiRequest")
    @patch("invoker.invoker_multi_request_priority_queue.InvokerPool")
    def test_run_one_possible(self, mock_invoker_pool, mock_invoker_multi_request):
        class TempQueue(InvokerMultiRequestPriorityQueue):
            pass

        queue = TempQueue()
        mock_invoker_pool.free_invokers_count = 4
        mock_invoker_pool.get.return_value = [0, 1, 2, 3]
        queue.invoker_pool = mock_invoker_pool
        mock_invoker_multi_request.invoker_requests_count = 4
        queue.invoker_multi_request_queue.put((0, mock_invoker_multi_request))
        queue.run()
        self.assertEqual(queue.invoker_multi_request_queue.qsize(), 0)

    @patch("invoker.invoker_multi_request_priority_queue.InvokerPool")
    @patch("invoker.invoker_multi_request_priority_queue.InvokerMultiRequest.run")
    def test_run_mixed(self, mock_imr_run, mock_invoker_pool):
        class TempQueue(InvokerMultiRequestPriorityQueue):
            pass

        queue = TempQueue()

        queue.invoker_pool.free_invokers_count = 4
        queue.invoker_pool.get.return_value = [0, 1, 2, 3]

        for i in range(3):
            mock_invoker_multi_request = InvokerMultiRequest([], i)
            mock_invoker_multi_request.run = mock_imr_run
            mock_invoker_multi_request.invoker_requests_count = 4
            queue.invoker_multi_request_queue.put((i, mock_invoker_multi_request))

        for i in range(3):
            mock_invoker_multi_request = InvokerMultiRequest([], i)
            mock_invoker_multi_request.run = mock_imr_run
            mock_invoker_multi_request.invoker_requests_count = 6
            queue.invoker_multi_request_queue.put((i, mock_invoker_multi_request))
        queue.run()
        self.assertEqual(queue.invoker_multi_request_queue.qsize(), 5)

    @patch("invoker.invoker_multi_request_priority_queue.InvokerPool")
    @patch("invoker.invoker_multi_request_priority_queue.InvokerMultiRequest.run")
    def test_add_then_run_overflow_request_count(self, mock_imr_run, mock_invoker_pool):
        class TempQueue(InvokerMultiRequestPriorityQueue):
            pass

        queue = TempQueue()
        queue.invoker_pool.free_invokers_count = 4
        queue.invoker_pool.get.return_value = [0, 1, 2, 3]
        invoker_multi_request = InvokerMultiRequest([])
        invoker_multi_request.run = mock_imr_run
        invoker_multi_request.invoker_requests_count = 100
        queue.add(invoker_multi_request, Priority.RED)
        self.assertEqual(queue.invoker_multi_request_queue.qsize(), 1)

    @patch("invoker.invoker_multi_request_priority_queue.InvokerPool")
    @patch("invoker.invoker_multi_request_priority_queue.InvokerMultiRequest.run")
    def test_add_then_run(self, mock_imr_run, mock_invoker_pool):
        class TempQueue(InvokerMultiRequestPriorityQueue):
            pass

        queue = TempQueue()
        invoker_requests_count = [1, 2, 3, 4]
        for i in range(100):
            queue.invoker_pool.free_invokers_count = 4
            queue.invoker_pool.get.return_value = [0, ] * invoker_requests_count[i % 4]
            invoker_multi_request = InvokerMultiRequest([])
            invoker_multi_request.run = mock_imr_run
            invoker_multi_request.invoker_requests_count = invoker_requests_count[i % 4]
            queue.add(invoker_multi_request, Priority.GREEN)
            self.assertEqual(queue.invoker_multi_request_queue.qsize(), 0)
            self.assertTrue(invoker_multi_request.run.called)

    @patch("invoker.invoker_multi_request_priority_queue.InvokerPool")
    @patch("invoker.invoker_multi_request_priority_queue.InvokerMultiRequest.run")
    def test_add_multiple_then_run(self, mock_imr_run, mock_invoker_pool):
        class TempQueue(InvokerMultiRequestPriorityQueue):
            pass

        queue = TempQueue()
        invoker_requests_count = [1, 2, 3, 4]
        for i in range(100):
            queue.invoker_pool.free_invokers_count = 4
            queue.invoker_pool.get.return_value = [0, ] * invoker_requests_count[i % 4]
            invoker_multi_request = InvokerMultiRequest([])
            invoker_multi_request.run = mock_imr_run
            invoker_multi_request.invoker_requests_count = invoker_requests_count[i % 4]
            queue.invoker_multi_request_queue.put((Priority.RED, invoker_multi_request))
        queue.run()
        self.assertEqual(queue.invoker_multi_request_queue.qsize(), 0)
