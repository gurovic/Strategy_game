from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from threading import Thread
from pathlib import Path
import subprocess
import tempfile
import logging
import typing
import enum
import io

from django.conf import settings
from django.utils import timezone
from django.core.files import File as FileDjango

from invoker.filesystem import File, delete_directory
from invoker.models import InvokerReport, File as FileModel


class InvokerStatus(enum.Enum):
    FREE = enum.auto()
    WORKING = enum.auto()


@dataclass
class RunResult:
    command: str
    output: str
    error: str
    exit_code: int | None

    time_start: datetime
    time_end: datetime

    timelimit: typing.Optional[int] = None
    exceeded_timelimit: bool = False

    label: typing.Optional[str] = None

    input_files: typing.Optional[list[File]] = None
    preserved_files: typing.Optional[list[File]] = None


class TimeoutExpired(Exception):
    def __init__(self, timelimit: int):
        self.timelimit = timelimit

    def __str__(self):
        return f"Timeout {self.timelimit} expired"



class StdIn(typing.Protocol):
    def write(self, data: str):
        ...


class StdOut(typing.Protocol):
    def read(self) -> str:
        ...

    def readline(self) -> str:
        ...


class InvokerProcess(ABC):
    stdin: StdIn
    stdout: StdOut

    def __init__(self, label: typing.Optional[str] = None, timelimit: typing.Optional[int] = None,
                 callback: typing.Optional[typing.Callable[[bool], None]] = None):
        self.label = label

        self.timelimit = timelimit
        self.callback = callback

        self._exceeded_timelimit = False

        if self.callback:
            self.register_callback()

    def register_callback(self):
        Thread(target=self._wait_for_end).start()

    @abstractmethod
    def wait(self):
        """Wait until process finished or raise TimeoutExpired if timelimit exceeded"""

    @abstractmethod
    def kill(self):
        """Kill process"""

    def connect(self, input: str) -> str:
        self.stdin.write(input)
        return self.stdout.readline()

    def _wait_for_end(self):
        try:
            self.wait()
        except TimeoutExpired:
            self.kill()
            self._exceeded_timelimit = True
        self.send_callback()

    def send_callback(self):
        if self.callback:
            self.callback(self._exceeded_timelimit)


class NormalProcess(InvokerProcess):
    def __init__(self, process: subprocess.Popen, *args, **kwargs):
        self._process = process
        self.stdin = self._process.stdin
        self.stdout = self._process.stdout

        super().__init__(*args, **kwargs)

    def wait(self):
        try:
            self._process.wait(self.timelimit)
        except subprocess.TimeoutExpired:
            raise TimeoutExpired(self.timelimit)

    def kill(self):
        self._process.kill()


class InvokerEnvironment(ABC):
    @abstractmethod
    def launch(self, command: str, file_system: typing.Optional[list[File]] = None,
               preserve_files: typing.Optional[list[str]] = None, timelimit: typing.Optional[int] = None) -> RunResult:
        ...


class NormalEnvironment(InvokerEnvironment):
    @staticmethod
    def initialize_workdir(file_system: typing.Optional[list[File]] = None) -> str:
        tmpdir = tempfile.mkdtemp()
        if file_system:
            for file in file_system:
                file.make(tmpdir)
        return tmpdir

    def launch(self, command: str, file_system: typing.Optional[list[File]] = None,
               preserve_files: typing.Optional[list[str]] = None, timelimit: typing.Optional[int] = None) -> RunResult:
        work_dir = self.initialize_workdir(file_system)

        time_start = timezone.now()

        logging.debug(
            f'Command \"{command}\" was launched with files={file_system}, preserve_files={preserve_files} and timelimit={timelimit}')

        try:
            result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=work_dir,
                                    timeout=timelimit, shell=True)
            return_code = result.returncode
            timeout_error = False
            logging.debug(f"Command \"{command}\" launch was ended with exit code {return_code}!")
        except subprocess.TimeoutExpired as exc:
            logging.debug(f"Command \"{command}\" launch time was exceeded timelimit!")
            result = exc
            return_code = None
            timeout_error = True

        time_end = timezone.now()

        input_dir = [file for file in file_system] if file_system else None

        path = Path(work_dir)
        preserve_dir = [File.load(path / file) for file in preserve_files if
                        (path / file).exists()] if preserve_files else None

        delete_directory(work_dir)

        return RunResult(
            command,
            result.stdout,
            result.stderr,
            return_code,
            time_start,
            time_end,
            timelimit,
            timeout_error,
            input_dir,
            preserve_dir
        )


class DockerEnvironment(InvokerEnvironment):
    def launch(self, command: str, file_system: typing.Optional[list[File]] = None,
               preserve_files: typing.Optional[list[str]] = None, timelimit: typing.Optional[int] = None) -> RunResult:
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
        return self.environment(self.notify).launch(command, file_system, preserve_files=preserve_files,
                                                    timelimit=timelimit, label=label)

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
                                              status=InvokerReport.Status.TL if result.exceeded_timelimit else InvokerReport.Status.OK if result.exit_code == 0 else InvokerReport.Status.RE)
        if result.input_files:
            for file in result.input_files:
                report.input_files.add(
                    FileModel.objects.create(file=FileDjango(io.BytesIO(file.source), name=file.name), name=file.name))
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
           "InvokerStatus", "NoInvokerPoolCallbackData", "InvokerProcess", "NormalProcess", "TimeoutExpired"]
