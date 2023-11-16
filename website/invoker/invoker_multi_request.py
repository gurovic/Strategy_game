import random

from invoker.invoker_multi_request_priority_queue import InvokerMultiRequestPriorityQueue
from invoker.invoker_request import InvokerRequest
from invoker.models import InvokerReport


class InvokerMultiRequest:
    def __init__(self, invoker_requests: [InvokerRequest], priority):
        self.subscribers = []
        self.claimed_reports = []
        self.invoker_requests = invoker_requests
        self.invoker_requests_count = len(invoker_requests)
        self.invoker_request_ended = 0
        self.priority = priority

    def start(self):
        invoker_pq = InvokerMultiRequestPriorityQueue()
        invoker_pq.add(self, self.priority)

    def run(self, invokers):
        for (invoker, invoker_request) in zip(invokers, self.invoker_requests):
            invoker_request.run(invoker)

    def notify(self, invoker_report: InvokerReport):
        self.invoker_requests_count += 1
        self.claimed_reports.append(invoker_report)
        if self.invoker_request_ended >= self.invoker_requests_count:
            for subscriber in self.subscribers:
                subscriber.notify(self.claimed_reports)
