import time

from ..models.game import Game
from ..models import CompilerReport
from ..classes.sandbox import Sandbox
from ..compiler import Compiler

from django.shortcuts import render


class CompileFile:
    LANGUAGE = {
        'c++': 'cpp',
        'c#': 'cs',
        'c': 'c',
        'python': 'py',
        'javascript': 'js',
        'java': 'Java',
    }

    def __init__(self, file, lang):
        self.compiler = None
        self.report = None
        self.compiler_report = None
        self.file = file
        self.lang = self.LANGUAGE[lang]
        self.compiler = Compiler(self.file, self.lang, self.notify)

    def run(self):
        self.compiler.compile()

    def notify(self, report):
        self.report = report
        self.compiler_report = CompilerReport.objects.get(pk=self.report)


class CreateSandbox:
    def __init__(self, game, strategy):
        self.report = None
        self.game = game
        self.strategy = strategy
        self.sandbox = Sandbox(game, strategy, self.notify)

    def run(self):
        self.sandbox.run_battle()

    def notify(self, report):
        self.report = report


def show(request, id):
    if request.method == 'POST':
        print(request.POST['language'])
        file_compiler = CompileFile(request.FILES['strategy'], request.POST['language'])
        file_compiler.run()
        strategy = None
        while strategy is None:
            time.sleep(0.1)
            strategy = file_compiler.compiler_report

        if strategy.status == 0:
            game = Game.objects.get(pk=id)
            sandbox = CreateSandbox(game, strategy)
            report = sandbox.report()
            while report is None:
                time.sleep(0.1)
                report = sandbox.report()
            return render(request, 'sandbox.html', {'report': report})
        else:
            return render(request, 'sandbox.html', {'failed_report': strategy})
    else:
        return render(request, "sandbox.html", {})
