import datetime
import logging
import random

from django.http import HttpResponse
from django.template import loader
from django.db import models

from Strategy_game.invokersstructure.compiler import Compiler, CompilerReport


class FileLoader:
    # LOGGING TEXTS
    CREATOR_NOTIFYING = "FileLoader with id {} notifying it's own creator and finished it's work at {}"
    STARTING_COMPILATION = "FileLoader with id {} started compilation of it's file (path: {})"
    CREATED_FILE_LOADER = "FileLoader with id {} was created at {}"
    WRONG_FUNCTION_CALLING_ERROR = "Wrong calling of make_response function in class FileLoader with id {}"
    # OTHER CONSTS
    AVAILABLE_FORMATS = []  # Writes by Miroslav

    def __init__(self, file_path: str, creator):
        logging.basicConfig(level=logging.INFO, filename="../../../logs/boris.log", filemode='w',
                            format='%(asctime)s %(message)s', datefmt='%I:%M:%S')
        self.creator = creator
        self.id = random.randint(1, 1000000000000000000)
        self.file_path = file_path
        self.lang = self.get_format(file_path)
        self.compiler_report = None
        with open(self.file_path) as file:
            self.compiler = Compiler(file, self.lang, self.notify())
        logging.info(self.CREATED_FILE_LOADER.format(self.id, datetime.datetime.now().strftime("%Y%m%d")))
        self.compile()

    def make_response(self, exp: str):
        if exp == 'formatEXE':
            date = datetime.datetime.now().strftime("%Y%m%d")
            report = CompilerReport(None, 0, date, "ERROR", "Wrong file format", None)
            self.creator.notify(report)
        else:
            logging.error(self.WRONG_FUNCTION_CALLING_ERROR.format(self.id))

    def compile(self):
        if not self.lang in self.AVAILABLE_FORMATS:
            return self.make_response("formatEXE")
        else:
            logging.info(self.STARTING_COMPILATION.format(self.id, self.file_path))
            self.compiler.compile()

    def notify(self, compiler_report):
        logging.info(self.CREATOR_NOTIFYING.format(self.id, datetime.datetime.now()))
        self.compiler_report = compiler_report

    async def get_compiler_report(self):
        while self.compiler_report == None:
            pass
        return self.compiler_report

    @staticmethod
    def get_format(file_path: str):
        # writes by Miroslav
        return ".cpp"
