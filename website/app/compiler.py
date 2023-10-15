import logging
import time
import InvokerReport
import InvokerRequest
import InvokerMultiRequest
import InvokerMultiRequestPriorityQueue
import random
import subprocess
import PRIORITY
from models import model_compiler_report
logging.basicConfig(filename="log_of_compiler.txt", format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.DEBUG)


class Compiler:
    COMMANDS = {'py': None,
                'cpp': "g++ -c {} -o Compiled_files/{}"}
    WHICHFILEISCOMPILING = "{} with id {} is compiling on {}"
    FILEISCOMPILED = "{} with id {} is compiled and saved in Compiled_files/{}"
    FILEISNOTCOMPILED = "{} with id {} is not compiled with error {}"
    FILETOCOMPILEISCREATED = "{} with id {} is created"

    def __init__(self, path_to_file, who_needs_compile):
        self.who_needs = who_needs_compile
        self.file = path_to_file
        self.extension = path_to_file.split(".")[-1]
        self.id = random.randint(0, int(1e12))
        if self.COMMANDS[self.extension] is not None:
            self.command = self.COMMANDS[self.extension].format(self.file, self.id)
        logging.info(self.FILETOCOMPILEISCREATED.format(self.file, self.id))

    def compile(self):
        logging.info(self.WHICHFILEISCOMPILING.format(self.file, self.id))
        self.report = InvokerReport()
        invoker_request = InvokerRequest(self.command, self.report, True)
        invoker_requests = [invoker_request]
        invoker_multirequest = InvokerMultiRequest(invoker_requests, self, PRIORITY.RED)
        queue = InvokerMultiRequestPriorityQueue()
        queue.add(invoker_multirequest)

    def notify(self):
        compile_report = model_compiler_report.CompilerReport
        compile_report.id = "id of compiler is {}".format(self.id)
        compile_report.time = "at {} started, at {} ended".format(self.report.time_start, self.report.time_end)
        compile_report.compile_status = self.report.compile_status
        compile_report.compile_error_text = self.report.compile_error_text
        if self.report.compile_status == 1:
            self.who_needs.notify()
            logging.info(self.FILEISCOMPILED.format(self.file, self.id, self.id))
        else:
            self.who_needs.notify()
            logging.error(self.FILEISNOTCOMPILED.format(self.file, self.id, self.report.compile_status))






