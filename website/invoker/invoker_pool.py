import logging

from django.conf import settings

from invoker.invoker import Invoker, InvokerStatus
from invoker.utils import Singleton



class LowInvokerCap(Exception):
    def __init__(self, need_count: int, usable_count: int):
        self.need_count = need_count
        self.usable_count = usable_count

    def __str__(self):
        return f"Need {self.need_count} but have only {self.usable_count}"


class InvokerPool(metaclass=Singleton):
    def __init__(self):
        self.all_invokers_count = settings.MAX_INVOKERS_COUNT
        self.all_invokers = []
        for i in range(self.all_invokers_count):
            self.all_invokers.append(Invoker())

    @property
    def free_invokers_count(self):
        logging.info("Something asked for free Invokers count")
        return len(list(filter(lambda x: x.status == InvokerStatus.FREE, self.all_invokers)))

    def free(self, invoker: Invoker):
        if invoker.status == InvokerStatus.WORKING:
            invoker.status = InvokerStatus.FREE
            logging.info(f"Invoker with id: {self.all_invokers.index(invoker)} was transferred from WORKING to FREE")

    def get(self, need_count: int):
        if self.free_invokers_count < need_count:
            raise LowInvokerCap(need_count, self.free_invokers_count)

        result = []
        for invoker in self.all_invokers:
            if invoker.status == InvokerStatus.FREE:
                invoker.status = InvokerStatus.WORKING
                result.append(invoker)
            if len(result) == need_count:
                break
        return result


__all__ = ["InvokerPool", "LowInvokerCap"]
