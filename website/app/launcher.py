from django.conf import settings

from invoker.invoker_request import InvokerRequest


class NotSupportedExtension(ValueError):
    def __init__(self, extension: str):
        self.extension = extension

    def __str__(self):
        return f"Language with extension {self.extension} is not supported!"


class Launcher(InvokerRequest):

    def __init__(self, file: str, *args, **kwargs):
        self.file = file
        self.extension = self.file.split(".")[-1]

        super(Launcher, self).__init__(self.get_command(), timelimit=settings.LAUNCHER_RUN_TL[self.extension],  *args, **kwargs)
        self.files.append(self.file)

    def get_command(self):
        if self.extension not in settings.LAUNCHER_COMMANDS:
            raise NotSupportedExtension(self.extension)
        if settings.LAUNCHER_COMMANDS[self.extension] is None:
            return ' '.join([self.file])
        else:
            command_tags = settings.LAUNCHER_COMMANDS[self.extension]
            command_tags = [self.file if i == "%1" else i for i in command_tags]
            return ' '.join(command_tags)
