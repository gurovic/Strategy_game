from invoker.filesystem import File, delete_directory
from invoker.models import InvokerReport, File as FileModel

from django.conf import settings
from django.utils import timezone
from django.core.files import File as FileDjango

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import subprocess
import tempfile
import logging
import typing
import enum
import io


class InvokerStatus(enum.Enum):
    FREE = enum.auto()
    WORKING = enum.auto()


@dataclass
class RunResult:
    command: str
    output: str
    exit_code: int

    time_start: datetime
    time_end: datetime

    timelimit: typing.Optional[int] = None
    exceeded_timelimit: bool = False

    input_files: typing.Optional[typing.List[File]] = None
    preserved_files: typing.Optional[typing.List[File]] = None


class InvokerEnvironment(ABC):
    @abstractmethod
    def launch(self, command: str, file_system: typing.Optional[typing.List[File]] = None,
               preserve_files: typing.Optional[typing.List[str]] = None, timelimit: typing.Optional[int] = None) -> RunResult:
        ...


class NormalEnvironment(InvokerEnvironment):
    @staticmethod
    def initialize_workdir(file_system: typing.Optional[typing.List[File]] = None) -> str:
        tmpdir = tempfile.mkdtemp()
        if file_system:
            for file in file_system:
                file.make(tmpdir)
        return tmpdir

    def launch(self, command, file_system: typing.Optional[typing.List[File]] = None,
               preserve_files: typing.Optional[typing.List[str]] = None, timelimit: typing.Optional[int] = None) -> RunResult:
        work_dir = self.initialize_workdir(file_system)

        time_start = timezone.now()

        logging.debug(
            f'Command \"{command}\" was launched with files={file_system}, preserve_files={preserve_files} and timelimit={timelimit}')

        try:
            result = subprocess.run(command.split() if isinstance(command, str) else command, text=True,
                                    stdout=subprocess.PIPE, cwd=work_dir, timeout=timelimit, shell=True)
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

        preserve_dir = [File.load(Path(work_dir) / file) for file in preserve_files] if preserve_files else None

        delete_directory(work_dir)

        return RunResult(
            command,
            result.stdout,
            return_code,
            time_start,
            time_end,
            timelimit,
            timeout_error,
            input_dir,
            preserve_dir
        )


class DockerEnvironment(InvokerEnvironment):
    def launch(self, command: str, file_system: typing.Optional[typing.List[File]] = None,
               preserve_files: typing.Optional[typing.List[str]] = None, timelimit: typing.Optional[int] = None) -> RunResult:
        pass


class Invoker:
    def __init__(self):
        self.status: InvokerStatus = InvokerStatus.FREE
        self.environment = DockerEnvironment() if settings.USE_DOCKER else NormalEnvironment()

    def run(self, command: str, files=None,
            preserve_files: typing.Optional[typing.List[str]] = None, timelimit: typing.Optional[int] = None,
            callback: typing.Optional[typing.Callable[[InvokerReport], None]] = None):
        file_system = [file if isinstance(file, File) else File.load(file) for file in files] if files else None

        result = self.environment.launch(command, file_system, preserve_files=preserve_files, timelimit=timelimit)

        report = self.make_report(result)
        self.send_report(report, callback)

        self.free()

    def free(self):
        # <== Костыль (Circular Import) ==>
        from invoker.invoker_pool import InvokerPool
        current_pool = InvokerPool()
        current_pool.free(self)

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

    def send_report(self, report: InvokerReport,
                    callback: typing.Optional[typing.Callable[[InvokerReport], None]] = None):
        if callback:
            callback(report)


__all__ = ["Invoker", "DockerEnvironment", "NormalEnvironment", "InvokerEnvironment", "RunResult",
           "InvokerStatus"]
