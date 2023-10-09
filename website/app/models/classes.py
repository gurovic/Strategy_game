from django.utils import timezone
from .models import *
from enum import Enum
import SETTINGS


class InvokerStatus(Enum):
    WORKING = 1
    FREE = 0


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
    ALL_INVOKERS_COUNT = SETTINGS.ALL_INVOKERS_COUNT
    def __init__(self):
        self.free_invokers_count = self.ALL_INVOKERS_COUNT
        self.all_invokers = []
        for i in range(self.ALL_INVOKERS_COUNT):
            self.all_invokers.append(Invoker(id=i))

    def get_free_invokers_count(self):
        return self.free_invokers_count

    # TODO сделать чтобы после освобождения некоторых Invoker IP говорил IMRPQ что есть свободные Invokers
    def free(self, id: int):
        if self.all_invokers[id].status == InvokerStatus.WORKING:
            self.free_invokers_count += 1
            self.all_invokers[id].status = InvokerStatus.FREE


    def get(self, need_count: int):
        if self.get_free_invokers_count() < need_count:
            return None
        result = []
        for invoker in self.all_invokers:
            if invoker.status == InvokerStatus.FREE:
                invoker.status = InvokerStatus.WORKING
                result.append(invoker.id)
            if len(result) == need_count:
                break
        return result

# TODO сделать SUBSCRIBE
# TODO логи?
