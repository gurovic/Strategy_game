# Created at 2023/10/09
from queue import PriorityQueue

from invoker.invoker_multi_request import InvokerMultiRequest
from invoker.invoker_pool import InvokerPool
from invoker.utils import Singleton


class InvokerMultiRequestPriorityQueue:
    def __init__(self):
        self.invoker_multi_request_queue = PriorityQueue()
        print("Pool Created")
        self.invoker_pool = InvokerPool()

    def run(self):
        if self.invoker_multi_request_queue.empty():
            return
        free_invokers_count = self.invoker_pool.free_invokers_count
        invoker_multi_request = self.invoker_multi_request_queue.get()
        need_invokers_count = invoker_multi_request.invoker_requests_count
        if need_invokers_count > free_invokers_count:
            self.invoker_multi_request_queue.put(invoker_multi_request)
        else:
            free_invokers = self.invoker_pool.get(need_invokers_count)
            invoker_multi_request.run(free_invokers)
            self.run()

    def add(self, invoker_multi_request: InvokerMultiRequest):
        InvokerMultiRequest.queue_notify = self.notify
        self.invoker_multi_request_queue.put(invoker_multi_request)
        self.run()

    def notify(self):
        self.run()


__all__ = ["InvokerMultiRequestPriorityQueue"]
