# Author: derwes
# at 2023/10/15
import random
import os

from invokerReport import InvokerReport


class Invoker:
    subscribers = []

    def __init__(self):
        self.id = random.randint(0, 1000000000000)

    def run(self, command):
        exitreport = os.popen(command)
        report = InvokerReport(exitreport)
        for subscriber in self.subscribers:
            subscriber.notify(id, report)
