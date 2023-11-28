import time

from ..models.game import Game
from ..models import CompilerReport
from ..classes import FileLoader, save_file, Sandbox

from django.shortcuts import render
from django import forms


def compile(file):
    path = save_file(file)
    file_loader = FileLoader(path)

    compiler_report_id = None
    while compiler_report_id is None:
        try:
            compiler_report_id = file_loader.get_compiler_report_id()
        except:
            compiler_report_id = None
            time.sleep(1)

    compiler_report = None
    while compiler_report is None:
        try:
            compiler_report = CompilerReport.objects.get(pk=compiler_report_id)
        except:
            compiler_report = None
            time.sleep(1)
    return compiler_report


def show(request, id):
    if request.method == 'POST':
        strategy = compile(request.FILES['strategy'])
        if strategy.status == 0:
            game = Game.objects.get(pk=id)
            sandbox = Sandbox(game, strategy)
            report = sandbox.get_report()
            return render(request, 'sandbox_views.html', {'report': report})
        else:
            return render(request, 'sandbox_views.html', {'failed_report': strategy})
    else:
        return render(request, "sandbox_views.html", {})
