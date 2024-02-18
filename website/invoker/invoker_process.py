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

from django.conf import settings
from django.utils import timezone
from django.core.files import File as FileDjango

from invoker.filesystem import File, delete_directory
from invoker.models import InvokerReport, File as FileModel
from invoker.invoker import RunResult


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
