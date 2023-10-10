import logging
import time
import InvokerReport
import InvokerRequest
import InvokerMultiRequest
import InvokerMultiRequestPriorityQueue
import random
import subprocess
import PRIORITY

logging.basicConfig(filename="log_of_compiler.txt", format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.DEBUG)


class Compiler:
    COMMANDS = {'py': None,
                'cpp': "g++ -c {} -o Compiled_files/{}"}
    WHICHFILEISCOMPILING = "{} with id {} is compiling on {}"
    FILEISCOMPILED = "{} with id {} is compiled and saved in Compiled_files/{}"
    FILEISNOTCOMPILED = "{} with id {} is not compiled with error {}"
    FILETOCOMPILEISCREATED = "{} with id {} is created"

    def __init__(self, path_to_file):
        self.file = path_to_file
        self.extension = path_to_file.split(".")[-1]
        self.id = random.randint(0, int(1e12))
        if self.COMMANDS[self.extension] is not None:
            self.command = self.COMMANDS[self.extension].format(self.file, self.id)
        self.is_ended = 0   # 0 - просто создан, 1 - откомпилирован, 2 - произошла ошибка
        logging.info(self.FILETOCOMPILEISCREATED.format(self.file, self.id))

    def compile(self):
        logging.info(self.WHICHFILEISCOMPILING.format(self.file, self.id))
        self.report = InvokerReport()
        invoker_request = InvokerRequest(self.command, self.report, True)
        invoker_requests = [invoker_request]
        invoker_multirequest = InvokerMultiRequest(invoker_requests, "Compiler", PRIORITY.RED)
        queue = InvokerMultiRequestPriorityQueue()
        queue.add(invoker_multirequest)

    def notify(self):
        if self.report.compile_status == 1:
            self.is_ended = 1
            logging.info(self.FILEISCOMPILED.format(self.file, self.id, self.id))
        else:
            self.is_ended = 2
            logging.error(self.FILEISNOTCOMPILED.format(self.file, self.id, self.report.compile_status))






