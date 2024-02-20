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


class AbstractCompile:
    def __init__(self, source: str, lang: str, callback: typing.Optional[CompilerReportSubscriber] = None):
        self.source = source
        self.lang = lang
        self.callback = callback

    def command(self) -> (str, str | File, str):
        """Return compile command, input file and output file name"""

    def compile(self):
        command, input_file, output_file = self.command()
        timelimit = None
        if self.lang in settings.COMPILE_TL:
            timelimit = settings.COMPILE_TL[self.lang]
        request = InvokerMultiRequest([InvokerRequest(command, files=[input_file], preserve_files=[output_file], timelimit=timelimit)],
                                      priority=Priority.RED).subscribe(self)
        queue = InvokerMultiRequestPriorityQueue()
        queue.add(request)

    def notify(self, report: list[InvokerReport]):
        compiler_report = self.make_report(report[0])
        self.send_report(compiler_report)

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
            compiled_file = report.preserved_files.get(name=self.command()[2]).file

        return CompilerReport.objects.create(
            invoker_report=report,
            time=report.time_end - report.time_start,
            status=end_status,
            error=report.error,
            compiled_file=compiled_file)

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
        self.report = None

        if self.lang not in self.COMMANDS:
            raise NotSupportedLanguage(self.lang)

        compiler_type = self.COMMANDS[self.lang]
        self.command: AbstractCompile = compiler_type(self.source, self.lang, callback=self.notify)

    def compile(self):
        self.command.compile()

    def notify(self, report: CompilerReport):
        self.report = report
        if self.callback:
            self.callback(report)
