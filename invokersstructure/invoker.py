# Author: derwes
# at 2023/10/15
import subprocess
import random

from invokerReport import InvokerReport


class Invoker:
    subscribers = []

    def __init__(self):
        self.id = random.randint(0, 1000000000000)

    def run(self, command):
        exitreport = subprocess.Popen(command)  # что в него передавать ещё предстоит узнать
        report = InvokerReport(exitreport)
        for subscriber in self.subscribers:
            subscriber.notify(id, report)
