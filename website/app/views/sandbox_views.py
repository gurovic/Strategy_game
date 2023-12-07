import time
from typing import Any

from ..models.game import Game
from ..models import CompilerReport
from ..classes import FileLoader, save_file, Sandbox

from django.shortcuts import render
from django import forms


def get_compiler_report(file):
    class ToNotify:
        def __init__(self):
            self.report = None
            self.compiler_report = None

        def notify(self, report):
            self.report = report
            self.compiler_report = CompilerReport.objects.get(pk=self.report)

    path = save_file(file)
    file_loader_report_receiver = ToNotify()
    file_loader = FileLoader(path, file_loader_report_receiver.notify)

    while file_loader_report_receiver.compiler_report is None:
        time.sleep(1)
    return file_loader_report_receiver.compiler_report


def show(request, id):
    if request.method == 'POST':
        strategy = get_compiler_report(request.FILES['strategy'])
        if strategy.status == 0:
            game = Game.objects.get(pk=id)
            sandbox = Sandbox(game, strategy)
            report = sandbox.get_report()
            return render(request, 'sandbox_views.html', {'report': report})
        else:
            return render(request, 'sandbox_views.html', {'failed_report': strategy})
    else:
        return render(request, "sandbox_views.html", {})
