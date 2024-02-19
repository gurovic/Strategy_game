import typing
import enum

from invoker.invoker import Invoker
from invoker.models import InvokerReport


class InvokerRequestType(enum.Enum):
    PLAY = enum.auto()
    STRATEGY = enum.auto()
    OTHER = enum.auto()


class InvokerRequest:
    def __init__(self, command: str, files: typing.Optional[list[str]] = None,
                 preserve_files: typing.Optional[list[str]] = None,
                 report_callback=None, process_callback=None):
        self.command = command
        self.files = files
        self.preserve_files = preserve_files
        self.report_callback = report_callback
        self.process_callback = process_callback
        self.label = None

    def run(self, invoker: Invoker):
        invoker_process = invoker.run(self.command, files=self.files, preserve_files=self.preserve_files, label=self.label, callback=self.notify)

        if self.process_callback is not None:
            self.process_callback(invoker_process)

    def notify(self, report: InvokerReport):
        if self.report_callback is not None:
            self.report_callback(report)


__all__ = ["InvokerRequest"]
