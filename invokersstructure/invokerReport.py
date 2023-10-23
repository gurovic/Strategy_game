# Created at 2023/10/15

class InvokerReport:

    def __init__(self, report):
        self.exitcode = report
        self.exitreport = report.read()
