# Author: derwes
# at 2023/10/09

import InvokerMultiRequests


class InvokerMultiRequestsPriorityQueue:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(InvokerMultiRequestsPriorityQueue, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        pass

    def add(self, invokermultirequests: [InvokerMultiRequests]):
        pass


a = InvokerMultiRequestsPriorityQueue()
b = InvokerMultiRequestsPriorityQueue()
print('Object 1: ', a)
print('Object 2: ', b)
print(a == b)
