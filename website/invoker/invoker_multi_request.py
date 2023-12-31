from __future__ import annotations

import typing
import enum

from invoker.invoker_multi_request_priority_queue import InvokerMultiRequestPriorityQueue
from invoker.invoker_request import InvokerRequest
from invoker.models import InvokerReport


class Priority(enum.IntEnum):
    GREEN = 1
    YELLOW = 2
    RED = 3


class InvokerMultiRequest:
    def __init__(self, invoker_requests: list[InvokerRequest], priority: Priority = Priority.GREEN):
        self.queue_notify_callback = None
        self.subscribers = []
        self.claimed_reports = []
        self.invoker_requests = invoker_requests
        self.invoker_requests_count = len(invoker_requests)
        self.invoker_request_ended = 0
        self.priority = priority

    def __lt__(self, other: InvokerMultiRequest):
        return self.priority > other.priority

    def start(self):
        invoker_pq = InvokerMultiRequestPriorityQueue()
        invoker_pq.add(self)

    def subscribe(self, instance) -> InvokerMultiRequest:
        self.subscribers.append(instance)
        return self

    def run(self, invokers):
        for (current_invoker, invoker_request) in zip(invokers, self.invoker_requests):
            invoker_request.callback = self.notify
            invoker_request.run(current_invoker)

    def notify(self, invoker_report: InvokerReport):
        self.invoker_request_ended += 1
        self.claimed_reports.append(invoker_report)
        if self.invoker_request_ended == self.invoker_requests_count:
            if self.queue_notify_callback:
                self.queue_notify_callback()
            for subscriber in self.subscribers:
                subscriber.notify(self.claimed_reports)


__all__ = ["InvokerMultiRequest", "Priority"]
