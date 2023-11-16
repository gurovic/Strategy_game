from invoker.filesystem import Directory, File
from invoker.models import InvokerReport

from django.conf import settings

from abc import ABC, abstractmethod
from dataclasses import dataclass
import subprocess
import tempfile
import random
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

    file_system: typing.Optional[Directory] = None


class InvokerEnvironment(ABC):
    @abstractmethod
    def launch(self, command: str, file_system: typing.Optional[Directory] = None, preserve_files=False) -> RunResult:
        ...


class NormalEnvironment(InvokerEnvironment):
    @staticmethod
    def initialize_workdir(file_system: typing.Optional[Directory] = None) -> str:
        with tempfile.TemporaryDirectory() as tmpdir:
            file_system.make(tmpdir)
            return tmpdir

    def launch(self, command: str, file_system: typing.Optional[Directory] = None, preserve_files=False) -> RunResult:
        work_dir = self.initialize_workdir(file_system)
        result = subprocess.run(command, text=True, cwd=work_dir)
        return RunResult(
            command,
            result.returncode,
            result.stdout,
            Directory.load(work_dir) if preserve_files else None
        )


class DockerEnvironment(InvokerEnvironment):
    def launch(self, command: str, file_system: typing.Optional[Directory] = None, preserve_files=False) -> RunResult:
        pass


class Invoker:
    def __init__(self, callback: typing.Optional[typing.Callable[[InvokerReport], None]] = None):
        self.id = random.randint(1000000000, 9999999999)
        self.callback = callback

        self.working_status: InvokerStatus = InvokerStatus.FREE
        self.environment = DockerEnvironment() if settings.USE_DOCKER else NormalEnvironment()

    def run(self, command: str, files: typing.Optional[typing.List[str]] = None, preserve_files: typing.Optional[bool] = False):
        if files:
            file_system = Directory("WorkDir")
            for file in files:
                file_system / File.load(file)
        else:
            file_system = None

        result = self.environment.launch(command, file_system, preserve_files=preserve_files)

        report = self.make_report(result)
        self.send_report(report)

    def make_report(self, result: RunResult) -> InvokerReport:
        pass

    def send_report(self, report: InvokerReport):
        if self.callback:
            self.callback(report)
