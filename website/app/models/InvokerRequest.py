import os
import Invoker
impoer InvokerLog
import InvokerPool
import InvokerReport
from datetime import datetime


class InvokerRequest:
    def __init__(self, start_file):
        self.start_file = start_file
        self.time_start = None
        self.time_end = None
        # зачем нужны время начала в время конца в self, когда они уже хранятся в self.running_result?
        self.is_compile = True
        # зачему нужен этот флаг, когда компиляция и запуск проходят друг за другом в функции run?
        self.running_result = None

    def run(self, id):
        self.time_start = datetime.now()
        return_report = InvokerReport()

        compile_report = Invoker.compile_file(self.start_file, id)
        self.is_compile = False
        return_report.compile_status = compile_report.compile_status
        return_report.compile_error_text = compile_report.compile_error_text

        if return_report.compile_status == 'OK':
            # куда Invoker складывает скомпилированный фвйл?? Пусть в InvokerReport.file
            run_report = Invoker.run_file(compile_report.file, id)
            return_report.run_status = run_report.run_status
            return_report.run_error_text = compile_report.run_error_text

        self.time_end = datetime.now()
        InvokerPool.free(id)

        return_report.time_start = self.time_start
        return_report.time_end = self.time_end
        self.running_result = return_report
        InvokerLog.add_invoker(return_report)
        return return_report
