from ..models.game import Game
from ..models import CompilerReport
from ..classes import FileLoader, save_file

from django.shortcuts import render
from django import forms


def compile(file):
    path = save_file(file)
    file_loader = FileLoader(path)
    compiler_report_id = file_loader.get_compiler_report_id()
    compiler_report = CompilerReport.objects.get(pk=compiler_report_id)
    return compiler_report


def show():
    pass