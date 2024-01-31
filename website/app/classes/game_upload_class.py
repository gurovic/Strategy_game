from ..compiler import *
import functools

class FileReport:
    def __int__(self, file, language, label, status=None):
        self.compiled_file = Compiler(file, language, functools.partial(notify, label))
        self.report = None
        self.status = status
        self.label = label
