import time

from app.models import Game, CompilerReport
from app.classes import FileLoader, save_file, Sandbox

from django.shortcuts import render


class CompileFile:
    def __init__(self, file):
        self.report = None
        self.compiler_report = None
        self.file = file

    def run(self):
        path = save_file(self.file)
        file_loader = FileLoader(path, self.notify)

    def notify(self, report):
        self.report = report
        self.compiler_report = CompilerReport.objects.get(pk=self.report)


def show(request, id):
    if request.method == 'POST':
        file_compiler = CompileFile(request.FILES['strategy'])
        file_compiler.run()
        strategy = None
        while strategy is None:
            time.sleep(0.1)
            strategy = file_compiler.compiler_report

        if strategy.status == 0:
            game = Game.objects.get(pk=id)
            sandbox = Sandbox(game, strategy)
            report = sandbox.get_report()
            return render(request, 'sandbox.html', {'report': report})
        else:
            return render(request, 'sandbox.html', {'failed_report': strategy})
    else:
        return render(request, "sandbox.html", {})
