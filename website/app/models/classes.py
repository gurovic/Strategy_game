from django.utils import timezone
from .models import *


class InvokerRequest:
    def run(self):
        pass


class InvokerMultiRequest:
    def __init__(self, _invoker_requests: [InvokerRequest], _creator, _priority):
        self.invoker_requests = _invoker_requests
        self.invoker_requests_count = len(_invoker_requests)
        self.creator = _creator
        self.priority = _priority
        self.pub_date = timezone.now()

    def run(self, ids: [int]):
        # InvokerMultiRequest should pass the id[i] to his i InvokerRequest
        for i in range(self.invoker_requests_count):
            self.invoker_requests[i].run(ids[i])
