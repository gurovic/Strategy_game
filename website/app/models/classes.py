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


class InvokerPool:
    def __init__(self):
        self.all_invokers_count = 100  # TODO сделать определенное количество изначальных Invoker
        self.free_invokers_count = self.all_invokers_count
        self.invokers = []
        for i in range(self.all_invokers_count):
            self.invokers.append(Invoker(id=i))

    def get_free_invokers_count(self):
        return self.free_invokers_count

    def free(self, id: int):
        if self.invokers[id].status == "Working":
            self.free_invokers_count += 1
            self.invokers[id].status = "Free"

    def get(self, need_count: int, _priority: int, _user):
        result = []
        for invoker in self.invokers:
            if invoker.status == "Free":
                invoker.status = "Working"
                result.append(invoker.id)
            if len(result) == need_count:
                break
        return result
