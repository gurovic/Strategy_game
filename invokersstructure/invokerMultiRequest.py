# Created at 2023/10/09

from django.utils import timezone

from invokerRequest import InvokerRequest


class InvokerMultiRequest:
    def __init__(self, invoker_requests: [InvokerRequest], creator, priority):
        self.invoker_requests = invoker_requests
        self.invoker_requests_count = len(invoker_requests)
        self.creator = creator
        self.priority = priority
        self.pub_date = timezone.now()

    def run(self, ids: [int]):
        # InvokerMultiRequest should pass the id[i] to his i InvokerRequest
        for i in range(self.invoker_requests_count):
            self.invoker_requests[i].run(ids[i])
