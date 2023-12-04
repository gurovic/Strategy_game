from invoker.filesystem import File, delete_directory
from invoker.models import InvokerReport, File as FileModel

from django.conf import settings
from django.utils import timezone
from django.core.files import File as FileDjango

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from threading import Thread
import subprocess
import tempfile
import logging
import typing
import shlex
import enum
import io


class StdIn(typing.Protocol):
    def write(self, data: str):
        ...


class StdOut(typing.Protocol):
    def read(self) -> str:
        ...

    def readline(self) -> str:
        ...


class InvokerStatus(enum.Enum):
    FREE = enum.auto()
    WORKING = enum.auto()


@dataclass
class RunResult:
    command: str
    output: str
    exit_code: int | None

    time_start: datetime
    time_end: datetime

    timelimit: typing.Optional[int] = None
    exceeded_timelimit: bool = False

    label: typing.Optional[str] = None

    input_files: typing.Optional[list[File]] = None
    preserved_files: typing.Optional[list[File]] = None


class InvokerProcess(ABC):
    stdin: StdIn
    stdout: StdOut

    def __init__(self, *args, label: typing.Optional[str] = None,
                 preserve_files: typing.Optional[list[str]] = None,
                 timelimit: typing.Optional[int] = None,
                 callback: typing.Optional[typing.Callable[[RunResult], None]] = None,
                 **kwargs):
        self.label = label
        self.preserve_files = preserve_files
        self.timelimit = timelimit
        self.callback = callback
        self._run_result = None
        super().__init__(*args, **kwargs)

        if self.callback:
            self.register_callback()

    def register_callback(self):
        Thread(target=self._wait_for_end).start()

    @abstractmethod
    def wait(self, timeout: typing.Optional[int] = None):
        ...

    @abstractmethod
    def kill(self):
        ...

    def connect(self, input: str) -> str:
        self.stdin.write(input)
        return self.stdout.readline()

    def _wait_for_end(self):
        try:
            self.wait(self.timelimit)
        except subprocess.TimeoutExpired as exc:
            self.kill()
        self.send_callback()

    def send_callback(self):
        self.callback(self.run_result)

    @abstractmethod
    def make_run_result(self) -> RunResult:
        ...

    @property
    def run_result(self) -> RunResult:
        if not self._run_result:
            self._run_result = self.make_run_result()
        return self._run_result


class NormalProcess(subprocess.Popen, InvokerProcess):
    def __init__(self, *args, work_dir: typing.Optional[str] = None, **kwargs):
        self.work_dir = work_dir
        super().__init__(*args, cwd=work_dir, text=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True,
                         **kwargs)

    def make_run_result(self) -> RunResult:
        preserve_dir = [File.load(Path(self.work_dir) / file) for file in self.preserve_files] if self.preserve_files else None
        return RunResult(
            command,
            result.stdout,
            return_code,
            time_start,
            time_end,
            timelimit,
            timelimit_error,
            label,
            file_system,
            preserve_dir
        )


class InvokerEnvironment(ABC):
    process: typing.Type[InvokerProcess]

    def __init__(self, callback: typing.Callable[[RunResult], None]):
        self.callback = callback

    @abstractmethod
    def launch(self, command: str, file_system: typing.Optional[list[File]] = None,
               preserve_files: typing.Optional[list[str]] = None, timelimit: typing.Optional[int] = None,
               label: typing.Optional[str] = None) -> RunResult:
        ...


class NormalEnvironment(InvokerEnvironment):
    process = NormalProcess
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.work_dir = self.initialize_workdir()

    @staticmethod
    def initialize_workdir() -> str:
        return tempfile.mkdtemp()

    def place_file_system(self, file_system: typing.Optional[list[File]] = None):
        if file_system:
            for file in file_system:
                file.make(self.work_dir)

    def launch(self, command: list[str] | str, file_system: typing.Optional[list[File]] = None,
               preserve_files: typing.Optional[list[str]] = None, timelimit: typing.Optional[int] = None,
               label: typing.Optional[str] = None) -> NormalProcess:
        self.place_file_system(file_system)

        return self.process(shlex.shlex(command) if isinstance(command, str) else command)

    def notify(self, run_result: RunResult):
        delete_directory(self.work_dir)
        self.callback(run_result)


class DockerEnvironment(InvokerEnvironment):
    def launch(self, command: str, file_system: typing.Optional[list[File]] = None,
               preserve_files: typing.Optional[list[str]] = None, timelimit: typing.Optional[int] = None,
               label: typing.Optional[str] = None) -> RunResult:
        pass


class NoInvokerPoolCallbackData(Exception):

    def __init__(self, invoker_id: int):
        self.invoker_id = invoker_id

    def __str__(self):
        return f"No pool connected to invoker: {self.invoker_id}"


class Invoker:
    def __init__(self):
        self.status: InvokerStatus = InvokerStatus.FREE
        self.environment = DockerEnvironment if settings.USE_DOCKER else NormalEnvironment
        self.callback_free_myself = None
        self._callback = None

    def run(self, command: str, files: typing.Optional[list[str | File]] = None,
            preserve_files: typing.Optional[list[str]] = None, timelimit: typing.Optional[int] = None,
            label: typing.Optional[str] = None,
            callback: typing.Optional[typing.Callable[[InvokerReport], None]] = None) -> InvokerProcess:
        file_system = [file if isinstance(file, File) else File.load(file) for file in files] if files else None

        self._callback = callback
        return self.environment(self.notify).launch(command, file_system, preserve_files=preserve_files, timelimit=timelimit, label=label)

    def notify(self, result: RunResult):
        report = self.make_report(result)
        self.send_report(report)

        self.free()

    def free(self):
        if self.callback_free_myself:
            self.callback_free_myself(self)
        else:
            raise NoInvokerPoolCallbackData(id(self))

    def make_report(self, result: RunResult) -> InvokerReport:
        report = InvokerReport.objects.create(command=result.command, time_start=result.time_start,
                                              time_end=result.time_end, exit_code=result.exit_code,
                                              output=result.output,
                                              status=InvokerReport.Status.OK if result.exit_code == 0 else InvokerReport.Status.RE,
                                              )
        if result.input_files:
            for file in result.input_files:
                report.input_files.add(
                    FileModel.objects.create(file=FileDjango(io.BytesIO(file.source.encode()), name=file.name),
                                             name=file.name))
            report.save()

        if result.preserved_files:
            for file in result.preserved_files:
                report.preserved_files.add(
                    FileModel.objects.create(file=FileDjango(io.BytesIO(file.source), name=file.name), name=file.name))
            report.save()

        return report

    def send_report(self, report: InvokerReport):
        if self._callback:
            self._callback(report)


__all__ = ["Invoker", "DockerEnvironment", "NormalEnvironment", "InvokerEnvironment", "RunResult",
           "InvokerStatus"]
