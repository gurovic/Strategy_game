from invoker.filesystem import Directory, File
from invoker.models import InvokerReport, File as FileModel

from django.conf import settings
from django.utils import timezone

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
import subprocess
import tempfile
import typing
import enum


class InvokerStatus(enum.Enum):
    FREE = enum.auto()
    WORKING = enum.auto()


@dataclass
class RunResult:
    command: str
    exit_code: int

    log: str

    time_start: datetime
    time_end: datetime

    files: typing.Optional[Directory] = None


class InvokerEnvironment(ABC):
    @abstractmethod
    def launch(self, command: str, file_system: typing.Optional[Directory] = None, preserve_files: typing.Optional[typing.List[str]] = None) -> RunResult:
        ...


class NormalEnvironment(InvokerEnvironment):
    @staticmethod
    def initialize_workdir(file_system: typing.Optional[Directory] = None) -> str:
        with tempfile.TemporaryDirectory() as tmpdir:
            file_system.make(tmpdir)
            return tmpdir

    def launch(self, command: str, file_system: typing.Optional[Directory] = None, preserve_files: typing.Optional[typing.List[str]] = None) -> RunResult:
        work_dir = self.initialize_workdir(file_system)

        time_start = timezone.now()
        result = subprocess.run(command, text=True, cwd=work_dir)
        time_end = timezone.now()

        if preserve_files:
            return_dir = Directory()
            for file in preserve_files:
                return_dir.add(File.load(file))
        else:
            return_dir = None

        return RunResult(
            command,
            result.returncode,
            result.stdout,
            time_start,
            time_end,
            return_dir
        )


class DockerEnvironment(InvokerEnvironment):
    def launch(self, command: str, file_system: typing.Optional[Directory] = None, preserve_files: typing.Optional[typing.List[str]] = None) -> RunResult:
        pass


class Invoker:
    def __init__(self):
        self.status: InvokerStatus = InvokerStatus.FREE
        self.environment = DockerEnvironment() if settings.USE_DOCKER else NormalEnvironment()

    def run(self, command: str, files: typing.Optional[typing.List[str]] = None, preserve_files: typing.Optional[typing.List[str]] = None, callback: typing.Optional[typing.Callable[[InvokerReport], None]] = None):
        if files:
            file_system = Directory()
            for file in files:
                file_system.add(File.load(file))
        else:
            file_system = None

        result = self.environment.launch(command, file_system, preserve_files=preserve_files)

        report = self.make_report(result)
        self.send_report(report, callback)

    def make_report(self, result: RunResult) -> InvokerReport:
        if result.files:
            files = [FileModel.objects.create()]
        return InvokerReport.objects.create(command=result.command, time_start=result.time_start,
                                            time_end=result.time_end, exit_code=result.exit_code, log=result.log,
                                            status=InvokerReport.Status.OK if result.exit_code == 0 else InvokerReport.Status.RE,
                                            files=X
                                            )

    def send_report(self, report: InvokerReport, callback: typing.Optional[typing.Callable[[InvokerReport], None]] = None):
        if callback:
            callback(report)
