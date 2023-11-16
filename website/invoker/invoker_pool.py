import logging

from django.conf import settings

from invoker.invoker import Invoker, InvokerStatus
from invoker.invoker_multi_request_priority_queue import InvokerMultiRequestPriorityQueue
from invoker.utils import Singleton


class DoNotHaveNeedInvokerCount(Exception):
    def __init__(self, need_count: int, max_count: int):
        self.need_count = need_count
        self.max_count = max_count

    def __str__(self):
        return f"Need {self.need_count} but have only {self.max_count}"


class InvokerPool(metaclass=Singleton):
    GET_FREE_INVOKERS_COUNT_INVOKERS = "{'INFO:} Something got free Invokers count"
    FREE_INVOKER = "{'INFO:'} Invoker with id: {-1} was transferred from {'WORKING'} to {'FREE'}"
    GET_INVOKERS = "{'INFO:'} Invokers with ids: {[]} was got by InvokerMultiRequestQueue"

    def __init__(self):
        self.all_invokers_count = settings.MAX_INVOKERS_COUNT
        self.invoker_multi_request_priority_queue = InvokerMultiRequestPriorityQueue()
        self.all_invokers = []
        for i in range(self.all_invokers_count):
            self.all_invokers.append(Invoker())

    @property
    def free_invokers_count(self):
        logging.info("Something got free Invokers count")

        return len(list(filter(lambda x: x.status == InvokerStatus.FREE, self.all_invokers)))

    def free(self, invoker: Invoker):
        if invoker.status == InvokerStatus.WORKING:
            invoker.status = InvokerStatus.FREE
            logging.info(f"Invoker with id: {self.all_invokers.index(invoker)} was transferred from WORKING to FREE")
        else:
            logging.warning(f"Invoker with id: {self.all_invokers.index(invoker)} was transferred from FREE to FREE")

    def get(self, need_count: int):
        if self.free_invokers_count < need_count:
            raise DoNotHaveNeedInvokerCount(need_count, self.free_invokers_count)

        result = []
        for invoker in self.all_invokers:
            if invoker.status == InvokerStatus.FREE:
                invoker.status = InvokerStatus.WORKING
                result.append(invoker)
            if len(result) == need_count:
                break

        logging.warning(
            self.GET_INVOKERS.format(result)
        )

        return result
