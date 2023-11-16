import logging
import SETTINGS

from invoker import Invoker
from singleton import Singleton
from invoker import InvokerStatus
from invokerMultiRequestPriorityQueue import InvokerMultiRequestPriorityQueue


class InvokerPool:
    ALL_INVOKERS_COUNT = SETTINGS.ALL_INVOKERS_COUNT
    GET_FREE_INVOKERS_COUNT_INVOKERS_LOG_TEXT = "{'INFO:} Something got free Invokers count"
    FREE_INVOKER_LOG_TEXT = "{'INFO:'} Invoker with id: {-1} was transferred from {'WORKING'} to {'FREE'}"
    GET_INVOKERS_LOG_TEXT = "{'INFO:'} Invokers with ids: {[]} was got by InvokerMultiRequestQueue"

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(InvokerPool, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        logging.basicConfig(level=logging.INFO, filename="../../logs/InvokerPool.log", filemode='w',
                            format='%(asctime)s %(message)s', datefmt='%I:%M:%S')
        self.invoker_multi_request_priority_queue = InvokerMultiRequestPriorityQueue()
        self.free_invokers_count = self.ALL_INVOKERS_COUNT
        self.all_invokers = []
        for i in range(self.ALL_INVOKERS_COUNT):
            self.all_invokers.append(Invoker(id=i))

    def get_free_invokers_count(self):
        logging.info(
            self.GET_FREE_INVOKERS_COUNT_INVOKERS_LOG_TEXT
        )
        return self.free_invokers_count

    def free(self, id: int):
        if self.all_invokers[id].status == InvokerStatus.WORKING:
            self.free_invokers_count += 1
            self.all_invokers[id].status = InvokerStatus.FREE
            logging.info(
                self.FREE_INVOKER_LOG_TEXT.format(id)
            )
        else:
            logging.warning(
                self.FREE_INVOKER_LOG_TEXT.format("WARNING:", id, "FREE", "FREE")
            )

    def get(self, need_count: int):
        if self.get_free_invokers_count() < need_count:
            logging.warning(
                self.GET_INVOKERS_LOG_TEXT.format('WARNING:', )
            )
            return None
        result = []
        for invoker in self.all_invokers:
            if invoker.status == InvokerStatus.FREE:
                invoker.status = InvokerStatus.WORKING
                result.append(invoker.id)
            if len(result) == need_count:
                break
        logging.warning(
            self.GET_INVOKERS_LOG_TEXT.format(result)
        )
        return result
