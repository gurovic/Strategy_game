import InvokerReport
import InvokerRequest
import InvokerMultiRequest
import InvokerMultiRequestPriorityQueue
import random
import subprocess
import PRIORITY


class Compiler:
    COMMANDS = {'py': None,
                'cpp': "g++ -c {} -o Compiled_files/{}"}

    def __init__(self, path_to_file):
        self.file = path_to_file
        self.extension = path_to_file.split(".")[-1]
        self.id = random.randint(0, int(1e12))
        if self.COMMANDS[self.extension] is not None:
            self.command = self.COMMANDS[self.extension].format(self.file, self.id)

    def compile(self):
        self.report = InvokerReport()
        invoker_request = InvokerRequest(self.command, self.report, True)
        invoker_requests = [invoker_request]
        invoker_multirequest = InvokerMultiRequest(invoker_requests, "Compiler", PRIORITY.RED)
        queue = InvokerMultiRequestPriorityQueue()
        queue.add(invoker_multirequest)




a = Compiler("ciplusplus\\main.cpp")
print("f")

#надо будет добавить проверку результата и кому его возвращать(OBSERVER)