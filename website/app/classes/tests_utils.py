import os
from django.db import models
from django.core.files import File

from app.compiler import Compiler, CompilerReport


def compile_and_upload_to_file_field(objects_file_field: models.FileField, path_to_file: str, lang: str):
    def get_compiler_callback(report: CompilerReport):
        path_to_compiled_file = report.compiled_file.path
        name = path_to_compiled_file.split("/")[-1]
        local_file = open(path_to_compiled_file)
        django_file = File(local_file)
        objects_file_field.save(name, django_file)
        local_file.close()
        os.remove(path_to_compiled_file)

    path_to_file = os.path.abspath(path_to_file)
    compiler = Compiler(path_to_file, lang, get_compiler_callback)
    compiler.compile()