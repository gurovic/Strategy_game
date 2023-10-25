import InvokerRequest
import InvokerMultiRequest
import InvokerMultiRequestPriorityQueue
from models import model_compiler_report


class Compiler:
    import logging
    logging.basicConfig(filename="log_of_compiler.txt",
                        format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.DEBUG)

    COMMANDS = {'py': None,
                'cpp': "g++ -c {} -o {}"}
    WHICHFILEISCOMPILING = "{} with id {} is compiling on {}{}"
    FILEISCOMPILED = "{} with id {} is compiled and saved in {}{}"
    FILEISNOTCOMPILED = "{} with id {} is not compiled with error {}"
    FILETOCOMPILEISCREATED = "{} with id {} is created"
    WHOCREATED = "{} with id {} is created by {}"

    def __init__(self, path_to_file, class_who_is_using, where_to_save):
        from random import randint
        self.clas = class_who_is_using
        self.path = path_to_file
        self.extension = path_to_file.split(".")[-1]
        self.id = randint(0, int(1e12))
        self.where = where_to_save
        if self.COMMANDS[self.extension] is not None:
            self.command = self.COMMANDS[self.extension].format(self.path, self.where, self.id)
        self.logging.info(self.FILETOCOMPILEISCREATED.format(self.path, self.id))
        self.logging.info(self.WHOCREATED.format(self.path, self.id, self.clas))

    def compile(self):
        import PRIORITY
        self.logging.info(self.WHICHFILEISCOMPILING.format(self.path, self.id))
        invoker_request = InvokerRequest(self.command, True)
        invoker_requests = [invoker_request]
        invoker_multirequest = InvokerMultiRequest(invoker_requests, self)
        queue = InvokerMultiRequestPriorityQueue()
        queue.add(invoker_multirequest, PRIORITY.RED)

    def notify(self, report):
        compile_report = model_compiler_report.CompilerReport()
        compile_report.id = self.id
        compile_report.path = self.path
        compile_report.time = "at {} started, at {} ended".format(report.time_start, report.time_end)
        compile_report.compile_status = report.program_status
        compile_report.compile_error_text = report.program_error_text
        if report.compile_status == "OK":
            self.clas.notify()
            self.logging.info(self.FILEISCOMPILED.format(self.path, self.id, self.where, self.id))
        else:
            self.clas.notify()
            self.logging.error(self.FILEISNOTCOMPILED.format(self.path, self.id, report.compile_status))






