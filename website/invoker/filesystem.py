from __future__ import annotations

from dataclasses import dataclass, field
from abc import ABCMeta, abstractmethod
from pathlib import Path
import logging
import shutil
import typing


_RawPathType = typing.Union[str, Path]


def _get_path(raw_path: _RawPathType) -> Path:
    if isinstance(raw_path, Path):
        return raw_path
    return Path(raw_path)


def create_directory(directory: _RawPathType):
    _get_path(directory).mkdir()


def delete_directory(directory: _RawPathType):
    shutil.rmtree(_get_path(directory), ignore_errors=True)


def write_file(file: _RawPathType, source: bytes = b""):
    _get_path(file).write_bytes(source)


def delete_file(file: _RawPathType):
    _get_path(file).unlink()


class _MakeAble(metaclass=ABCMeta):
    @abstractmethod
    def make(self, path: Path):
        ...


@dataclass
class File(_MakeAble):
    name: str
    source: bytes

    @classmethod
    def load(cls, path: _RawPathType) -> File:
        path = _get_path(path)

        return cls(path.name, path.read_bytes())

    def make(self, path: _RawPathType):
        path = _get_path(path)

        if not (path/self.name).exists():
            write_file(path/self.name, self.source)
            logging.debug(f"File {path/self.name} was successfully created")
        else:
            delete_file(path/self.name)
            self.make(path)


@dataclass
class Directory(_MakeAble):
    name: typing.Optional[str] = None
    files: typing.List[File] = field(default_factory=list)
    directories: typing.List[Directory] = field(default_factory=list)

    @classmethod
    def load(cls, path: _RawPathType) -> Directory:
        path = _get_path(path)

        directory = cls(path.name)
        for entry in path.iterdir():
            if entry.is_dir():
                directory / cls.load(entry)
            else:
                directory / File.load(entry)

        return directory

    def __truediv__(self, other: typing.Union[File, Directory]) -> typing.Union[File, Directory]:
        return self.add(other)

    def _add_file(self, file: File) -> File:
        self.files.append(file)
        return file

    def _add_directory(self, directory: Directory) -> Directory:
        self.directories.append(directory)
        return directory

    def add(self, file_or_directory: typing.Union[File, Directory]) -> typing.Union[File, Directory]:
        if isinstance(file_or_directory, File):
            return self._add_file(file_or_directory)
        elif isinstance(file_or_directory, Directory):
            return self._add_directory(file_or_directory)

    def is_empty(self):
        return not (self.files or any(map(lambda x: not x.is_empty(), self.directories)))

    def make(self, path: _RawPathType):
        path = _get_path(path)

        if self.name:
            path = path / self.name

        if not self.is_empty():
            try:
                create_directory(path)
                logging.debug(f"Directory {path} was successfully created")
            except FileExistsError:
                delete_directory(path)
                self.make(path)
            for file in self.files:
                file.make(path)
            for directory in self.directories:
                directory.make(path)
