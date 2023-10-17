# Created at 2023/10/09
from queue import PriorityQueue
import logging

from invokerMultiRequests import InvokerMultiRequest
from invokerPool import InvokerPool
from singleton import Singleton

logging.basicConfig(filename='LOG.log', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%I:%M:%S')


class InvokerMultiRequestsPriorityQueue(metaclass=Singleton):
    invokerMultiRequestQueue = PriorityQueue()
    SELECTEDINVOKERS = "For multirequest {0} selected invokers with id's {1}"
    MULTIREQUESTADDED = "Multirequest with priority: {0} added with id: {1}"
    MULTIREQUESTSELECTED = "Multirequest with id {0} and priority: {1} selected"
    MULTIREQUESTLAUNCHED = "Multirequest with id: {0} launched"

    def __init__(self):
        self.invokerPool = InvokerPool()
        pass

    def run(self):
        # Можно разбить на несколько очередей (Визуал, Компиляция, ...) Для отсутствия застоя по всем группам
        freeinvokerscount = self.invokerPool.get_free_invokers_count()
        priority, invokermultirequest = self.invokerMultiRequestQueue.get()
        logging.info(
            self.MULTIREQUESTSELECTED.format(invokermultirequest.id, priority)
        )
        while freeinvokerscount < invokermultirequest.invoker_requests_count:
            freeinvokerscount = self.invokerPool.get_free_invokers_count()
        freeinvokersid = self.invokerPool.get(invokermultirequest.invoker_requests_count)
        logging.info(
            self.SELECTEDINVOKERS.format(invokermultirequest.id, freeinvokersid)
        )
        invokermultirequest.run(freeinvokersid)
        logging.info(self.MULTIREQUESTLAUNCHED.format(invokermultirequest.id))

    def add(self, invokermultirequest: [InvokerMultiRequest], priority):
        self.invokerMultiRequestQueue.put((priority, invokermultirequest))
        logging.info(
            self.MULTIREQUESTADDED.format(priority, invokermultirequest.id)
        )
