import unittest
from unittest.mock import patch

from threading import Thread

from .invoker_multi_request_priority_queue import InvokerMultiRequestPriorityQueue
from .invoker_multi_request import InvokerMultiRequest
from .invoker_pool import InvokerPool


class TestInvokerMultiRequestPriorityQueue(unittest.TestCase):
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
        self.assertEqual(queues[0], queues[1])

    @patch(f"{__name__}.InvokerMultiRequest")
    @patch("invoker.invoker_multi_request_priority_queue.InvokerMultiRequestPriorityQueue.run")
    def test_addition(self, mock_invoker_multi_request, mock_run):
        class TempQueue(InvokerMultiRequestPriorityQueue):
            pass

        queue = TempQueue()
        queue.add(mock_invoker_multi_request, 0)
        self.assertEqual(queue.invoker_multi_request_queue.qsize(), 1)

    @patch(f"{__name__}.InvokerMultiRequest")
    @patch("invoker.invoker_multi_request_priority_queue.InvokerMultiRequestPriorityQueue.run")
    def test_notify(self, mock_invoker_multi_request, mock_run):
        queue = InvokerMultiRequestPriorityQueue()
        queue.add(mock_invoker_multi_request, 0)
        queue.notify()

    @patch("invoker.invoker_multi_request_priority_queue.InvokerPool")
    @patch(f"{__name__}.InvokerMultiRequest")
    def test_run_one_possible(self, mock_invoker_pool, mock_invoker_multi_request):
        class TempQueue(InvokerMultiRequestPriorityQueue):
            pass

        queue = TempQueue()
        prev_invoker_pool = queue.invoker_pool
        mock_invoker_pool.get_free_invokers_count.return_value = 4
        mock_invoker_pool.get.return_value = [0, 1, 2, 3]
        queue.invoker_pool = mock_invoker_pool
        mock_invoker_multi_request.invoker_requests_count = 4
        queue.invoker_multi_request_queue.put((0, mock_invoker_multi_request))
        queue.run()
        self.assertEqual(queue.invoker_multi_request_queue.qsize(), 0)

    @patch("invoker.invoker_multi_request_priority_queue.InvokerPool")
    @patch(f"{__name__}.InvokerMultiRequest.run")
    def test_run_mixed(self, mock_invoker_pool, mock_imr_run):
        class TempQueue(InvokerMultiRequestPriorityQueue):
            pass

        queue = TempQueue()

        mock_invoker_pool.get_free_invokers_count.return_value = 4
        mock_invoker_pool.get.return_value = [0, 1, 2, 3]
        queue.invoker_pool = mock_invoker_pool

        for i in [1, 5, 8]:
            mock_invoker_multi_request = InvokerMultiRequest()
            mock_invoker_multi_request.run = mock_imr_run
            mock_invoker_multi_request.invoker_requests_count = 4
            queue.add(mock_invoker_multi_request, i)

        for i in [7, 10, 11]:
            mock_invoker_multi_request = InvokerMultiRequest()
            mock_invoker_multi_request.run = mock_imr_run
            mock_invoker_multi_request.invoker_requests_count = 6
            queue.add(mock_invoker_multi_request, i)

        queue.run()
        self.assertEqual(queue.invoker_multi_request_queue.qsize(), 4)

    @patch("invoker.invoker_multi_request_priority_queue.InvokerPool")
    @patch(f"{__name__}.InvokerMultiRequest.run")
    def test_add_then_run_overflow_request_count(self, mock_invoker_pool, mock_imr_run):
        class TempQueue(InvokerMultiRequestPriorityQueue):
            pass

        queue = TempQueue()
        prev_invoker_pool = queue.invoker_pool
        mock_invoker_pool.get_free_invokers_count.return_value = 4
        mock_invoker_pool.get.return_value = [0, 1, 2, 3]
        invoker_multi_request = InvokerMultiRequest()
        invoker_multi_request.run = mock_imr_run
        invoker_multi_request.invoker_requests_count = 100
        invoker_multi_request.id = 12345
        queue.invoker_pool = mock_invoker_pool
        queue.add(invoker_multi_request, 0)
        queue.run()
        self.assertEqual(queue.invoker_multi_request_queue.qsize(), 1)

    @patch("invoker.invoker_multi_request_priority_queue.InvokerPool")
    @patch(f"{__name__}.InvokerMultiRequest.run")
    def test_add_then_run(self, mock_invoker_pool, mock_imr_run):
        class TempQueue(InvokerMultiRequestPriorityQueue):
            pass

        queue = TempQueue()
        invoker_requests_count = [1, 2, 3, 4]
        ids = [1, 5, 12312, 0, 61351]
        for i in range(100):
            prev_invoker_pool = queue.invoker_pool
            mock_invoker_pool.get_free_invokers_count.return_value = 4
            mock_invoker_pool.get.return_value = [0, ] * invoker_requests_count[i % 4]
            invoker_multi_request = InvokerMultiRequest()
            invoker_multi_request.run = mock_imr_run
            invoker_multi_request.invoker_requests_count = invoker_requests_count[i % 4]
            invoker_multi_request.id = ids[i % 5]
            queue.invoker_pool = mock_invoker_pool
            queue.add(invoker_multi_request, 0)
            queue.run()
            self.assertEqual(queue.invoker_multi_request_queue.qsize(), 0)

    @patch("invoker.invoker_multi_request_priority_queue.InvokerPool")
    @patch(f"{__name__}.InvokerMultiRequest.run")
    def test_add_multiple_then_run(self, mock_invoker_pool, mock_imr_run):
        class TempQueue(InvokerMultiRequestPriorityQueue):
            pass

        queue = TempQueue()
        invoker_requests_count = [1, 2, 3, 4]
        ids = [1, 5, 12312, 0, 61351]
        for i in range(100):
            prev_invoker_pool = queue.invoker_pool
            mock_invoker_pool.get_free_invokers_count.return_value = 4
            mock_invoker_pool.get.return_value = [0, ] * invoker_requests_count[i % 4]
            invoker_multi_request = InvokerMultiRequest()
            invoker_multi_request.run = mock_imr_run
            invoker_multi_request.invoker_requests_count = invoker_requests_count[i % 4]
            invoker_multi_request.id = ids[i % 5]
            queue.invoker_pool = mock_invoker_pool
            queue.add(invoker_multi_request, 0)
        queue.run()
        self.assertEqual(queue.invoker_multi_request_queue.qsize(), 0)


if __name__ == '__main__':
    unittest.main()
