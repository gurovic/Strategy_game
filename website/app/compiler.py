import io

from django.core.files import File as FileDjango

from app.models import CompilerReport

from invoker.models import InvokerReport
from invoker.invoker_multi_request import Priority, InvokerMultiRequest
from invoker.invoker_request import InvokerRequest
from invoker.invoker_multi_request_priority_queue import InvokerMultiRequestPriorityQueue
from invoker.filesystem import File

import typing


class NotSupportedLanguage(ValueError):
    def __init__(self, lang: str):
        self.lang = lang

    def __str__(self):
        return f"Language {self.lang} is not supported!"


CompilerReportSubscriber: typing.Type = typing.Callable[[CompilerReport], None]


class AbstractCompile:
    def __init__(self, source: str, lang: str, callback: typing.Optional[CompilerReportSubscriber] = None):
        self.source = source
        self.lang = lang

        self.callback = callback

    def command(self) -> (str, str | File, str):
        """Return compile command, input file and output file name"""
    
    def compile(self):
        command, input_file, output_file = self.command()
        request = InvokerMultiRequest([InvokerRequest(command, files=[input_file], preserve_files=[output_file])], priority=Priority.RED).subscribe(self)
        queue = InvokerMultiRequestPriorityQueue()
        queue.add(request)

    def notify(self, report: InvokerReport):
        compiler_report = self.make_report(report)
        self.send_report(compiler_report)

    def make_report(self, report: InvokerReport):
        return CompilerReport.objects.create(invoker_report=report, time=report.time_end - report.time_start,
                                             status=CompilerReport.Status.OK if report.status == InvokerReport.Status.OK else CompilerReport.Status.COMPILATION_ERROR,
                                             error=report.error, compiled_file=report.files.get(name=self.command()[2]).file)

    def send_report(self, report: CompilerReport):
        if self.callback:
            self.callback(report)


class CPPCompile(AbstractCompile):
    INPUT_FILE_NAME = "main.cpp"
    OUTPUT_FILE_NAME = "compiled"

    def command(self) -> (str, str | File, str):
        file = File(self.INPUT_FILE_NAME, self.source)
        return f"g++ -o {self.OUTPUT_FILE_NAME} {file.name}", file, self.OUTPUT_FILE_NAME


class DoNothingCompile(AbstractCompile):
    FILE_NAME = "compiled.{}"

    def compile(self):
        report = CompilerReport.objects.create(status=CompilerReport.Status.OK,
                                               compiled_file=FileDjango(io.StringIO(self.source),
                                                                        name=self.FILE_NAME.format(self.lang))
                                               )
        self.send_report(report)


class Compiler:
    COMMANDS = {
        "cpp": CPPCompile,
        "py": DoNothingCompile,
    }

    def __init__(self, source: str, lang: str, callback: typing.Optional[CompilerReportSubscriber] = None):
        self.source = source
        self.lang = lang
        self.callback = callback

        if self.lang not in self.COMMANDS:
            raise NotSupportedLanguage(self.lang)

        self.command: AbstractCompile = self.COMMANDS[self.lang](self.source, self.lang, callback=self.notify)

    def compile(self):
        self.command.compile()

    def notify(self, report: CompilerReport):
        if self.callback:
            self.callback(report)
