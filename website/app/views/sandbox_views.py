import time
import csv
from django.shortcuts import render

from ..models import CompilerReport, Game
from ..classes import Sandbox, SandboxNotifyReceiver, CompilerNotifyReceiver, LANGUAGES
from ..compiler import Compiler

LANGUAGES = {
    'c++': 'cpp',
    'c#': 'cs',
    'c': 'c',
    'python': 'py',
    'javascript': 'js',
    'java': 'Java',
}


def show(request, game_id):
    game = Game.objects.get(pk=game_id)
    if request.method == 'POST':
        if request.POST['type'] == 'compiler':
            file_content = request.FILES['strategy'].read()
            lang = request.POST['language']
            file_compiler = Compiler(file_content, LANGUAGES[lang], None)
            file_compiler.compile()

            return render(request, 'sandbox.html',
                          {'status': 'receive compiler report', 'report': file_compiler.report, 'game': game})
        elif request.POST['type'] == 'sandbox':
            compiler_report_id = request.POST['compiler_report_id']
            compiler_report = CompilerReport.objects.get(pk=compiler_report_id)
            sandbox = SandboxNotifyReceiver(game, compiler_report.compiled_file)

            try:
                # report = {}
                # sandbox.notify(report)
                sandbox.run()
            except ():
                return render(request, 'sandbox.html', {'status': 'none'})

            return render(request, 'sandbox.html',
                          {'status': 'receive sandbox report', 'game': game, 'report': sandbox.report})
        else:
            return render(request, 'sandbox.html', {'status': 'failed', 'game': game})
    else:
        return render(request, "sandbox.html",
                      {'status': 'filling compilation form', 'game': game, 'available_languages': LANGUAGES})
