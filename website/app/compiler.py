import io
import typing

from django.core.files import File as FileDjango
from django.conf import settings

from app.models import CompilerReport
from invoker.models import InvokerReport
from invoker.invoker_multi_request import Priority, InvokerMultiRequest
from invoker.invoker_request import InvokerRequest
from invoker.invoker_multi_request_priority_queue import InvokerMultiRequestPriorityQueue
from invoker.filesystem import File


class NotSupportedLanguage(ValueError):
    def __init__(self, lang: str):
        self.lang = lang

    def __str__(self):
        return f"Language {self.lang} is not supported!"


CompilerReportSubscriber: typing.Type = typing.Callable[[CompilerReport], None]


class NormalCompile:
    INPUT_FILE_NAME = "main.{}"
    OUTPUT_FILE_NAME = "compiled.e{}"

    def __init__(self, source: str, lang: str, command: str = None,
                 callback: typing.Optional[CompilerReportSubscriber] = None):
        self.source = source
        self.lang = lang
        self.command = command
        self.callback = callback
        try:
            with open(self.source, "r") as f:
                self.input_file = f.read()
        except FileNotFoundError:
            self.input_file = None
        self.output_file = None

    def compile(self):
        command = self.command
        self.output_file = self.OUTPUT_FILE_NAME.format(self.lang)
        timelimit = None
        if self.lang in settings.COMPILE_TL:
            timelimit = settings.COMPILE_TL[self.lang]
        invoker_request = InvokerRequest(' '.join(command), files=[self.source], preserve_files=[self.output_file],
                                     timelimit=timelimit)
        multi_request = InvokerMultiRequest([invoker_request], priority=Priority.RED).subscribe(self)

        queue = InvokerMultiRequestPriorityQueue()
        queue.add(multi_request)

    def make_report(self, report: InvokerReport):

        end_status = None
        if report.status == InvokerReport.Status.TL:
            end_status = CompilerReport.Status.TIMELIMIT
        elif report.status == InvokerReport.Status.OK:
            end_status = CompilerReport.Status.OK
        else:
            end_status = CompilerReport.Status.COMPILATION_ERROR

        compiled_file = None
        if end_status == CompilerReport.Status.OK:
            compiled_file = report.preserved_files.get(name=self.output_file).file

        return CompilerReport.objects.create(
            invoker_report=report,
            time=report.time_end - report.time_start,
            status=end_status,
            error=report.error,
            compiled_file=compiled_file)

    def notify(self, report: list[InvokerReport]):
        compiler_report = self.make_report(report[0])
        self.send_report(compiler_report)

    def send_report(self, report: CompilerReport):
        if self.callback:
            self.callback(report)


class FakeCompile:
    INPUT_FILE_NAME = "main.{}"
    OUTPUT_FILE_NAME = "compiled.e{}"

    def __init__(self, source: str, lang: str, command: str = None,
                 callback: typing.Optional[CompilerReportSubscriber] = None):
        self.source = source
        self.lang = lang
        self.command = command
        self.callback = callback
        try:
            with open(self.source, "r") as f:
                self.input_file = f.read()
        except FileNotFoundError:
            self.input_file = None
        self.output_file = None

    def compile(self):
        compiled_file = FileDjango(io.StringIO(self.input_file), name=self.OUTPUT_FILE_NAME.format(self.lang))

        report = CompilerReport.objects.create(status=CompilerReport.Status.OK,
                                               compiled_file=compiled_file)
        self.send_report(report)

    def send_report(self, report: CompilerReport):
        if self.callback:
            self.callback(report)


class Compiler:
    def __init__(self, source: str, lang: str, callback: typing.Optional[CompilerReportSubscriber] = None):
        self.source = source
        self.lang = lang
        self.callback = callback
        self.report = None

        if self.lang not in settings.COMPILER_COMMANDS:
            raise NotSupportedLanguage(self.lang)

        command = settings.COMPILER_COMMANDS[self.lang]

        if command is None:
            self.compiler = FakeCompile(source=self.source, lang=self.lang, callback=self.notify)
        else:
            command[-1] = self.source
            self.compiler = NormalCompile(source=self.source, lang=self.lang, command=command, callback=self.notify)

    def compile(self):
        self.compiler.compile()

    def notify(self, report: CompilerReport):
        self.report = report
        if self.callback:
            self.callback(report)
