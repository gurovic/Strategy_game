import typing

from django.conf import settings

from invoker.invoker_multi_request import Priority, InvokerMultiRequest
from invoker.invoker_request import InvokerRequest
from invoker.invoker_multi_request_priority_queue import InvokerMultiRequestPriorityQueue


class NotSupportedExtension(ValueError):
    def __init__(self, extension: str):
        self.extension = extension

    def __str__(self):
        return f"Language with extension {self.extension} is not supported!"


class Launcher(InvokerRequest):

    def __init__(self, file: str, *args, **kwargs):
        self.file = file
        self.extension = self.file.split(".")[-1]

        super(Launcher, self).__init__(self.command, *args, **kwargs)
        self.files.append(self.file)

    @property
    def command(self):
        for i in range(len(self.file)):
            if self.extension[i] not in settings.LAUNCHER_COMMANDS:
                raise NotSupportedExtension(self.extension[i])
            if settings.LAUNCHER_COMMANDS[self.extension[i]] is None:
                return ' '.join([self.file[i]])
            else:
                command_tags = settings.LAUNCHER_COMMANDS[self.extension[i]]
                command_tags = [self.file[i] if i == "%1" else i for i in command_tags]
                return ' '.join(command_tags)
