# Author: derwes
# at 2023/10/15
import subprocess
import random

from enum import Enum

from invokerReport import InvokerReport


class InvokerStatus(Enum):
    WORKING = 1
    FREE = 0


class Invoker:
    subscribers = []

    def __init__(self):
        self.status = InvokerStatus.FREE
        self.id = random.randint(0, 1000000000000)

    def run(self, command):
        exitreport = subprocess.Popen(command)  # что в него передавать ещё предстоит узнать
        report = InvokerReport(exitreport)
        for subscriber in self.subscribers:
            subscriber.notify(self.id, report)
