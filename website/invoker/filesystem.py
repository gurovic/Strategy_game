from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import logging
import shutil
import typing


_RawPathType = typing.Union[str, Path]


def _get_path(raw_path: _RawPathType) -> Path:
    if isinstance(raw_path, Path):
        return raw_path
    return Path(raw_path)


def delete_directory(directory: _RawPathType):
    shutil.rmtree(_get_path(directory), ignore_errors=True)


def write_file(file: _RawPathType, source: bytes = b""):
    _get_path(file).write_bytes(source)


def delete_file(file: _RawPathType):
    _get_path(file).unlink()


@dataclass
class File:
    name: str
    source: str | bytes

    def __post_init__(self):
        self.source = self.source if isinstance(self.source, bytes) else self.source.encode()

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


__all__ = ["File", "delete_directory", "write_file", "delete_file"]
