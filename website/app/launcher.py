from django.conf import settings

from invoker.invoker_multi_request import Priority, InvokerMultiRequest
from invoker.invoker_request import InvokerRequest
from invoker.invoker_multi_request_priority_queue import InvokerMultiRequestPriorityQueue


class NotSupportedExtension(ValueError):
    def __init__(self, extension: str):
        self.extension = extension

    def __str__(self):
        return f"Language with extension {self.extension} is not supported!"


class Launcher:

    def __init__(self, file, callback = None):
        self.file = file
        self.extension = file.split(".")[-1]
        self.callback = callback

    def command(self):
        if self.extension not in settings.LAUNCHER_COMMANDS:
            raise NotSupportedExtension(self.extension)
        if settings.LAUNCHER_COMMANDS[self.extension] is None:
            return ' '.join([self.file])
        else:
            command_tags = settings.LAUNCHER_COMMANDS[self.extension]
            if command_tags[-1] == "%1":
                command_tags[-1] = self.file
            return ' '.join(command_tags)

    def launch(self):
        request = InvokerRequest(self.command(), files=[self.file], timelimit=settings.LAUNCHER_RUN_TL[self.extension], process_callback=self.notify)
        multi_request = InvokerMultiRequest([request], priority=Priority.RED)
        queue = InvokerMultiRequestPriorityQueue()
        queue.add(multi_request)

    def notify(self, process=None):
        if process is not None:
            self.callback(process)
