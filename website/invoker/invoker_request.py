from invoker.invoker import Invoker
from invoker.models import InvokerReport

import typing


class InvokerRequest:
    def __init__(self, command: str, files: typing.Optional[typing.List[str]] = None, preserve_files: typing.Optional[typing.List[str]] = None, callback: typing.Optional[typing.Callable[[InvokerReport], None]] = None):
        self.command = command
        self.files = files
        self.preserve_files = preserve_files
        self.callback = callback

        self.report = None

    def run(self, invoker: Invoker):
        invoker.run(self.command, files=self.files, preserve_files=self.preserve_files, callback=self.notify)

    def notify(self, report: InvokerReport):
        self.report = report
        if self.callback:
            self.callback(report)
