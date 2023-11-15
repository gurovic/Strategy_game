from invoker.invoker import Invoker
from invoker_log import InvokerLog
from invoker.invoker_pool import InvokerPool
from invoker.models import InvokerReport
from datetime import datetime
import os


class InvokerRequest:
    def __init__(self, run_command, subscribers):
        self.run_command = run_command
        self.time_created = datetime.now()
        self.subscribers = subscribers
        self.return_report = None

    def run(self, current_invoker, preserve_files):
        self.time_created = datetime.now()
        self.current_invoker = current_invoker
        return_report = InvokerReport()

        compile_report = self.current_invoker.compile_file(self.run_command, id)
        return_report.compile_status = compile_report.compile_status
        return_report.compile_error_text = compile_report.compile_error_text

        if return_report.compile_status == 'OK':
            run_report = self.current_invoker.run_file(compile_report.file, id)
            return_report.run_status = run_report.run_status
            return_report.run_error_text = compile_report.run_error_text

        InvokerPool.free(id)

        return_report.time_start = self.time_created
        return_report.time_end = datetime.now()
        InvokerLog.add_invoker(return_report)
        self.return_report = return_report
        return return_report

    def notify(self):
        InvokerMultiRequest.notify(self.return_report)
