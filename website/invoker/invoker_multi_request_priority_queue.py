# Created at 2023/10/09
from queue import PriorityQueue
import logging

from invoker.invoker_multi_request import InvokerMultiRequest
from invoker.invoker_pool import InvokerPool
from invoker.utils import Singleton


class InvokerMultiRequestPriorityQueue(metaclass=Singleton):
    SELECTEDINVOKERS = "For multirequest {0} gaven invokers."
    MULTIREQUESTADDED = "Multirequest with priority: {0} added with id: {1}"
    MULTIREQUESTSELECTED = "Multirequest with id {0} and priority: {1} selected"
    MULTIREQUESTLAUNCHED = "Multirequest with id: {0} launched"

    def __init__(self):
        self.invoker_multi_request_queue = PriorityQueue()
        self.invoker_pool = InvokerPool()

    def run(self):
        if self.invoker_multi_request_queue.empty():
            return
        free_invokers_count = self.invoker_pool.free_invokers_count
        priority, invoker_multi_request = self.invoker_multi_request_queue.get()
        if invoker_multi_request.invoker_requests_count > free_invokers_count:
            self.invoker_multi_request_queue.put((priority, invoker_multi_request))
        else:
            free_invokers = self.invoker_pool.get(invoker_multi_request.invoker_requests_count)
            invoker_multi_request.run(free_invokers)
            self.run()

    def add(self, invoker_multi_request: InvokerMultiRequest, priority):
        self.invoker_multi_request_queue.put((priority, invoker_multi_request))
        logging.info(self.MULTIREQUESTADDED.format(priority, invoker_multi_request))
        self.run()

    def notify(self):
        self.run()
