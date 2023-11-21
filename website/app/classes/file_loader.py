import datetime
import logging
import random
import os
import time

from django.http import HttpResponse
from django.template import loader
from django.db import models

from app.models import CompilerReport
from app.compiler import Compiler


class FileLoader:
    # LOGGING TEXTS
    CREATOR_NOTIFYING = "FileLoader with id {} notifying it's own creator and finished it's work at {}"
    STARTING_COMPILATION = "FileLoader with id {} started compilation of it's file (path: {})"
    CREATED_FILE_LOADER = "FileLoader with id {} was created at {}"
    WRONG_FUNCTION_CALLING_ERROR = "Wrong calling of make_response function in class FileLoader with id {}"
    FILE_PATH_EXCEPTION = "FileLoader with id {} hadn't found file in {}"
    # OTHER CONSTS
    AVAILABLE_FORMATS = ['cpp', 'py', 'java', 'rs', 'cs', 'go', 'hs', 'kt', 'P', 'js', 'dpr', 'ts']

    def __init__(self, file_path: str):
        self.compiler_report = None
        logging.basicConfig(level=logging.INFO, filename="media/logs/file_loader.log", filemode='w',
                            format='%(asctime)s %(message)s', datefmt='%I:%M:%S')
        self.id = random.randint(1, 1000000000000000000)
        self.file_path = file_path
        self.lang = self.get_format(file_path)
        try:
            with open(self.file_path) as file:
                self.compiler = Compiler(file.read(), self.lang, self.notify)
        except:
            return
        logging.info(self.CREATED_FILE_LOADER.format(self.id, datetime.datetime.now().strftime("%Y%m%d")))
        self.compile()

    def make_response(self, exc: str):
        if exc == 'formatEXE':
            date = datetime.datetime.now().strftime("%Y%m%d")
            report = CompilerReport(compiled_file=None,
                                    time=0,
                                    datetime_created=date,
                                    error="Wrong file format",
                                    status=2,
                                    invoker_report=None)
            self.compiler_report = report
        elif exc == '404':
            logging.error(self.FILE_PATH_EXCEPTION.format(self.id, self.file_path))
            date = datetime.datetime.now().strftime("%Y%m%d")
            report = CompilerReport(
                compiled_file=None,
                time=0,
                datetime_created=date,
                status=2,
                error="No such file found {}".format(self.file_path),
                invoker_report=None)
            self.compiler_report = report
        else:
            logging.error(self.WRONG_FUNCTION_CALLING_ERROR.format(self.id))

    def compile(self):
        if not self.lang in self.AVAILABLE_FORMATS:
            return self.make_response("formatEXE")
        elif self.compiler_report is None:
            print('compiling started')
            logging.info(self.STARTING_COMPILATION.format(self.id, self.file_path))
            self.compiler.compile()

    def notify(self, compiler_report):
        print('compiling finished')
        logging.info(self.CREATOR_NOTIFYING.format(self.id, datetime.datetime.now()))
        self.compiler_report = compiler_report

    def get_compiler_report_id(self):
        while self.compiler_report is None:
            time.sleep(1)
        return self.compiler_report.id

    def get_format(self, file_path: str):
        try:
            with open(file_path):
                pass
            filename, file_extension = os.path.splitext(file_path)
            file_extension = file_extension[1:]
        except:
            self.make_response("404")
            return None
        return file_extension
