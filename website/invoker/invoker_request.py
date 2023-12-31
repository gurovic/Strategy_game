from invoker.invoker import Invoker
from invoker.models import InvokerReport

import typing


class InvokerRequest:
    def __init__(self, command: str, files: typing.Optional[list[str]] = None,
                 preserve_files: typing.Optional[list[str]] = None):
        self.command = command
        self.files = files
        self.preserve_files = preserve_files
        self.callback = None
        self.report = None

    def run(self, invoker: Invoker):
        invoker.run(self.command, files=self.files, preserve_files=self.preserve_files, callback=self.notify)

    def notify(self, report: InvokerReport):
        if self.callback:
            self.callback(report)


__all__ = ["InvokerRequest"]
