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

    def __init__(self, files,  callback = None):
        self.files = files
        self.extensions = [i.split(".")[-1] for i in files]
        self.callback = callback

    def command(self):
        for i in range(len(self.files)):
            if self.extensions[i] not in settings.LAUNCHER_COMMANDS:
                raise NotSupportedExtension(self.extensions[i])
            if settings.LAUNCHER_COMMANDS[self.extensions[i]] is None:
                return ' '.join([self.files[i]])
            else:
                command_tags = settings.LAUNCHER_COMMANDS[self.extensions[i]]
                command_tags = [self.files[i] if i == "%1" else i for i in command_tags]
                return ' '.join(command_tags)

    def launch(self):
        requests = []
        for i in range(len(self.files)):
            request = InvokerRequest(self.command(), files=[self.files[i]], timelimit=settings.LAUNCHER_RUN_TL[self.extensions[i]], process_callback=self.notify)
            requests.append(request)
        multi_request = InvokerMultiRequest(requests, priority=Priority.RED)
        queue = InvokerMultiRequestPriorityQueue()
        queue.add(multi_request)

    def notify(self, process=None):
        if process is not None:
            self.callback(process)
