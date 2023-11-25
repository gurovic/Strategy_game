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
        self.free_invokers = set()
        for i in range(self.all_invokers_count):
            new_invoker = Invoker()
            new_invoker.callback_free_myself = self.free
            self.all_invokers.append(new_invoker)
            self.free_invokers.add(new_invoker)

    @property
    def free_invokers_count(self):
        logging.info("Something asked for free Invokers count")
        return len(self.free_invokers)

    def free(self, invoker: Invoker):
        if invoker.status == InvokerStatus.WORKING:
            invoker.status = InvokerStatus.FREE
            self.free_invokers.add(invoker)
            logging.info(f"Invoker with id: {self.all_invokers.index(invoker)} was transferred from WORKING to FREE")
        else:
            logging.info("We've lost our Invoker")

    def get(self, need_count: int):
        if self.free_invokers_count < need_count:
            raise LowInvokerCap(need_count, self.free_invokers_count)

        result = []
        for invoker in self.free_invokers:
            invoker.status = InvokerStatus.WORKING
            result.append(invoker)
            if len(result) == need_count:
                break
        for i in result:
            self.free_invokers.remove(i)
        return result


__all__ = ["InvokerPool", "LowInvokerCap"]
