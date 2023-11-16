# Created at 2023/10/09
import random

from django.utils import timezone

from invokerRequest import InvokerRequest
from invokerMultiRequestPriorityQueue import InvokerMultiRequestPriorityQueue


class InvokerMultiRequest:
    def __init__(self, invoker_requests: [InvokerRequest], creator, priority):
        self.invoker_requests = invoker_requests
        self.invoker_priority_queue = InvokerMultiRequestPriorityQueue()
        self.invoker_requests_count = len(invoker_requests)
        self.creator = creator
        self.priority = priority
        self.invoker_reports = []
        self.pub_date = timezone.now()
        self.invoker_priority_queue.add(self, self.priority)
        self.id = random.randint(1, 1000000000000)

    def run(self, ids: [int]):
        # InvokerMultiRequest should pass the id[i] to his i InvokerRequest
        for i in range(self.invoker_requests_count):
            self.invoker_requests[i].run(ids[i], self)

    def notify(self, invoker_report):
        self.invoker_reports.append(invoker_report)
        if len(self.invoker_reports) == len(self.invoker_requests):
            self.creator.notify(self.invoker_reports)
