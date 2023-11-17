from app.models import CompilerReport

from invoker.models import InvokerReport
from invoker.invoker_multi_request import Priority, InvokerMultiRequest
from invoker.invoker_request import InvokerRequest
from invoker.invoker_multi_request_priority_queue import InvokerMultiRequestPriorityQueue
from invoker.filesystem import File

from abc import ABC, abstractmethod
import typing


class NotSupportedLanguage(ValueError):
    def __init__(self, lang: str):
        self.lang = lang

    def __str__(self):
        return f"Language {self.lang} is not supported!"


CompilerReportSubscriber: typing.Type = typing.Callable[[CompilerReport], None]


class AbstractCompile(ABC):
    def __int__(self, source: str, lang: str, callback: typing.Optional[CompilerReportSubscriber] = None):
        self.source = source
        self.lang = lang

        self.callback = callback

    @abstractmethod
    def command(self) -> (str, str | File, str):
        ...
    
    def compile(self):
        command, input_file, output_file = self.command()
        request = InvokerMultiRequest([InvokerRequest(command, files=[input_file], preserve_files=[output_file], callback=self.notify)], priority=Priority.RED)
        queue = InvokerMultiRequestPriorityQueue()
        queue.add(request)

    def notify(self, report: InvokerReport):
        compiler_report = self.make_report(report)
        self.send_report(compiler_report)

    def make_report(self, report: InvokerReport):
        compiler_report = CompilerReport(invoker_report=report)
        compiler_report.time = report.time_end = report.time_start
        compiler_report.status = CompilerReport.Status.OK if report.status == InvokerReport.Status.OK else CompilerReport.Status.COMPILATION_ERROR
        compiler_report.error = report.error
        compiler_report.compiled_file = report.files.filter(name=self.command()[1])
        compiler_report.save()

        return compiler_report

    def send_report(self, report: CompilerReport):
        self.callback(report)


class CPPCompile(AbstractCompile):
    def command(self):
        file = File("main.cpp", self.source)
        return f"g++ -o compiled {file.name}", file


class DoNothingCompile(AbstractCompile):
    def command(self):
        pass


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
        self.callback(report)
